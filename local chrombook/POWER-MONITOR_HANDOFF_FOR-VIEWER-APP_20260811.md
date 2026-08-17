# POWER-MONITOR (PROJ_066) — FULL SYSTEM HANDOFF FOR VIEWER-APP BUILD
**Doc-ID:** POWER-MONITOR_HANDOFF_FOR-VIEWER-APP · **Date:** 2026-08-11 · **Origin:** C2, from verified source reads this session
**Provenance discipline:** Everything below is VERIFIED from the live system unless tagged [UNVERIFIED — confirm at source].

---

## 1. WHAT THE SYSTEM IS

A two-part power telemetry pipeline on the Kali workstation (i9-14900K + RTX 3060), running 24/7 as a systemd service, purpose-built around one hardware quirk: **the GPU disappears from the host whenever it's passed through to the win11-wife VM** (VFIO passthrough for evening gaming). The system measures what it can, flags what it can't, and estimates the gap at report time.

**Components (all in `/home/mrpat/projects/power-monitor/` on kali):**

| File | Size | Role |
|---|---|---|
| `collector.py` | 9,909 B | Daemon. Samples CPU + GPU watts every 60s, appends one CSV row |
| `report.py` | 6,971 B | On-demand. Integrates the CSV to kWh, applies multipliers, prints cost in soles |
| `power_log.csv` | ~253 KB and growing | The dataset — one row per minute since ~2026-08-03 |
| `power-monitor.service` | 343 B | systemd unit keeping collector.py alive [UNVERIFIED contents — `cat` it to confirm restart policy] |
| `ollama_history.log` | 38 MB | [UNVERIFIED role — likely Ollama activity log for correlating inference load with power draw; confirm before using] |

---

## 2. THE DATA — power_log.csv (this is what your app reads)

**Schema, verified from collector.py source:**
```
timestamp_iso, cpu_watts, gpu_watts, domain_used, vm_active
```

| Column | Meaning |
|---|---|
| `timestamp_iso` | ISO datetime of the sample |
| `cpu_watts` | CPU package power, measured via Intel RAPL energy counters (`/sys/class/powercap/intel-rapl/.../energy_uj`, two reads ~1s apart, delta → watts) |
| `gpu_watts` | GPU draw via `nvidia-smi --query power.draw`. **0.000 when vm_active=1** (host can't see the GPU during passthrough) |
| `domain_used` | Which RAPL domain the CPU figure came from [UNVERIFIED exact values — likely `package-0` or similar; check distinct values in the CSV] |
| `vm_active` | 1 = GPU passed through to a running QEMU/KVM VM (detected via lspci/QEMU process check), 0 = host owns GPU |

**Data properties your app must handle:**
- One row per ~60 seconds; **gaps exist** (collector skips bad samples by design, machine reboots leave holes). Never assume continuous rows — integrate over actual timestamp deltas.
- `gpu_watts=0` is ambiguous alone; it means "unmeasurable" only when `vm_active=1`. Your app must substitute an estimate for those intervals (default 160W) or display them as a distinct "VM gaming" category — that's the honest rendering.
- File is append-only, written every 60s. Safe to read live (reader may catch a partially-written last line — discard any malformed final row).
- ~1,440 rows/day → ~525K rows/year. Trivial for pandas/SQLite; plan for it anyway.

---

## 3. THE MATH — how report.py turns rows into soles (replicate this in your app)

Verified from source and --help:

1. **Integrate:** for each pair of consecutive rows, energy = watts × Δt. Sum over window → kWh per component (CPU measured, GPU measured, GPU estimated-during-VM).
2. **VM substitution:** intervals where `vm_active=1` get `--gpu-vm-watts` (default **160**) in place of the recorded 0. Measured vs estimated GPU energy are reported **separately** — keep that separation in the app; it's the honesty layer.
3. **Wall multiplier:** subtotal × `--multiplier` (default **1.5**) — accounts for PSU inefficiency, motherboard/RAM/drives/fans not covered by RAPL, monitor, peripherals. This is a calibration knob: the day a kill-a-watt meter measures the real wall draw, this gets tuned.
4. **Cost:** kWh × `--rate` (soles per kWh). Rate is user-supplied every run — **not stored anywhere in the system.** Your app should store it as a setting (Luz del Sur all-in estimate: S/ 0.75–0.85; real number comes off the bill).
5. **Projection block:** average wall watts over the covered window, extrapolated to a full month [UNVERIFIED exact output format — run the report once and capture stdout before parsing it].

**CLI contract (verified from --help):**
```
report.py (--month YYYY-MM | --since ISO) --rate RATE [--multiplier 1.5] [--gpu-vm-watts 160]
```

---

## 4. KNOWN OPERATING CONTEXT (what the numbers mean physically)

- **Day profile:** host owns GPU → Ollama/local-LLM inference loads (RTX 3060 12GB working). gpu_watts real.
- **Night profile:** VM takes GPU (Natasha's gaming, L4D2 etc.) → vm_active=1, GPU estimated. A libvirt hook restarts ollama.service 8s after the VM releases the GPU — the vm_active 1→0 transitions in the CSV mark those handbacks.
- Baselines previously captured: idle, gaming, inference wattage [figures live at the kali seat, not in this doc].
- Data starts ~2026-08-03. Any "monthly" report before September is a partial-month projection.

---

## 5. VIEWER-APP BUILD NOTES (recommendations, not requirements)

- **Read the CSV directly** — it's the single source of truth, append-only, and the path is stable: `/home/mrpat/projects/power-monitor/power_log.csv`. No need to touch collector.py.
- Natural views: live wattage (tail of CSV), daily kWh bars stacked by CPU/GPU-measured/GPU-estimated, cost-to-date vs projected month, VM-hours per day (Natasha's gaming time falls out of the data for free), inference-load correlation if ollama_history.log proves parseable.
- Serve it the way the portfolio already works: small FastAPI reading the CSV + a web front end, same stack pattern as Y-TIP. Runs on kali, viewable from phone/Chromebook over the LAN/Tailscale.
- **Do not write to the CSV, ever.** Collector owns it. App is read-only on it. If the app needs its own state (rate setting, calibration), separate file.
- Settings the app should own: rate (S/ per kWh), multiplier, gpu-vm-watts — the three knobs report.py takes per-run.

## 6. OPEN ITEMS AGAINST THIS SYSTEM
1. Real S/ per kWh from a Luz del Sur bill — replaces the 0.80 estimate everywhere.
2. `cat power-monitor.service` — confirm restart policy + that it's `enabled` (survives reboot).
3. One full `report.py` run captured to file — pins the exact output format before any parser is written.
4. Wall-multiplier calibration against a real watt meter — someday, not urgent.
5. ollama_history.log format check — determines whether inference-correlation view is buildable.

**END HANDOFF — everything above verified at source this session except items tagged otherwise.**
