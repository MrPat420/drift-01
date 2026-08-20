#!/usr/bin/env python3
"""
KEY ROTOR — Gemini API key rotation with SQLite quota tracking
================================================================
The single front door for ALL Gemini calls across every research engine.

Why this exists:
  Free Gemini keys allow ~1,500 requests/day each, then hard-stop with 429.
  Instead of waiting for the error (reactive), we COUNT usage proactively and
  rotate to the next key at a safe threshold, leaving a buffer. Free keys are
  spent first; the paid key (KEY_1) is the last-resort fallback.

Design rule (critical):
  NOTHING calls a Gemini key directly. Every engine imports this module and
  calls `gemini_request()`. This is what keeps the SQLite counter from drifting
  — there is no path to a key that bypasses the counter.

Quota reset:
  Google's free-tier daily quota resets at midnight Pacific. The counter keys
  every row by (key_id, pacific_date), so a new day automatically starts fresh
  without us deleting anything (full history is retained for analytics).
"""

import os
import sqlite3
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------

# Daily request ceiling per free key. Google's published free-tier limit is
# 1,500/day for flash models; we rotate BEFORE hitting it to leave a buffer.
FREE_KEY_DAILY_LIMIT = 1500
SAFETY_BUFFER        = 100          # rotate when this many requests remain
ROTATE_AT            = FREE_KEY_DAILY_LIMIT - SAFETY_BUFFER   # = 1400

# Pacific offset for quota-reset bucketing. Google resets at midnight PT.
# PST = UTC-8, PDT = UTC-7. We use -8 as the bucketing anchor; being off by an
# hour at the DST boundary only shifts the reset moment slightly and never
# causes over-counting, so this is safe without a full tz database.
PACIFIC_OFFSET = timedelta(hours=-8)

# Where the quota database lives. On Mr_Pat's box this should resolve under the
# real home; the env override lets engines point at a shared DB if desired.
DB_PATH = Path(os.getenv("KEY_ROTOR_DB", Path.home() / ".key_rotor" / "quota.db"))

# Gemini key precedence: FREE keys spent first (2..5), PAID key (1) last.
# The order of this list IS the rotation priority.
KEY_ENV_ORDER = [
    ("GEMINI_KEY_2", "free"),
    ("GEMINI_KEY_3", "free"),
    ("GEMINI_KEY_4", "free"),
    ("GEMINI_KEY_5", "free"),
    ("GEMINI_KEY_1", "paid"),   # fallback — effectively unlimited / billed
]

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)
DEFAULT_MODEL = "gemini-2.5-flash"


# ----------------------------------------------------------------------------
# ENV LOADING — read keys from ~/.env (runtime source of truth)
# ----------------------------------------------------------------------------

def _load_env_keys():
    """Parse ~/.env directly. Avoids the .bashrc non-interactive guard that
    silently fails to export keys in scripted shells."""
    keys = {}
    env_path = Path.home() / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    # Environment overrides .env if both present
    for k, _ in KEY_ENV_ORDER:
        if os.getenv(k):
            keys[k] = os.getenv(k)
    return keys


# ----------------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------------

def _pacific_date(dt=None):
    """Return the YYYY-MM-DD string in Pacific time for quota bucketing."""
    dt = dt or datetime.now(timezone.utc)
    return (dt + PACIFIC_OFFSET).strftime("%Y-%m-%d")


@contextmanager
def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _init_db():
    with _db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usage (
                key_id        TEXT NOT NULL,
                pacific_date  TEXT NOT NULL,
                tier          TEXT NOT NULL,
                count         INTEGER NOT NULL DEFAULT 0,
                last_used_utc TEXT,
                PRIMARY KEY (key_id, pacific_date)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                ts_utc    TEXT NOT NULL,
                key_id    TEXT NOT NULL,
                status    INTEGER,
                note      TEXT
            )
        """)


def _get_count(conn, key_id, day):
    row = conn.execute(
        "SELECT count FROM usage WHERE key_id=? AND pacific_date=?",
        (key_id, day),
    ).fetchone()
    return row["count"] if row else 0


def _bump(conn, key_id, tier, day):
    conn.execute("""
        INSERT INTO usage (key_id, pacific_date, tier, count, last_used_utc)
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT(key_id, pacific_date)
        DO UPDATE SET count = count + 1, last_used_utc = excluded.last_used_utc
    """, (key_id, day, tier, datetime.now(timezone.utc).isoformat()))


def _log_event(conn, key_id, status, note):
    conn.execute(
        "INSERT INTO events (ts_utc, key_id, status, note) VALUES (?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(), key_id, status, note),
    )


# ----------------------------------------------------------------------------
# ROTOR CORE
# ----------------------------------------------------------------------------

class NoKeysAvailable(Exception):
    """Raised when every free key is exhausted AND no paid fallback is set."""


def _select_key(keys, day):
    """Return (env_name, tier, key_value) for the first key with headroom.
    Free keys are tried in order; each must be under ROTATE_AT. The paid key
    has no local ceiling (billed), so it's always eligible as the fallback."""
    with _db() as conn:
        for env_name, tier in KEY_ENV_ORDER:
            key_value = keys.get(env_name)
            if not key_value:
                continue  # key not configured, skip
            if tier == "paid":
                return env_name, tier, key_value  # always eligible
            used = _get_count(conn, env_name, day)
            if used < ROTATE_AT:
                return env_name, tier, key_value
    raise NoKeysAvailable(
        f"All free keys at/over {ROTATE_AT} for {day} and no paid fallback configured."
    )


def gemini_request(prompt, model=DEFAULT_MODEL, max_tokens=2000,
                   generation_config=None, tools=None, timeout=60):
    """
    THE FRONT DOOR. Make a Gemini call through the rotor.

    Counts the request against the selected key's daily quota, rotates
    automatically when a free key nears its limit, and falls back to the paid
    key only when all free keys are spent.

    Returns the parsed JSON response dict on success.
    Raises NoKeysAvailable if nothing can serve the request.
    """
    _init_db()
    keys = _load_env_keys()
    day = _pacific_date()

    # Try keys in priority order; on a real 429 (quota), mark that key spent
    # for the day and advance. This makes the counter self-correcting even if
    # an external process burned some quota we didn't see.
    attempted = set()
    while True:
        env_name, tier, key_value = _select_key(keys, day)
        if env_name in attempted and tier != "paid":
            # avoid tight loop on the same free key
            with _db() as conn:
                # force this key to its ceiling so _select_key advances
                conn.execute("""
                    INSERT INTO usage (key_id, pacific_date, tier, count, last_used_utc)
                    VALUES (?,?,?,?,?)
                    ON CONFLICT(key_id, pacific_date)
                    DO UPDATE SET count = MAX(count, ?)
                """, (env_name, day, tier, ROTATE_AT,
                      datetime.now(timezone.utc).isoformat(), ROTATE_AT))
            continue
        attempted.add(env_name)

        body = {"contents": [{"parts": [{"text": prompt}]}]}
        cfg = {"maxOutputTokens": max_tokens}
        if generation_config:
            cfg.update(generation_config)
        body["generationConfig"] = cfg
        if tools:
            body["tools"] = tools

        url = GEMINI_ENDPOINT.format(model=model)
        try:
            r = requests.post(url, params={"key": key_value},
                              json=body, timeout=timeout)
        except Exception as e:
            with _db() as conn:
                _log_event(conn, env_name, None, f"network error: {e}")
            # network failure isn't a quota problem; advance to next key
            if tier == "paid":
                raise
            continue

        # Count the attempt regardless of outcome (it consumed quota unless
        # it was a hard auth/quota rejection, which we handle below).
        if r.status_code == 200:
            with _db() as conn:
                _bump(conn, env_name, tier, day)
                _log_event(conn, env_name, 200, "ok")
            return r.json()

        if r.status_code == 429:
            # quota exhausted on this key — mark spent, advance
            with _db() as conn:
                conn.execute("""
                    INSERT INTO usage (key_id, pacific_date, tier, count, last_used_utc)
                    VALUES (?,?,?,?,?)
                    ON CONFLICT(key_id, pacific_date)
                    DO UPDATE SET count = ?, last_used_utc = excluded.last_used_utc
                """, (env_name, day, tier, FREE_KEY_DAILY_LIMIT,
                      datetime.now(timezone.utc).isoformat(), FREE_KEY_DAILY_LIMIT))
                _log_event(conn, env_name, 429, "quota exhausted -> rotate")
            if tier == "paid":
                raise NoKeysAvailable("Paid key returned 429.")
            continue

        # other errors (4xx/5xx): log and advance, but count the consumed call
        with _db() as conn:
            _bump(conn, env_name, tier, day)
            _log_event(conn, env_name, r.status_code, r.text[:200])
        if tier == "paid":
            r.raise_for_status()
        # else advance to next key


# ----------------------------------------------------------------------------
# STATUS / REPORTING
# ----------------------------------------------------------------------------

def status():
    """Return today's per-key usage as a list of dicts (for the dashboard)."""
    _init_db()
    keys = _load_env_keys()
    day = _pacific_date()
    out = []
    with _db() as conn:
        for env_name, tier in KEY_ENV_ORDER:
            configured = bool(keys.get(env_name))
            used = _get_count(conn, env_name, day)
            if tier == "free":
                remaining = max(0, FREE_KEY_DAILY_LIMIT - used)
                headroom = max(0, ROTATE_AT - used)
            else:
                remaining = None  # unlimited / billed
                headroom = None
            out.append({
                "key": env_name,
                "tier": tier,
                "configured": configured,
                "used_today": used,
                "remaining": remaining,
                "rotate_headroom": headroom,
            })
    return {"pacific_date": day, "rotate_at": ROTATE_AT, "keys": out}


def print_status():
    s = status()
    print(f"\n  KEY ROTOR STATUS — Pacific date {s['pacific_date']}  (rotate at {s['rotate_at']})")
    print("  " + "-" * 66)
    print(f"  {'KEY':<16}{'TIER':<8}{'USED':>8}{'REMAIN':>10}{'HEADROOM':>12}")
    print("  " + "-" * 66)
    for k in s["keys"]:
        if not k["configured"]:
            print(f"  {k['key']:<16}{k['tier']:<8}{'—':>8}{'not set':>10}{'':>12}")
            continue
        rem = "∞" if k["remaining"] is None else str(k["remaining"])
        hr  = "∞" if k["rotate_headroom"] is None else str(k["rotate_headroom"])
        print(f"  {k['key']:<16}{k['tier']:<8}{k['used_today']:>8}{rem:>10}{hr:>12}")
    print("  " + "-" * 66 + "\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print_status()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        # Live smoke test — makes ONE real billable call through the rotor.
        print("Making one test call through the rotor...")
        resp = gemini_request("Reply with the single word: OK")
        text = (resp.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", ""))
        print(f"Response: {text.strip()!r}")
        print_status()
    else:
        print("Usage: key_rotor.py [status|test]")
        print("  status  — show today's per-key quota usage")
        print("  test    — make one real call through the rotor and show status")
