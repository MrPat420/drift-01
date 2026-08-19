> **AUTHORITY NOTE — 2026-07-10:** /home/mrpat/gem01/registry_current.json
> (v4, 45 entries) is the machine-canonical registry. The GEM-01 classifier
> reads it directly. This .md is the human-facing log; when the two conflict,
> the JSON wins. Registry changes are made by patch script, then noted here.

# MASTER PROJECT REGISTRY
Last updated: 2026-05-31
Maintained by: Shaun Patrick Kelly (mrpat)
Rule: Every project gets an entry. Claude keeps this in sync.

---

## STATUS KEY
- 🟢 COMPLETE    — closed, archived
- 🔵 IN WORK     — actively being executed
- 🟡 OPEN        — decided, not yet started
- ⚪ FUTURE      — planned/possible, not yet decided

---

## PROJECTS

### 🟢 BOFA-01 — Bank of America Fraud Recovery
- **Status:** ✅ CLOSED — SEALED 2026-06-14. All credits confirmed, no open items.
- **Recovered:** $1,905.88 total. BofA permanently credited both claims May 27 2026.
- **Claim 5775:** $602.37 permanently credited (May 27 2026 letter)
- **Claim 5964:** $234.40 permanently credited (May 27 2026 letter + June statement) — BofA: "no relevant documents"
- **Archive (current):** /home/mrpat/fraud_analysis_ARCHIVE_2026-06-14.tar.gz + .sha256 (1.6G, sha256 d6c5bab6…, includes sealed FINANCIAL_STATUS_FINAL.md). Prior snapshot 2026-05-29 retained.
- **Financial status:** /home/mrpat/fraud_analysis/legal_docs/FINANCIAL_STATUS_FINAL.md (SEALED) — supersedes FINANCIAL_STATUS_2026-05-30.md
- **Notes:** $234.40 confirmed landed on June 2026 statement (2026-06-14). Fully closed, cannot re-deny. Tarball rebuilt 2026-06-14 (verified). GDrive upload: DEFERRED — archival-only, not a blocker; BOFA-01 considered closed without it. MP unanswered liability $939.76 tracked under MP-01.

---

### 🔵 MP-01 — MercadoPago Accountability (Peru)
- **Status:** IN WORK — Phase 2 active
- **Goal:** Hold MercadoPago legally accountable for fraud facilitation, 9-month stonewall, and fabricated evidence submission.
- **Venue:** INDECOPI (primary) + DIVINDAT/Fiscalía (secondary)
- **Working dir:** /home/mrpat/fraud_analysis/
- **Legal docs:** /home/mrpat/fraud_analysis/legal_docs/peru_legal/
- **Local rep:** Alien (Carta Poder required)
- **Hard gate:** Peru lawyer + Alien review must happen before any filing
- **Next actions:**
  - [ ] Lawyer/Alien review of MP matter — CARTA PODER DRAFT READY
  - [x] Carta Poder draft created (EN + ES) — 2026-05-30
  - [x] ARCO data request FILED — 2026-05-30 (awaiting response, due 2026-06-20)
  - [ ] Carta Poder execution (expired passport workaround TBD by lawyer)
  - [ ] Fuller MP transaction export
  - [ ] June 7 2025 OTP timestamp alignment
  - [ ] DIVINDAT denuncia
  - [ ] INDECOPI complaint

---

### 🟡 MP-02 — MercadoPago Accountability (US side)
- **Status:** OPEN — placeholder
- **Goal:** US-side legal options TBD (FTC, CFPB, civil, etc.)
- **Legal docs:** /home/mrpat/fraud_analysis/legal_docs/us_legal/
- **Dependency:** Peru tracks must inform US strategy
- **Notes:** Not yet scoped. Awaiting lawyer guidance.

---

### ⚪ SYS-01 — Kali Linux Desktop Repair (LightDM)
- **Status:** FUTURE — low priority pending legal work
- **Goal:** Restore LightDM auto-launch on boot (broken after GParted resize)
- **Workaround active:** sudo pkill -9 Xorg && sleep 2 && startxfce4
- **Next actions (when prioritized):**
  - [ ] grep EE /var/log/Xorg.0.log
  - [ ] sudo systemctl disable lightdm && sudo systemctl enable lightdm
  - [ ] Consider reinstalling lightdm + lightdm-gtk-greeter (needs USB tether via Xiaomi)
  - [ ] Fallback: switch to SDDM

---

### 🔵 JFK-01 — JFK Assassination Research
- **Status:** ACTIVE
- **Working dir:** /mnt/linux_data/jfk_research/

---

### 🔵 UAP-01 — UAP Research
- **Status:** ACTIVE
- **Working dir:** /mnt/linux_data/uap_research/

---

## ADDING A NEW PROJECT
Copy this template:

- **Status:**
- **Goal:**
- **Working dir:**
- **Notes:**

### 🔵 BOFA-02 — Bank of America Consequential Damages + Bad Faith
- **Status:** IN WORK
- **Goal:** Recover $715.53 consequential damages + $4,500 statutory + $2,146.59 93A treble = $7,362.12 total
- **Posture:** Bad faith conduct + pattern of deception + document refusal. Fraud claims credited May 27 2026.
- **Venues:** CFPB · OCC · FTC · Massachusetts AG / Chapter 93A · Veterans Legal Services
- **Key weapon:** Two-hour capitulation May 27 = willful bad faith under 93A §9(3)
- **Legal docs:** /home/mrpat/fraud_analysis/legal_docs/us_legal/drafts/
- **Contacts:** BofA Rep Rita ID 9WFN5 · BofA Fax 1-866-905-9072 · VLS (857) 317-4474
- **Next actions:**
  - [ ] Lawyer review all four documents
  - [ ] Verify DHL $85.00 receipt on disk
  - [ ] Redact SSN from DD-214 before filing as Exhibit H
  - [ ] Send 93A demand by certified mail + fax simultaneously
  - [ ] File CFPB v3, OCC v3, FTC v3 online
  - [ ] Call Veterans Legal Services: (857) 317-4474

---

### 🟡 BABY-BACKROOMS — Kelly Family Horror Short Film
**Status:** PLANNING
**Created:** 2026-05-31
**Type:** Creative / Family Short Film

Family horror short. The Backrooms have not just reached the Kelly house — they *started* here. The lore hook: kids' rooms are the same color (yellow), matching canonical Backrooms aesthetics. The expansion radiates outward from the house, not inward.

**Working title:** Baby Back Rooms

- Canonical Backrooms: fluorescent-lit, yellow-wallpapered liminal space
- Kelly house twist: the rooms were always this color — the Backrooms didn't invade, they originated here
- Kids' rooms = Ground Zero

- Claude: story structure, script, lore consistency, shot list
- Image AI (SD WebUI on Kali): concept art, scene stills, poster
- Gemini: unstructured scene descriptions, atmosphere notes

- [ ] Sketch the narrative arc (origin story vs. discovery story)
- [ ] Map house layout to Backrooms zones
- [ ] Decide format: short film, photo essay, or YouTube creepypasta
- [ ] Generate first concept art on SD WebUI

- Project root: /home/mrpat/projects/baby_backrooms/

### ⚪ KELLY-THEORY-01 — Subject's Original Concepts
- **Status:** FUTURE — stub active, extraction pending
- **Goal:** Document subject's original theories and concepts: structural reinforcement drone, Leary biocomputer protocol, and additional concepts as identified from JSON
- **Working dir:** /home/mrpat/projects/KELLY-THEORY-01/
- **Master doc:** KELLY-THEORY-01_MASTER_2026-06-04.md
- **Cross-ref:** PERU-INTEL-01 Sections 22–23
- **Keywords:** kill chain, autonomous drone, DoD authentication, NATO drone security
- **Notes:** Two confirmed concepts seeded. Drone origin likely [4958]. Leary cluster [767]–[772]. Full pulls pending.

---

### ⚪ SHAMROCK-01 — Pre-Peru Origin Arc
- **Status:** FUTURE — stub active, extraction pending
- **Goal:** Document subject's pre-Peru history: birth record, Connecticut period, Gathering of the Vibes, Sikorsky/PT Barnum, Jonathan Kelly / 3 Chromebooks
- **Working dir:** /home/mrpat/projects/SHAMROCK-01/
- **Master doc:** SHAMROCK-01_MASTER_2026-06-04.md
- **Cross-ref:** PERU-INTEL-01 (entry [622] Connecticut Dossier)
- **Notes:** Birth Oct 30 1974, Apgar 1, 3 transfusions, released Nov 5. Full JSON pull pending.

---






## 🔴 DETENTION-01 — Peru Involuntary Detentions
**Status:** OPEN — Documentation phase
**Priority:** HIGH
**Facts:** Two involuntary detentions in Peru alleged by operator, same common-law spouse as actor. Detention B (~2 yrs, ~2019–2021) is CORPUS-CONFIRMED (berkshirebuds entry 59, hash 20c253b9b7b4). Detention A (~1 yr) is OPERATOR TESTIMONY ONLY — not located in any of 5 searched accounts; no corpus signal either way. Do not treat A as established fact absent facility records or non-corpus corroboration.
**Vienna Convention Art. 36:** OPEN QUESTION — whether US Embassy Lima was ever notified of Detention B is not established by the corpus (entry 59 documents denial of lawyer contact and controlled family calls; it does not document a requested-and-denied consular contact, nor prove the Embassy was never notified). Details about "multiple requests to facility staff" and "facility contacted wife" are operator testimony from prior sessions, not corpus-sourced. Recast as an open thread, not a settled violation. See DETENTION-01_MASTER.md OPEN THREADS #4.
**Pattern:** IF Detention A is substantiated, two detentions by same alleged actor with same denial-of-rights methodology = pattern of coercive control. Pattern is conditional on A, which is currently testimony-only.
**Related:** CHILDSUPPORT-01, BBUDS-01
**Action needed:** Independent legal counsel — outside family. US Embassy Lima ACS: +51 1 618-2000
**Resources:** Veterans Legal Services 857-317-4474
**Corpus source:** berkshirebuds entry 59, Oct 2025

## 🟡 CHILDSUPPORT-01 — US Child Support / VA Disability
**Status:** OPEN — Jurisdiction review needed
**Priority:** MEDIUM
**Facts:** $100K arrears, 100% VA disability, two kids in Peru, US court-ordered
**Legal issues:** VA disability generally exempt from garnishment under federal law. Peru-US jurisdiction complexity on enforcement.
**Action needed:** Family law attorney with international experience
**Resources:** Veterans Legal Services 857-317-4474
**Related:** DETENTION-01

## 🔵 BIOMARK-01 — Hemp DNA Currency Security Integration
**Status:** CONCEPT — Pre-AI era original, needs full DD
**Priority:** LOW (pending)
**Concept:** Hemp DNA strains grown in Hinsdale MA, classified integration into Crane & Co. paper products (Dalton MA — US currency/passport manufacturer). Geographic adjacency to 374 Maple St operation was intentional.
**Origin:** Pre-AI era concept, conceived in Berkshire County MA
**Related:** BBUDS-01, Crane & Co. Dalton MA
**Action needed:** DD from corpus — extract all entries mentioning Crane, hemp DNA, currency security
**Corpus source:** berkshirebuds entry 8, simian420_main

## 🔴 BBUDS-01 — Berkshire Buds Federal Civil Rights Case
**Status:** ACTIVE — HIGH PRIORITY
**Location:** /home/mrpat/projects/BBUDS-01/
**Master doc:** BBUDS-01_Master_Document_v3.docx
**Evidence:** 127 police/DA files + 5 medical docs, all SHA-256 hashed
**Core claim:** §1983 Federal Civil Rights — FLIR perjury, Grand Jury fraud, 4th/14th Amendment
**Lead claim:** Unwarranted MacBook search — exam June 21, warrant scanned Aug 2 (42 days later), date field blank
**Medical auth:** CannaMed recommendations confirmed — subject + 2 caregiver patients. Non-rooted plant language explicitly authorized in physician's recommendation.
**Facts:** Licensed MA medical cannabis operation, 374 Maple St Hinsdale MA 01235. Raided despite compliance. Case dismissed 2015-16. Equipment damaged/missing, ~120 seedlings destroyed, house lost, $30K setup, heroin relapse 5-7 years as direct consequence.
**Target:** $2M-$6M+
**SOL:** Standard 3yr window closed ~2018-19. Tolling doctrines: fraudulent concealment (FLIR perjury — clock starts at discovery, not raid), equitable tolling (relapse/Peru as direct consequences), continuing violation, discovery rule. FLIR expertise = credible basis to argue when perjury was identified.
**Target attorney:** Loevy + Loevy | Co-counsel: Prince Lobel Tye
**Resources:** Veterans Legal Services 857-317-4474
**Related tracks:** DETENTION-01, CHILDSUPPORT-01, BIOMARK-01 (Crane/hemp DNA connection)
**Gaps:** SJC dismissal date | psychiatric commitment dates
**Corpus source:** berkshirebuds entries 1-30, Oct 9-10 2025
---

### 🔵 SENTINEL-01 — Pacific Sentinel Analytics
- **Status:** IN WORK — concept phase
- **Goal:** Maritime intelligence firm with three divisions: Lost Dog SAR (search and rescue consulting), Sentinel Crisis Portal / LEDAA (crisis response platform), Andean Vantage (Peru export goods)
- **Working dir:** /home/mrpat/projects/SENTINEL-01/
- **Notes:** Umbrella org. AV-01 and SAR-01 are standalone sub-projects.

---

### 🟡 AV-01 — Andean Vantage
- **Status:** OPEN — concept confirmed
- **Goal:** Peru-to-global export business. Alpaca textiles, ceremonial-grade cacao, artisan products. Wife G-Girl's local supplier network is core asset.
- **Working dir:** /home/mrpat/projects/AV-01/
- **Notes:** Formerly SolTerra Goods. Most immediately actionable revenue project.

---

### 🟡 SAR-01 — SAR Methodology (Eielson Personnel Recovery)
- **Status:** OPEN — concept confirmed
- **Goal:** Package Eielson AFB sub-arctic Personnel Recovery / SAR operational methodology as consulting product for Peruvian emergency services. Predictive modeling + AI layer.
- **Working dir:** /home/mrpat/projects/SAR-01/
- **Notes:** Feeds Lost Dog division of SENTINEL-01.

---

### 🟡 EDU-01 — Neurodivergent First Principles Curriculum
- **Status:** OPEN — concept confirmed
- **Goal:** AI-assisted first-principles learning curriculum for neurodivergent kids. Based on Shaun's own dyslexia/ADHD learning methodology. Targets Peruvian schools.
- **Working dir:** /home/mrpat/projects/EDU-01/
- **Notes:** Connected to RUINS-01 and CINCO-01.

---

### 🟡 OAX-PUB — Radio OAX Telecom History Publication
- **Status:** OPEN — research complete, publication pending
- **Goal:** Publish historical research on Radio OAX origin story — Casa de Correos y Telégrafos, Marconi correspondence, Pasaje Piura architecture.
- **Working dir:** /home/mrpat/projects/OAX-PUB/
- **Notes:** Builds credibility for OAX-01 commercial track. Field research confirmed at Central Lima.

---

### 🟡 CRYPTO-01 — Blockchain Application Layer
- **Status:** OPEN — concept confirmed
- **Goal:** Blockchain application layer built over ARCH-01 (80x80Q distributed node architecture).
- **Working dir:** /home/mrpat/projects/CRYPTO-01/
- **Notes:** Dependency: ARCH-01 must be sufficiently developed first.

---

### 🔵 CINCO-01 — Five AI Babies (MINEDU Agent Network)
- **Status:** IN WORK — concept confirmed, build pending
- **Goal:** Five AI agents deployed to Peruvian schools to learn curriculum. Originated from MINEDU 9,999-school database found at Plaza Mayor Lima.
- **Working dir:** /home/mrpat/projects/CINCO-01/
- **Notes:** Google Meet internal request angle confirmed in corpus. Connected to EDU-01.

---

### 🟡 RUINS-01 — Children as Digital Forensic Analysts
- **Status:** OPEN — concept confirmed
- **Goal:** Program using CONIDA satellite imagery to train children as digital forensic analysts. Discovery-based learning via real geospatial data.
- **Working dir:** /home/mrpat/projects/RUINS-01/
- **Notes:** Connected to EDU-01.

---

### 🔵 PERU-INTEL-01 — Lima Operational History 2014–2019
- **Status:** IN WORK — extraction ongoing
- **Goal:** Document Shaun's Lima operational period: Surfire/Cerfire avionics items found in Central Lima office, Trump Summit April 2018 Rustibar incident, PPK resignation March 21 2018 simultaneous device-pull observation, CIA seal item from Ministerio de Justicia rep.
- **Working dir:** /home/mrpat/projects/PERU-INTEL-01/
- **Notes:** Cross-ref KELLY-THEORY-01 Sections 22–23. Corpus source: simian420_main, simiandox.

---

### 🔴 GUARDIAN-01 — Federal Civil Rights (BBUDS Parallel Track)
- **Status:** ACTIVE — documentation phase
- **Goal:** Civil rights case stemming from June 21 2013 raid. FLIR perjury as core 4th Amendment claim. Shaun is certified FLIR specialist with video evidence proving testimony false.
- **Working dir:** /home/mrpat/projects/GUARDIAN-01/
- **Primary source:** "The Central Protocols" document — simian420_main entry 321, Jan 25 2026
- **Target valuation:** $2M–$6M+
- **Notes:** Case dismissed 2015–16. SOL tolling via fraudulent concealment. See also BBUDS-01.

---

### 🔵 EMPLOY-01 — Remote Employment and Freelance Development
- **Status:** ACTIVE
- **Goal:** Secure remote contract/freelance US employment. Target domains: OSINT research, AI pipeline engineering, legal tech support.
- **Working dir:** /home/mrpat/projects/EMPLOY-01/
- **Target platforms:** Upwork, Contra, Toptal, direct law firm outreach
- **Notes:** US citizen, legally eligible for US remote work from Peru. SCRIPTS-01 sub-track: existing pipelines as portfolio pieces.

---

### ⚪ ARCH-01 — 80x80Q Distributed Node Architecture
- **Status:** FUTURE — concept only
- **Goal:** 80x80Q distributed node architecture. Foundational layer for CRYPTO-01.
- **Working dir:** /home/mrpat/projects/ARCH-01/
- **Notes:** SHAMROCK-01 intellectual lineage feeds this. CAC state integer theory is the origin concept.


### 🔴 FED-01 -- Federal Criminal Investigation (Title 18 / Title 31)
Keywords: title 18, title 31, federal, criminal, BSA, bank secrecy, money laundering, sworn, investigation, oath

### 🔴 NUC-01 -- Nuclear Security / Strategic Arms
Keywords: nuclear, strategic arms, SALT, START, warhead, deterrence, ICBM, nuclear security, fissile, proliferation

### 🔴 KELLY-LEGAL-01 — Personal Legal Track
**Status:** ACTIVE
**Description:** Passport denial due to child support arrearage (~$100k, predominantly penalties). Massachusetts DOR opposing agency. 100% P&T disabled veteran on fixed VA+SSI income. Currently coordinating from Lima Peru (exile). Pro bono target: Veterans Legal Services Boston.
**Keywords:** passport denied, child support, arrearage, massachusetts dor, veterans legal, kelly legal, pro bono, 100k debt, disability income
**Aliases:** legal track, passport case, child support case

### 🟡 BIOMARK-01 — Hemp DNA Authentication Concept
**Status:** ACTIVE
**Description:** DNA encoding in paper-based substrates for secure government documents. Geographic supply chain: Hinsdale MA (hemp cultivation) → Lee MA (Kimberly-Clark mill) → Dalton MA (Crane & Co. currency paper). Real opportunity: international security printing market via Giesecke+Devrient Green LongLife protocols. NOT US currency (cotton/linen blend). Concept was active at time of 2013 raid. Shares origin event with BBUDS-01.
**Keywords:** hemp, biomark, crane and co, giesecke, green longlife, dna currency, paper substrate, security printing, passport paper, industrial hemp, hinsdale hemp, dalton crane
**Aliases:** hemp project, dna paper, biomark

### 🟡 DARPA-01 — DARPA Concept Development Track
**Status:** ACTIVE
**Description:** DARPA job applications (rejected), RamOS program tracking, 3-layer obscuring protocol, city of the future / Media Overflow Cities concept, carbon fiber nanotube structural reinforcement drone concept, door-to-door drone logistics concept.
**Keywords:** darpa, ramos, media overflow, city of the future, carbon fiber nanotube, door to door drone, drone delivery, autonomous drone, broad agency, iarpa, skunk works, darpa challenge
**Aliases:** darpa track, drone concepts, ramos program

### 🟢 BBUDS-01 — Berkshire Buds Civil Rights Case
**Status:** ACTIVE — replaces GUARDIAN-01 (retired June 20 2026)
**Description:** 2013 Massachusetts State Police raid on Shaun's property. Raid hit both Berkshire Buds AND the hemp/DNA currency concept simultaneously. 42 U.S.C. 1983 federal civil rights lawsuit — malicious prosecution. FLIR thermal imaging evidence — police perjury claim. Fourth Amendment violations (Kyllo v. United States). Criminal case dismissed 2015-2016. Loss of parental rights, home, business. Coordinating from Lima Peru (exile).
**Keywords:** berkshire buds, 2013 raid, flir, fourth amendment, kyllo, malicious prosecution, mass state police, civil rights, 1983 lawsuit, bbuds, permit denial hinsdale, cpcs records
**Aliases:** berkshire buds, bbuds, guardian (retired label)

### ⚪ GEM-01 — Personal Archive Intelligence Recovery Pipeline
**Status:** ACTIVE
**Description:** The pipeline itself. Ingests, classifies, and routes Gemini AI conversation history into project buckets. Commercial product: PAIR Pipeline. Local-first, privacy-preserving, human-in-the-loop architecture.
**Keywords:** gem-01, pair pipeline, gem01, pipeline work, narrative generation, ck-c review, routing decisions, vtt correction, ollama, qwen, ingest
**Aliases:** pair pipeline, gem pipeline

### 🟡 VENTURE-01 — PAIR Pipeline Patent and Commercialization
**Status:** ACTIVE — provisional patent ready for USPTO filing July 1 2026
**Description:** Commercial productization of GEM-01 as PAIR Pipeline (Personal Archive Intelligence Recovery). Provisional patent specification complete. USPTO micro-entity fee $320. Filing target: July 1 2026.
**Keywords:** venture-01, pair pipeline patent, uspto, provisional patent, micro-entity, patent pending, commercialization, pair pipeline commercial
**Aliases:** pair commercial, patent track

### 🟡 DEAD-01 — Death Documentation and Grateful Dead Research
**Status:** ACTIVE
**Description:** Documentation of known deceased persons (Tina Packer, Renee Goode news tracking). Grateful Dead / Jerry Garcia personal interest and research. Gathering of the Vibes (GOTV) documentation.
**Keywords:** jerry garcia, grateful dead, dead shows, garcia, deadhead, tina packer, renee goode, gathering of the vibes, gotv, dead concert, bob weir, phil lesh, steal your face
**Aliases:** grateful dead, dead research, garcia

---
## RETIRED PROJECTS

### ❌ GUARDIAN-01 — RETIRED June 20 2026
**Reason:** Gemini-introduced label. All content absorbed into BBUDS-01.
**Redirect:** See BBUDS-01


### REGISTRY NOTE — 2026-06-21
OAX-01 (commercial track) formally merged into ORPHAN-01.
OAX-PUB (publication track) remains independent — feeds ORPHAN-01 credibility.
Relationship: OAX-PUB research -> ORPHAN-01 commercial exploitation -> In-Q-Tel pipeline.

### ORPHAN-01 / OAX-PUB SITE CONFIRMATION — 2026-06-21
PHYSICAL ANCHOR: Lima Peru transmission site — confirmed unbroken lineage:
  Tesla Tower (original era) ->
  Radio OAX public broadcast tower (historical) ->
  AT&T telephonics broadcast tower (current)
Same physical location. Operator has photographic documentation of current tower.
This site connects: Paris Convention disclosure era -> OAX broadcast history ->
Casa de Correos archive -> current AT&T infrastructure.
Cross-reference: PERU-INTEL-01 infrastructure mapping (machine-buildings,
utility nodes, Telefonica as data hub).
Photo evidence: in operator possession. Flag for ORPHAN-01 evidentiary record.

### ORPHAN-01 / OAX-PUB GEOSPATIAL ANCHOR — CONFIRMED 2026-06-21
PRIMARY ADDRESS: Jirón Washington, Cercado de Lima (OAX original HQ)
TRANSMITTER SITE: San Miguel quarters, Lima (two towers, 10KW, English-built)
CHAIN OF TITLE:
  1921: Peruvian govt contracts Marconi Wireless Telegraph Co (25yr concession)
  1924: Peruvian Broadcasting Company acquires Marconi rights, founds OAX
  1925-06-20: OAX inaugurated by President Leguia, Plaza San Martin broadcast
  1926: State takeover -> Compania Nacional de Radiodifusion
  1933: Renamed Radio Nacional del Peru
  1937-01-30: Marconi rep launches OAX 4-A official station
  Current: AT&T/Telefonica tower on same site — operator has photographic documentation
MARCONI CONNECTION: Confirmed in chain of title. Not incidental.
SOURCE: El Comercio historical archive, Wikipedia Radio Nacional del Peru,
        concortv.gob.pe

### CRITICAL CROSS-REFERENCE — 2026-06-21
JIRÓN WASHINGTON CONVERGENCE:
OAX original HQ = Jirón Washington, Cercado de Lima (confirmed 1925)
PERU-INTEL-01 corpus entry = "1371 Jr. Washington" flagged as
  Machine-Building node in Shadow's infrastructure pre-mapping.
Same street. Same central Lima corridor.
The transmission infrastructure lineage (Tesla -> OAX -> AT&T/Telefonica)
and the PERU-INTEL-01 operational infrastructure mapping
both converge on Jirón Washington.
This is not coincidental. Flag for cross-project analysis:
ORPHAN-01 + PERU-INTEL-01 + OAX-PUB three-way convergence point.

### 🔴 INCA-01 -- Inca Cloth / Peruvian Artisan E-Commerce Venture

**Status:** NEW — registered 2026-06-21
**Origin:** Phase Two profiler — 183 new ventures flagged, Inca Cloth confirmed real

**Core Concept:**
E-commerce venture selling authentic Peruvian goods — clothing, blankets,
alpaca cloth, artisan textiles. Ethical sourcing model with community support
and charity components. Family business angle with personal Peru connection.

**What was developed in corpus:**
- Three logo concepts rendered (Artisan's Mark — rustic circular stamp,
  stylized alpaca with patterned border)
- Supplier research begun — "Coopain Cabana" as first supplier entry
- Ethical sourcing framework developed
- Community support and transparency model
- Artisan storytelling component for marketing

**Key corpus entries:**
- simian420 #1074 — logo concepts, Inca Cloth brand naming
- simiandox #396  — family business / artisan connection framing
- simiandox #445  — supplier spreadsheet, Coopain Cabana
- simiandox #462  — ethical sourcing plan
- simiandox #464  — community support / charity angle

**Connects to:**
- EMPLOY-01 (income generation track)
- PERU-INTEL-01 (Lima operational context)
- HELICON-01 (family business thread)

### ARCH-01 CANON NOTE — 2026-06-21
simian420 entry #23 (2026-01-27) contains full 80x80Q technical specification:
Smart Card nodes, 6400 points, non-volatile state retention, massively parallel
hybrid, self-repair/reroute on node failure, superposition values.
EARLIEST DATED TECH SPEC FOUND IN CORPUS. Flag for USPTO provisional filing.

### 🔴 MARITIME-01 -- Maritime Surveillance & Ocean Monitoring Venture

**Status:** NEW — registered 2026-06-21
**Origin:** Phase Two profiler high-signal filter, cross-account confirmed

**Core Concept:**
Two connected tracks confirmed real:
1. MARITIME SURVEILLANCE BUSINESS — technical prototype first approach,
   build the engine before the business framework. Demonstrable asset strategy.
2. OCEAN MONITORING AI PLATFORM — AI-powered data fusion and anomaly detection
   for ocean monitoring. Advanced home-security-style system but for the ocean.

**Cross-account confirmation:**
- simiandox #293 + opfor4us #293 — same maritime surveillance pivot (both accounts)
- simiandox #339 + opfor4us #339 — same ocean monitoring platform (both accounts)
- simiandox #333 + opfor4us #333 — financial modeling for maritime startup
Cross-account = recurring real project, not one-off session.

**Key corpus entries:**
- simiandox #293 / opfor4us #293 — strategic pivot, technical prototype first
- simiandox #339 / opfor4us #339 — AI data fusion, anomaly detection, ocean
- simiandox #333 / opfor4us #333 — lean financial plan, first year operations

**Connects to:**
- PERU-INTEL-01 (Lima coastal/operational context)
- DARPA-01 (defense surveillance technology angle)
- EMPLOY-01 (income generation track)

### ORPHAN-01 OPERATOR CONFIRMATION — 2026-06-22
Operator explicitly confirmed ORPHAN-01 as a real named venture.
Stage 5 narrative inflation flags reviewed and overridden by operator authority.
The venture is real. The framing is operator-confirmed canon.

### 🟢 INCIDENTAL-01 — General Incidental Queries
Generic one-off tech-support, trivia, unit conversion, or lookup questions
with no connection to any active project. Not personal/biographical
(that would be a different tag) — purely incidental, no throughline.
Added 2026-07-04 by Mr_Pat to replace UNKNOWN as the default bucket for
this category of content.

### 🟢 PERSONAL-01 — Personal History / Biographical
Personal life history, long-standing subscriptions, hobbies, family, or
biographical detail with no connection to any active project — distinct
from INCIDENTAL-01 (generic tech-support/trivia lookups with no personal
throughline). Added 2026-07-04 by Mr_Pat.

### 🟢 AI-RESEARCH-01 — AI Development & Research Interest
Ongoing interest in AI development, AI research contribution methods,
AI tooling/integration (e.g. Chrome AI extensions, contributing to open
source AI projects) — distinct from GEM-01 (the pipeline itself) and
INCIDENTAL-01 (no throughline). Added 2026-07-04 by Mr_Pat.

### 🔴 AV-01 — RETIRED 2026-07-04
Consolidated into INCA-01 (Peru business/venture umbrella) per Mr_Pat
2026-07-04. Do not use AV-01 going forward — route to INCA-01 instead.

## GEMINI-PERSONALITY-01 — Gemini Personality Builder
Status:    Active — research/decision-support phase
Started:   2026-07-09
Location:  ~/projects/gemini_personality_builder/
Purpose:   System for defining, storing, and dispatching reusable Gemini
           personas (Gems and/or API-side system_instruction configs).
Open item: Build direction not yet chosen (4 candidates under review).

**Y-TIP-01** — YouTube Trend Intelligence Pipeline. Multi-topic, channel-scoped and
keyword-scoped YouTube content monitoring. Topics: `uap` (institutional/disclosure-
focused UAP content, keyword-search-based) and `agentic_ai_infra` (27 verified
channels, channel-scoped, no keyword search). Built on LangGraph derivation graph,
FastMCP local tool server (hash verification), PostgresSaver checkpointer pattern.
Standalone — no dependency on other active projects.
# sanity check Thu Jul  9 06:46:20 PM -05 2026

## uap_kids_channel
- Created: 2026-07-10
- Status: Setup
- Summary: AI-generated animated UAP/UFO stories for children, separate
  Google account, Made for Kids designation.
- Brief: /home/mrpat/projects/uap_kids_channel/PROJECT_BRIEF.md

## kids_media_research
- Created: 2026-07-10
- Status: Not started
- Summary: Market/format research on children's programming, feeds
  uap_kids_channel.
- Brief: /home/mrpat/projects/kids_media_research/PROJECT_BRIEF.md

### 🔵 GOOGLE-DEV-01 — Google Behavioral Takeout
- **Status:** ACTIVE (added to .md 2026-07-10; existed in JSON since v3)
- **Goal:** Full Google behavioral Takeout beyond Gemini — My Activity, Chrome, Android, Play, Drive, Developer data.
- **Notes:** Behavioral metadata layer, distinct from Gemini conversation corpus.
---
### 🔵 HELICON-01 — The Helicon Project
- **Status:** ACTIVE (added to .md 2026-07-10; existed in JSON since v3)
- **Goal:** Family-led social enterprise — cancer research (Jonathan Kelly) + water business (Chris Hodgkins). Shaun = General Partner/Integrator.
- **Notes:** Surfaced CK-C 2026-06.
---

### REGISTRY RECONCILIATION — 2026-07-10
JSON registry patched v3 -> v4 (28 -> 45 entries). Added 17 tags that existed
only in this .md or were untracked: DETENTION-01, CHILDSUPPORT-01, FED-01,
NUC-01, DARPA-01, VENTURE-01, GEM-01, INCA-01, MARITIME-01, ORPHAN-01,
INCIDENTAL-01, PERSONAL-01, AI-RESEARCH-01, GEMINI-PERSONALITY-01, Y-TIP-01,
UAP-KIDS-01 (new tag for uap_kids_channel), KIDS-MEDIA-01 (new tag for
kids_media_research). AV-01 marked retired in JSON (route to INCA-01).
Classifier bug fixed same day: load_tags() never parsed the JSON (dict/list
mismatch, silent fallback to hardcoded stale list) and tag list was truncated
to 30. All classification batches before 2026-07-10 ran on the stale
hardcoded list — treat unreviewed batch tags as provisional.
Stale duplicate entries in this .md (old BBUDS-01 with dollar targets, old
GUARDIAN-01 ACTIVE, first BIOMARK-01) are superseded — JSON versions canonical.

## AGIMUS-01
- Status: active
- Active from: 2026-07-10
- Description: Gemini engagement-plausibility audit. Tests operator hypothesis that Gemini's depth of engagement tracks a concept's theoretical plausibility versus sycophantic coherence-following. Pipeline: extraction (origin patkelly74 s460) -> atomic claim decomposition (local Ollama, temp 0.0) -> blind panel grading (DeepSeek + GLM + third leg, Gemini excluded from primary) -> verdict matrix -> reusable audit methodology feeding GEM-01 inflation discipline.
- Keywords: agimus, m5-01, claim decomposition, blind panel, capability claim, inflation audit, verdict matrix, creed_session_460
- Disambiguation: Companion M5-01 = three-model code trial sub-protocol, not a separate registry tag.

## AFTERGLOW-01
- Status: active
- Description: Technical configuration and troubleshooting support for
  personal-use local LLM models (Ollama, `personal/` namespace). Model
  selection, VRAM/quantization sizing, parameter tuning, Modelfile
  mechanics, coherence troubleshooting. Does not generate or edit
  character/content text.
- Keywords: ollama, local llm, personal models, modelfile, vram, quantization


<!-- added 20260711T165737Z via registry_patch_drift.py -->
## DRIFT-01
- Status: active
- Active from: 2026-07-11
- Description: Instruction-following drift investigation. Why current-gen models overtrigger/drift under heavy instruction sets. Two-source finding: instruction-weight (leaning fixes) vs model/wording (leaning does not). Feeds INSTSET-BUILDER template retune.
- Keywords: drift, instruction-following, overtrigger, two-source, lean instruction set, AGIMUS transcript, INSTSET-BUILDER
## CTXMGR-01
- Status: active
- Active from: 2026-07-11
- Description: Local-LLM-as-context-manager architecture. Local model holds full conversation state and hands each remote model a compact clean packet per turn, so the remote never sees raw growing history. Foundation spec + API adapter verification complete.
- Keywords: context manager, local llm, state object, packet assembly, model adapter, hierarchical context
- Disambiguation: Architecture work predates formal registration; exact active_from unconfirmed, set to registration date.
## COGN-01
- Status: active
- Active from: 2026-07-11
- Description: Context/texture-degradation research. Qualitative context degradation (texture and nuance loss) as distinct from factual drift. Spun off from DRIFT-01.
- Keywords: cognition, texture loss, context degradation, nuance

## MEMORY-ALPHA-01
- Type: AI infrastructure / knowledge management
- Status: Scaffolded 2026-07-11
- Path: /home/mrpat/projects/MEMORY-ALPHA-01/
- Purpose: Self-documenting knowledge base — raw ingest → AI synthesis → structured wiki
- Structure: raw/ wiki/ archive/ prompts/ projects/
- Core prompts: translate.md (raw-to-wiki), weekly.md (weekly digest)

## HOUSEKEEP-DISPO-01
- **Status:** active
- **Description:** Disposition layer for housekeeping audit findings (v4.7 protocol) pasted from other working projects. Checks two documented failure patterns (false-completion claims, unpersisted "Logged" items) plus incomplete/ambiguous input, then produces one tagged disposition markdown per batch (Closed / Node-Dependent / Operator-Decision / Tracked-Low-Priority). Chat-only — no direct cross-Project access. Currently mid one-time portfolio sweep governed by TEMP_ORPHAN_RUN_CONSOLIDATION_PATCH.md, which retires once every working project is triaged to v4.7. Permanent reference: HOUSEKEEPING_PROTOCOL_v4_7_FINAL.md.
- **Keywords:** housekeeping, disposition, audit, v4.7, portfolio-sweep, false-completion, orphan-run
- **Registered:** 2026-07-14
- 2026-07-14: PROJ_054 / HOUSEKEEP-FORK-01 registered -- fork of HOUSEKEEP-DISPO-01, generalizing verification methodology, applied to backdoor-detection project + self-application. Phase 1 grounded source-verification script built, pending first run.
- 2026-07-15: PROJ_054 / HOUSEKEEP-FORK-01 — Phase 1 COMPLETE (16 sources verified by 5-model panel; 1 contested — Source 8 "Trust, but Don't Verify" arXiv 2606.05403, GPT could not confirm ID; 1 LIKELY — Source 11 Snyk stats conflict). Phase 2 COMPLETE and CONSOLIDATED (~40 model gaps deduplicated into 15 themes, 6 with full 5-model consensus) — see `~/projects/HOUSEKEEP-FORK-01/working/phase2_gap_analysis_CONSOLIDATED_20260715.md`, folded into `BACKDOOR-SCAN-01/OPEN_ITEMS_TRACKER.md`. Panel-composition correction: de facto Phase 2 panel as executed was {claude-opus-4.8, deepseek-v4-pro, gpt-5.6-sol, glm-5.2, grok-4.5} (n=5; hy3→grok after Phase 1 empty-content failure) — supersedes BACKDOOR-SCAN-01 INSTSET rule 4 "GLM dropped" framing for this fork's verification panel; BFT recomputed against n=5 (f=1, quorum floor 4). Source 8 contested-verification RESOLVED 2026-07-15: direct arXiv fetch confirms 2606.05403 exists (title/authors/date match; GPT's miss was transient), API returned v2 — version-mismatch on the model-count stat remains (pin version before quoting). Source 11 Snyk stats-conflict RESOLVED 2026-07-15: primary sources (arXiv 2605.28588 abstract + Snyk blog HTML) show no genuine conflict — three-population conflation (3,984 scanned; 534/13.4% critical; 1,467/36.82% any-flaw; 76 confirmed malicious; 91%-of-76 combined PI+malware; 100%-of-76 malicious code) originating in the blog's imprecise headline; Source 11 upgraded LIKELY → VERIFIED.

## BACKDOOR-SCAN-01

**Status:** Active — Layer 3 design validated against real code; research foundation verified and gap-analyzed via HOUSEKEEP-FORK-01 (Phase 1 source verification complete, Phase 2 design-gap analysis complete and consolidated 2026-07-15); Layer 2 not yet built; code fixes not yet applied.

**One-line description:** Multi-layer, multi-model system for detecting AI-introduced backdoors, vulnerabilities, and malicious code across Mr_Pat's AI-assisted, non-coder-directed software portfolio.

**Directory:** `/home/mrpat/projects/BACKDOOR-SCAN-01/` (create if not present; working files currently at `/home/mrpat/backdoor_concept_working/` — migrate into project structure)

**Architecture:**
- Layer 1 (deterministic tools) — BUILT, TESTED. gitleaks, bandit, semgrep, pip-audit, cargo-audit. Script: `~/layer1_scan.sh`.
- Layer 2 (capability manifest diff + secret-to-sink taint trace) — DESIGNED ONLY, not built as working code.
- Layer 3 (3-pass adversarial LLM review: malicious-hypothesis / benign-skeptic / adjudication) — BUILT, TESTED, VALIDATED against real code (y-tip-pipeline api.py). Script: `~/layer3_dry_test_panel.py`.

**Model panel (for Layer 3):** Claude (anthropic/claude-opus-4.1), GPT (openai/gpt-5.5), Qwen (qwen/qwen3-coder-plus), Sakana (sakana/fugu-ultra) — all via OpenRouter; DeepSeek (deepseek-chat) via direct API (DEEPSEEK_API_KEY in ~/.env), not OpenRouter. GLM (z-ai/glm-5.2) DROPPED after 3/3 empty-content failures across 3 separate test runs despite retry logic and 6000-token ceiling.

**Test subject to date:** y-tip-pipeline (FastAPI + Celery + PostgreSQL/psycopg2), specifically `api.py`. No other project in the portfolio has been tested yet.

**Key reference:** ESAA-Security (arXiv:2603.06365, github.com/elzobrito/ESAA-Security) — an event-sourced, replay-verifiable architecture for agent-assisted security audits. Noted as a relevant formalization of this project's informal persistence-gate/evidence-tiering discipline. Verified as a real source (Phase 1) and used as foundation material in the Phase 2 gap analysis — the specific 5-step ESAA comparison method from OPEN_ITEMS_TRACKER item 6 has not yet been run as its own deliverable.

**Research foundation (HOUSEKEEP-FORK-01):** 16 sources verified by a 5-model panel (Phase 1) — see `~/projects/HOUSEKEEP-FORK-01/working/phase1_verdicts_only.md`. Design gap analysis (Phase 2) consolidated into 15 themes, 6 with full 5-model consensus — see `~/projects/HOUSEKEEP-FORK-01/working/phase2_gap_analysis_CONSOLIDATED_20260715.md`. Source 8 ("Trust, but Don't Verify," arXiv 2606.05403) — the contested Phase 1 verification is RESOLVED 2026-07-15: direct arXiv fetch confirms the ID exists (title/authors/date match the Phase 1 majority; GPT's "could not confirm" was a transient search miss). It underpins the highest-priority gap and is safe to rely on. Residual: arXiv API returned **v2**; the model-count statistic differs by version (v1=5 models/3 families vs v2=6 models/4 families) — pin the version before quoting that number.

**See also:** Full history and rationale in `project_full_writeup-3.md` and consolidated code findings in `ytip_layer3_findings_consolidated.md`, both within this project's directory.
