# TRACE4QR WP2 — 5-Agent Pipeline
# System Prompt Split Guide v0.9 / rev3
# Source: TRACE4QR-WP2-DATASET-LABELING-v0.1 + Agent_Prompt_v0.7

---

## Pipeline Flow

```
[Repo URL]
    ↓
Agent1_Repository_Scanner.md          v0.9
  Phases: 0, 0b, 1, 2, 3
  Output: repository_intake_record, snapshot_record (full SHA),
          structural_scan (+ crypto_grep_hits), crypto_discovery_summary
    ↓
Agent2_Task_Evidence_Builder.md       v0.8
  Phases: 4, 5, 6  +  MD §8 Stage 6 follow-up loop
  Output: analysis_tasks[], evidence_records[], context_bundles[],
          negative_candidate_sweep, task_generation_summary
    ↓  (follow-up loop: Agent 3 → Agent 2 → Agent 3)
Agent3_Analysis_Labeling.md           v0.8
  Phases: 7, 7b, 8, 9, 10
  Output: human_analysis_records[], adjudication_records[] (placeholders),
          follow_up_requests[], planner_feedback[], batch_statistics
    ↓
Agent3_5_LLM_Adjudicator.md           v0.8  ← quality gate
  Phase: 7b (automated adjudication)
  Output: adjudication_records[] (populated), adjudication_summary,
          pipeline_ready flag
    ↓
Agent4_Output_Assessment.md           v0.8
  Phases: 11, 12, 13, 13b  +  MD §15.1 training examples
  Output: golden_dataset_candidates[], pqc_assessment,
          cbom (CycloneDX 1.6 — exact schema), training_examples[],
          Final WP2 JSON artifact
```

---

## Files

| File | Agent | Version | Key responsibility |
|---|---|---|---|
| `Agent1_Repository_Scanner.md` | Repo Scanner | v0.9 | Acquire, grep sweep, full-SHA pin |
| `Agent2_Task_Evidence_Builder.md` | Task & Evidence Builder | v0.8 | Tasks, evidence, context bundles, full method body rule |
| `Agent3_Analysis_Labeling.md` | Analysis & Labeling | v0.8 | HAR labels, uncertainties, follow_up_suggestions, trajectory |
| `Agent3_5_LLM_Adjudicator.md` | LLM Adjudicator | v0.8 | 6-check quality gate, pipeline_ready flag |
| `Agent4_Output_Assessment.md` | Output & Assessment | v0.8 | CBOM (CycloneDX 1.6), golden set, WP3 training examples |

---

## Global rules — present in every agent

- **INFERENCE ≠ VERIFIED EVIDENCE** — evidence elevation prohibition
- **Evidence quality classification** — 9 `evidence_quality` values
- **Outcome label rules** — 5 canonical `outcome` values
- **Confidence scoring** — `high / medium / low / unknown`
- **Label schema** — all `labels` sub-fields with allowed values
- **Not-crypto quota** — ≥30% of HARs must be `outcome: "not_crypto"`

---

## CBOM — CycloneDX 1.6

The CBOM schema is fully defined in `Agent4_Output_Assessment.md` Phase 13b.
Four component types with complete field definitions:

| assetType | Use for |
|---|---|
| `algorithm` | Named algorithms: AES, RSA, SHA-256, PBKDF2, etc. |
| `protocol` | TLS, SSH, JWT signing, IPsec, etc. |
| `related-crypto-material` | Keys, certificates, keystores, IVs, nonces, passwords |
| `library` | BouncyCastle, OpenSSL, libsodium, JCA provider, etc. |

**Only `crypto_finding` records with `confidence: "high"` or `"medium"` are promoted.**
All unverified fields (key size, algorithm version, mode) must be `null` — never inferred.

---

## Changelog rev1 → rev2 → rev3

| # | Fix | Agent |
|---|---|---|
| K1 | Seed repo list (MD §5) added | A1 |
| K2 | `cryptographic_operation` single-value constraint enforced | A3 |
| K3 | MD §15.1 `training_examples[]` structure added | A4 |
| K4 | MD §8 Stage 6 follow-up loop defined | A2 + A3 |
| K5 | `crypto_discovery_summary` noted as optional addition | A1 |
| K6 | `task_generation_summary` noted as optional side-channel | A2 |
| K7 | MD §18 future automation mapping added | A4 |
| K8 | Full 40-char SHA — 3-method acquisition (local git, API, Atom feed) | A1 |
| K9 | Mandatory clone-level grep sweep + `crypto_grep_hits` field | A1 |
| K10 | Clone ALL submodules rule made explicit | A1 |
| K11 | Mandatory full method body rule (AES/cipher tasks) | A2 |
| K12 | `uncertainties` mandatory rule added | A3 |
| K13 | `follow_up_suggestions` mandatory rule added | A3 |
| K14 | Agent 3.5 LLM Adjudicator created (new agent) | A3.5 |
| K15 | CycloneDX 1.6 schema fully defined — 4 component types, complete fields | A4 |
| K16 | All prompts translated to English | All |
