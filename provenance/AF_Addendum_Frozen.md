# C01 — AF-family Fixed-Coordinate Exploratory Addendum

## Minimum Protocol v1.0 FINAL

**Frozen date:** 2026-11-01  
**Status:** FINAL — protocol frozen; structural analysis NOT STARTED  
**Parent protocol:** C01 Minimum Protocol v1.0 FINAL (2026-10-31)  
**Parent protocol SHA256 (previously recorded):** `87ba6cb500bdf4fc67803bec8cf2f655443367431945c7f7df359a1bff0381fa`  
**Scope:** Independent exploratory supplement; does not amend or replace the parent C01 primary analysis.  
**Approval:** The user approved the v0.1 draft in full and explicitly approved inclusion of AF–Boltz DockQ, conditional Tier 2, and integration only after completion of the Addendum analyses. This v1.0 records those decisions without changing the scientific analysis definitions.

## 0. Mission

Compare **one already-published fixed AlphaFold-family MPC1L–MPC2 heterodimer prediction** and **one fixed Boltz-2 MPC1L–MPC2 prediction** with the *same four experimental reference structures*, using the frozen definitions and QC rules of C01 v1.0.

The purpose is reproducible **descriptive fixed-coordinate structural comparison**, not benchmarking general AF versus Boltz model performance. No new predictions are generated. Small, null, inconsistent, or literature-overlapping observations are reportable without attempting to rescue scientific novelty.

Explicit exclusions: general model ranking; state-selection probabilities or equilibrium populations; binding free energy or transport mechanism inference; statistical generalization from these non-independent models/references; post hoc choice of best AF/Boltz models or masks; modification of the parent C01 primary analysis.

## 1. Scientific questions and interpretation boundary

**RQ-A — Experimental reference sensitivity.** For the fixed AF structure, what are the fixed 73-residue interface Cα RMSDs against 9GIX, 9GIV, 9GIW, and 9GIY under precisely the same alignment as C01?

**RQ-B — Fixed-coordinate contrast.** How different are the fixed AF and Boltz coordinates under the 73/62/198-residue definitions, and how do their descriptive relationships to the four experimental structures compare?

**RQ-C — Local correspondence.** Can predeclared local residue geometry, helix geometry and interface-candidate screens describe, without assigning causation, areas of agreement or disagreement?

No directional hypothesis of AF or Boltz superiority is adopted. Equal reporting is required for agreement, disagreement, changes across reference structures, small differences, and conflict across metrics. The four experimental structures are related experimental conditions, **not independent statistical replicates**.

## 2. Fixed inputs and provenance

### 2.1 AF-family prediction

- Dataset: AlphaFold Protein Structure Database, NVIDIA complex predictions.
- Entry: `AF-0000000204012512`, entry version `v1`.
- Coordinate: `AF-0000000204012512-model_v1.cif` (original unmodified file).
- Associated PDB (if needed for tool conversion/checks): `AF-0000000204012512-model_v1.pdb`.
- PAE: `AF-0000000204012512-predicted_aligned_error_v1.json`.
- Software/model: AlphaFold-Multimer v2.3.0 weights; NVIDIA OpenFold-TRT/cuEq pathway.
- Entry creation date recorded: 2026-02-20.
- Chain A = MPC2, UniProt O95563, 127 residues; chain B = MPC1L, UniProt P0DKB6, 136 residues.
- Both chains have all 263 Cα atoms; PAE is 263×263 (previous Gate A inspection).

### 2.2 Frozen Boltz-2 prediction

- Source: Ille et al., Human PPI Atlas; atlas row recorded as 147.
- Coordinate: `O95563_P0DKB6_Boltz-2_v2-1-1.cif`.
- Model: Boltz-2 v2.1.1.
- GitHub repository: `structural-interactome/human-interactome`.
- Frozen repository commit: `dc55acabb3da7f233def7a0668d86e1c0ecb8e8e`.
- Coordinate SHA256 (previous C01 record): `3ef95557b603f6c32bcf2193158ff3bfe621f92c60013cdec7c15438c3f4fe64`.
- Chain A = MPC2 O95563; chain B = MPC1L P0DKB6.
- File's first GitHub addition: commit `7f903151242a9d813c263c53fbd3b82289e0df73`, 2025-06-29 17:41:41 UTC; **this is not a proven inference-generation timestamp**.

### 2.3 Four experimental references

| PDB | Condition | Reference state |
|---|---|---|
| 9GIX | Apo | Inward-open |
| 9GIV | C7 derivative | Outward-open |
| 9GIW | Zaprinast | Outward-open |
| 9GIY | Mitoglitazone | Outward-open |

Reuse **the exact original experimental CIF revisions already frozen in C01**, not newly fetched/revised replacements. Experimental chain IDs may differ from predicted chain IDs: map by protein identity, UniProt residue number, sequence and coordinates, never just a chain letter. Exclude experimentally present macrobody, ligands, lipids, detergent, water and other non-target components from target–target calculation exactly as in C01; retain their presence as interpretive context.

### 2.4 Input integrity and immutable records

Before calculations, create an `INPUT_MANIFEST` with complete SHA256 for the original AF ZIP/CIF/PDB/PAE, Boltz CIF, the four experimental CIFs, parent protocol and fixed masks; record paths, source URLs, revision/commit, retrieval details, code versions and execution environment. Verify existing recorded hashes rather than silently treating these document strings as freshly recomputed checksums. Keep originals unchanged, and relate every normalized/derived coordinate to its original.

If any original required input or frozen mask cannot be verified, **STOP primary execution** until provenance is resolved. No synthetic or inferred file should be presented as an original.

## 3. Frozen mask definitions and coordinate mapping

**No new interface mask is constructed.** Reuse the exact saved parent C01 masks and residue order:

| Mask | Definition | Count |
|---|---|---:|
| Primary | Union of <5 Å experimental interchain observed-heavy-atom contacts across all four references | 73 Cα |
| Sensitivity | Union of <4 Å experimental interchain observed-heavy-atom contacts | 62 Cα |
| Global | Common experimentally observed target-protein sequence | 198 Cα |

- Primary 73: MPC1L 37 residues + MPC2 36 residues.
- Sensitivity 62: MPC1L 30 + MPC2 32.
- Global 198: MPC1L UniProt 22–105 = 84; MPC2 UniProt 8–121 = 114.
- Earlier Gate A found AF-vs-experimental agreement for 198 residues × four references (792/792 residue identities).
- Recheck **all six** structures, including Boltz, using fixed lists before numerical comparisons.

Do not change masks, chain identity, fitting regions, residue selection, or coordinate-coverage rules based on observed AF results. If the saved mask lists disagree with the parent protocol or lack immutable evidence, stop until reconciled *without post hoc selection*.

## 4. Frozen roster: exactly five new comparisons

The original ten C01 comparisons (Boltz vs four experimental references plus six experiment–experiment pairs) are **not recalculated as a newly defined primary set**, changed, or replaced. Existing validated numbers may be used as historical controls, with traceable provenance.

| New ID | Pair | Role |
|---|---|---|
| AF-E01 | AF–9GIX | Fixed prediction–experimental reference |
| AF-E02 | AF–9GIV | Fixed prediction–experimental reference |
| AF-E03 | AF–9GIW | Fixed prediction–experimental reference |
| AF-E04 | AF–9GIY | Fixed prediction–experimental reference |
| AF-B01 | AF–Boltz | Fixed prediction–prediction contrast |

The AF–Boltz pair has **no experimentally validated 'native' side**. A consolidated matrix may show all 15 distinct pairs, provided the 10 parent and five Addendum pairs are labeled separately. Treat neither six structures nor four experimental states as independent samples for inference.

## 5. Primary geometry: identical C01 metric

**Primary endpoint:** `fixed_union5_interface_CA_RMSD_A`.

- 73 matched Cα positions in fixed order: MPC1L ascending UniProt numbering, followed by MPC2 ascending.
- Fit **both chains simultaneously** by proper rigid-body Kabsch rotation and translation, determinant `det(R)=+1`; no reflection, scaling, chain-wise independent fit or fitting-region selection.
- Evaluate RMSD on exactly the fitted 73 matched Cα atoms.
- Apply the same procedure to all five newly frozen pairs, including AF–Boltz.

**Required secondary/sensitivity geometry on each new pair:** fixed 62-residue two-chain Cα RMSD; fixed 198-residue two-chain Cα RMSD; MPC1L 84-residue chain-alone fit RMSD; MPC2 114-residue chain-alone fit RMSD; MPC1L-fit then evaluate the *unrefitted* MPC2 114-residue residual; MPC2-fit then evaluate the *unrefitted* MPC1L 84-residue residual. Distinguish fit set from evaluation set for every reported metric.

Save all five rows and associated residuals/transformations before interpreting. Record atom counts, complete residue crosswalk, proper-rotation check, coordinate hashes, transformation matrices and code version. Distances to reference states are descriptive, never evidence of true state occupancy or model-general accuracy.

## 6. Numerical QC and preflight

Apply **the mandatory QC in the parent C01 Minimum Protocol v1.0**, not a relaxed substitute. Include: complete chain–UniProt and Cα mapping; 73/62/198 coverage; consistent altloc handling; identical-input RMSD <1e-5 Å; rigid-transformation invariance; atom-order invariance; `det(R)=+1`; deliberate chain-swap and sequence-mismatch negative controls; cross-check one or more validated parent C01 pair results against the frozen code/inputs.

Any additional numeric tolerances, controls, or exception-handling details not restated here inherit the **parent protocol as authoritative**. Investigate discrepancies rather than changing historic results to match the AF calculation. Mandatory QC failure => stop reporting new Primary values; log the failure and evidence. Independent recomputation is distinct from simply rerunning or rereading the same code.

## 7. Local residue geometry — fixed, no post hoc additions

Predesignated cross-chain residue pairs (MPC2–MPC1L): W82–S35; W82–G31; I90–Q76; Y85–N79; K66–E51. For AF calculate and report Cα distance, shortest *observed heavy atom* distance and identities, <4 Å/<5 Å classification, missing atoms/altloc and QC; compare with frozen Boltz/experimental results.

E51–K66: distinguish generic heavy-atom proximity, backbone-to-sidechain proximity, and **carboxylate O–Lys NZ** salt-bridge geometry. Do not infer a salt bridge from generic minimum heavy-atom distance. Include available experimental local validation (Q-score, map inclusion, CIF B factors) from C01 Session 4 without treating AF pLDDT as the same scale as cryo-EM Q-score.

## 8. Helix geometry (same definitions as parent)

**H1 curvature proxy:** same HELANAL-like local-axis approach as C01; MPC1L residues 26–48, hinge 33; MPC2 residues 40–61, hinge 53. Reuse the fixed four-Cα local-axis, left/right averaging and angle definition, including endpoint numerical-sensitivity test. Strictly >5.0° change => `H1_NUMERIC_SENSITIVITY_GT5`. Preserve existing 9GIX MPC2 5.019° warning. Do not assert that this computational bend proxy is a validated physical hinge angle.

**Within-structure H2/H3 acute axis angle:** same segment PCA method and axis-sign conventions. MPC1L H2 54–75 / H3 79–105; MPC2 H2 68–89 / H3 93–121. Record coverage and eigenvalue anisotropy. Do **not** introduce inter-state rigid H2/H3 rotation; remain `NOT QUALIFIED / NOT RUN` under the parent C01 frame-qualification restriction. Do not claim reproduction of the original paper's reported rigid rotation values.

## 9. DockQ and FreeSASA

### DockQ — explicitly approved for all five pairs

Use the **same DockQ version, CLI, preprocessing and chain-mapping checks as parent C01 Session 2**. Record DockQ, Fnat, conventional interface RMSD, ligand RMSD, exact predicted/reference direction, command, versions, exit code, stdout/stderr, hashes, and mapping.

For AF–experimental comparisons, the corresponding experimental reference is native/reference. For **AF–Boltz**, *explicitly fix Boltz as the computational reference and AF as the model*; this is a **direction-dependent descriptive score, not experimental accuracy**. Never label the Boltz coordinates biological ground truth, and never present AF–Boltz DockQ as symmetric similarity.

### FreeSASA — AF single-structure computation

Reuse FreeSASA v2.2.1 settings from C01: Lee–Richards, probe radius 1.4 Å, 20 slices, ProtOr classifier, observed protein heavy atoms from the original AF coordinates only. Calculate isolated MPC1L SASA, isolated MPC2 SASA and complex SASA with the identical atom/radii policy. `DeltaSASA = SASA(MPC1L) + SASA(MPC2) − SASA(complex)`; `BSA_half = DeltaSASA/2`. Require complete radius-classification QC; otherwise `NOT RUN`. Explicitly report atom coverage and its differences between predicted and experimental structures. No BSA-to-affinity/free-energy inference.

## 10. Interchain interaction screens

**Tier 0, salt-bridge candidates:** identical C01 screen on observed heavy atoms; interchain Lys NZ / Arg NE,NH1,NH2 versus Asp OD1,OD2 / Glu OE1,OE2, distance strictly <4.0 Å. Save atom identities, min distances and unique residue pairs. Chemically unassessable missing functional atoms => `NOT EVALUABLE`, not zero.

**Tier 1, donor/acceptor proximity:** same C01 chemical typing and fixed D–A distance ≤3.0 Å, on original observed heavy atoms only. Save **atom-pair candidates**; do not claim validated hydrogen bonds.

**Tier 2, conditional hydrogenated geometry:** explicitly approved as a *conditional secondary only*, not Primary completion requirement. Attempt only under exact parent C01 validated environment/rules (OpenMM 8.2 series; PDBFixer 1.12; amber14-all.xml; pH 7 model; His HIE; only necessary terminal OXT additions; original heavy-atom displacement ≤1e-5 Å; full atom identity and force-field QC; positive/negative synthetic controls). D–A ≤3.0 Å, D–H–A ≥150°. If validation fails, `NOT RUN` with preserved failure logs: **no tolerance changes, coordinate optimization rescue or repeated arbitrary repairs**. Preserve 9GIX/9GIW/9GIY Tier 2 NOT RUN status from parent C01; avoid claims across insufficiently assessed experimental references.

## 11. Prediction confidence and provenance metadata

Record AF average pLDDT, ipTM, provided 263×263 PAE and available published pDockQ2/ipSAE/LIS. Record confidence information recoverable from original Boltz CIF. Preserve version, dataset, entry, algorithm and coordinate hash for each. Neither similarly named AF/Boltz confidence indices nor prediction confidence vs experimental Q-score are presumed calibrated across systems. PAE comparisons are conditional on definition equivalence, not Primary endpoints.

## 12. Frozen provenance uncertainty ledger

### AF-side evidence

**Individual CIF/report:** AlphaFold-Multimer weights v2.3.0; OpenFold-TRT/cuEq; MMseqs2-GPU release 18 and paired/filtered MSA; metadata explicitly states **`no templates`**; one model; no ligand atoms in coordinate; entry generation date 2026-02-20.

**Dataset-level evidence, not necessarily independently verified per run:** ColabFold-derived pipeline; sequence-search DB `uniref30_2302`; designated model1 final output; publication confidence filtering including pDockQ2max / ipSAEmax thresholds.

**Not individually recovered:** exact random seed; full input MSA and logs; independently rerun proof of template exclusion; all nonpublic intermediate candidates; possible indirect effects of older related protein structures. `no templates` is *direct individual metadata evidence*, not a reproduced run.

### Boltz-side evidence

**Individual:** original fixed CIF; model version Boltz-2 v2.1.1; repository/commit identity; Git addition 2025-06-29 17:41:41 UTC (not proven inference time).

**Atlas-level Methods, not individually verified run logs:** source UniProt sequences, MMseqs2 server, greedy MSA pairing, diffusion sample count 1, recycling steps 3, sampling steps 200, step scale 1.638, max MSA 8192 and `subsample_msa=False`, Google Colab/A100 High-RAM.

**Not individually recovered:** prediction timestamp, exact original YAML, template yes/no, command/log, seed, exact MSA and input server state, or any effect of structures available when prediction was performed. The word *de novo* and absence of YAML in the public repository **do not demonstrate** no-template inference.

### Training and inference information overlap

Reported structural training cutoffs: AF-Multimer v2.3.0 **2021-09-30** and Boltz-2 **2023-06-01** (use only as source-described model-family limits). Experimental PDBs 9GIX, 9GIV, 9GIW and 9GIY first released **2025-05-07**. Thus these *specific* experimental coordinates could not have entered the described weights under those stated cutoffs. This does **not** rule out related earlier training structures, use of inference-time structural templates (Boltz individually unresolved), or other indirect information overlap.

AF entry dates after experimental release; Boltz Git addition after experimental release, but Boltz true prediction date is unknown. Do not confuse publication/repository date with prediction date. Comparability is **not controlled** across pipelines, MSA creation, selection and availability of inference information.

### Model selection bias

AF DB item is a published **confidence-filtered NVIDIA** prediction, not a random raw sample or cherry-picked closest-to-experiment structure from the original paper's 100,000 AF-Multimer predictions. Boltz item is a single fixed Human PPI Atlas output drawn from its own target-PPI selection and diffusion sampling policy. These selection populations and mechanisms differ. There is no valid across-model performance benchmark based on two individual fixed structures.

## 13. Permitted versus prohibited interpretations

**Allowed:** fixed-mask geometric results for each named pair; specified local helix/residue/contact contrasts; sensitivity of conclusions to the fixed experimental reference and masks; provenance-qualified descriptive comparisons of these particular two predictions.

**Prohibited:** claims that one model family is generally better; statistical significance; conformational populations/state-selection probabilities; model architecture/MSA/template/seed as causal explanations; ligand-driven causal mechanism; guaranteed physiological validity from one score; energetic/affinity/kinetic conclusions; experimental proof of individual atom-pair H bonds or salt bridges; a new representative benchmark.

Reference-state/ligand differences are confounded: 9GIX apo inward versus the three ligand-associated outward structures. This cannot identify ligand causality. Data-quality asymmetry, especially Boltz template metadata absence, remains visible in results and figures.

## 14. Fixed execution flow — replicate C01 staged approach

- **Session A — Preflight and structural QC:** full hash, original file, six-structure residue crosswalk, saved mask matching, Kabsch numerical controls, known parent comparison control; GO/STOP for Primary.
- **Session B — Primary geometry:** *all five* frozen new pair comparisons; 73/62/198 and chain-alone/opposite-chain fit metrics; save full residual and transformation evidence before interpretation.
- **Session C — Local/helix secondary:** five preselected pairs, H1 proxy and H2/H3 within-structure geometry and numerical warning checks.
- **Session D — DockQ and FreeSASA:** five directional DockQ measurements, AF isolated/complex SASA and ProtOr radius QC.
- **Session E — Interaction candidates:** AF Tier 0/Tier 1; Tier 2 attempted only if frozen full QC passes, otherwise `NOT RUN`.
- **Session F — Independent audit and integration:** independent primary numerical check, all five pair reconciliation, provenance and source map, positive/negative/null outcomes, comparison with literature, assessment of incremental scientific value and MSC. **Do not integrate parent C01 results with Addendum interpretation until the Addendum-defined analyses have completed or reached their documented terminal NOT RUN/STOP disposition.** Parent C01's own Session 5 scientific assessment remains conceptually independent.

Every session report: (1) what was done, (2) observed results, (3) conclusions supported vs unsupported, (4) strength of evidence, (5) STOP conditions, (6) recommended next work. Record actual command, tool version, environment, source/derived mapping and failed attempts. Do not claim an analysis was performed when it was not.

## 15. Minimum reproducibility outputs

1. `INPUT_MANIFEST` with sources/hashes/revisions.
2. `RESIDUE_CROSSWALK` for six structures.
3. `MASK_QC` for 73/62/198 frozen lists.
4. `PRIMARY_5_COMPARISONS` complete measures.
5. `KABSCH_QC_AND_TRANSFORMS` with negative controls and per-atom residuals.
6. `LOCAL_GEOMETRY` for specified five pairs and helices.
7. `DOCKQ_RESULTS` with all five mapping/direction/CLI records.
8. `SASA_RESULTS` and radius/atom coverage checks.
9. `INTERACTION_CANDIDATES` Tier 0/1 and conditional Tier 2.
10. `PROVENANCE_AND_LIMITATIONS` symmetric AF/Boltz evidence ledger.
11. `INDEPENDENT_AUDIT` distinguishing independent recompute from same-code rerun.
12. `CURRENT_STATE_AND_STOP` with all failures, null/not-run and next-step status.

CSV/JSON/Markdown plus source code/logs as needed; no fabricated empty files or claimed outputs. Figures optional, never a substitute for machine-readable records.

## 16. STOP and change control

STOP affected work on input-hash inconsistency; missing/unreconciled saved masks or residue mapping; ambiguous protein-chain mapping; failed mandatory fit/negative control; unapproved coordinate movement; failed DockQ mapping; failed SASA radius check; Tier 2 fixed-QC breach. Failure of secondary checks does not retroactively invalidate a successful primary, but do not omit secondary NOT RUNs.

Forbidden after seeing results: selecting a different AF or Boltz model/seed; excluding unfavorable reference; changing 73/62/198 masks or fit method; relaxing thresholds; modifying salt/H-bond geometry cutoffs; concealing NULL outcomes; relabeling a prediction as native experimental truth. Any new question must be marked explicitly post hoc or placed into a separately versioned protocol; never silently appended to this frozen primary roster.

Parent C01 v1.0 remains unchanged.

## 17. Independent scientific-value and dissemination gate

After the analyses and independent audit, separately evaluate: **Scientific Validity**; **Minimum Scientific Contribution** relative to prior AF-Multimer MPC1L–MPC2 work and Human PPI Atlas; **Scholarly Publication Suitability**; and **Open Dissemination Value**. Publication is not presumed, and nonpublic CLOSE is an allowed outcome. A small or duplicated finding must not be inflated. The parent C01 contribution and this exploratory Addendum are evaluated separately.

## 18. Frozen pre-execution state

| Item | State at freeze |
|---|---|
| AF complex original coordinates and PAE | Retrieved; Gate A PASS |
| Boltz fixed atlas CIF | Retrieved; fixed repository file identified |
| Four experimental structures | Parent C01 originals already used; reuse unchanged |
| AF–experiment 198-residue mapping | Gate A PASS |
| 73 and 62 lists | Frozen in parent; check original list/hash at Session A |
| Parent C01 10 comparisons | Previously completed; not amended |
| AF–experiment four structural comparisons | **NOT RUN** |
| AF–Boltz one structural comparison | **NOT RUN** |
| AF local/helix, DockQ, SASA, Tier 0/1/2 | **NOT RUN** |
| General model-performance comparison | **NOT QUALIFIED** |
| This Addendum | **FINAL v1.0; analysis NOT STARTED** |
| Parent protocol | **v1.0 FINAL; unchanged** |

### Freeze declaration

This text fixes the exploratory comparison roster, endpoints, QC, analytic order, provenance uncertainties, interpretive boundaries and STOP criteria **before numerical AF comparisons**. No AF–Boltz or AF–experimental structural comparisons were newly computed in the course of preparing this document. Any later change requires explicit versioning and disclosure; the prior document and source data remain preserved.
