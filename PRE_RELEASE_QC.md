# C01 A+B pre-release computational QC

Candidate: Technical Note v1.0.0, 3 November 2026. This is a bounded computational/documentary QC within one AI-assisted production session, not independent experimental validation or a claim of external human review.

| Gate | Outcome and verified scope |
| --- | --- |
| G1 Scientific integrity | PASS for the frozen limited claim; A Primary and B Exploratory; previous Sichrovsky/Ille findings credited; no independent MSC, model ranking or new mechanism asserted |
| G2 Numerical integrity | PASS:105 original-coordinate RMSDs; independent quaternion max difference2.2870594307278225e-14Å;508 direct numerical table cells mapped;14 figure comparisons and README principal values checked |
| G3 Data identity | PASS:344 supplied A+B provenance records rehashed; selected unchanged public copies match source hashes; normalized/derived representations distinguished |
| G4 Reproduction | PASS within documented tiers: commands tested from a clean extracted candidate; no fresh Windows/dependency-download or third-party engine execution claimed |
| G5 Exceptions | PASS: rejected H1 PCA,9GIX MPC2 H1 flag, between-state bundle NOT QUALIFIED/NOT RUN, three Tier2 NOT RUN and historical AF typo all retained |
| G6 Rights | Source-material scope checked: PDBCC0, fixed AtlasMIT, AF per-fileCC-BY-4.0; third-party reports/articles/weights/MSAs excluded. Author approved ownership and proposed licenses on 3 Nov; publication identifiers still pending |
| G7 Presentation | PASS:9-page Technical Note and17-page SI, all26pages rendered and inspected; no clipped tables, detached figure caption, missing glyph or overlap found |
| G8 Release structure | PASS for a local candidate; Zenodo DOI 10.5281/zenodo.23910491 reserved (unpublished); real GitHub tag/commit and Zenodo publication remain pending; manifest/checksum exclusions prevent self-hashing cycles |

## Verification depth

Freshly recomputed:105RMSDs,73/62masks,480contacts,H1/H2/H3,30localpairs and all-observed Tier0/1. Saved-output checks only:15DockQ outputs,FreeSASA arithmetic/radius records,five Tier2triplets against rounded hydrogenated snapshots. DockQ/FreeSASA/OpenMM/PDBFixer/cryo-EM engines were not rerun.

Production caught and corrected a draft documentation count: the quality CSV has308rows, comprising77positions/reference(73interface+four quality-context positions), not292. The unchanged source CSV was always retained. It also resolved the earlier historical empty Tier2file as a noncanonical failed implementation attempt. No scientific result, threshold or mask was changed to make QC pass.

## Overall disposition

**CONDITIONAL for public release.** Numerical and scientific production is complete within the stated scope. The author has confirmed funding/competing-interest statements, ownership and intended own-material licenses. Final publication approval and actual DOI/tag/commit creation remain separate future actions. Actual repository/tag/commit/DOI creation and subsequent identifier/hash rebuild are separate future actions. No publication was performed.

See current_geometry/,current_independent/,current_auxiliary/,analysis_status.csv,ERRATUM.md and provenance/ for machine-readable evidence and the publication checklist. Full delivery QC and release receipts accompany the master delivery outside the scientific repository payload.
