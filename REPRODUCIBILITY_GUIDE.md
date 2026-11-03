# Reproducibility guide

Tested environment: Linux, Python 3.12.14, exact installed versions in requirements.txt and verification/production_environment.json. All commands below were executed successfully from a clean extracted candidate directory. Normal operation is offline once dependencies are present. The supplied conda YAML is an environment specification; creating a new conda environment and downloading/installing packages on Windows were not tested in this production.

1. Obtain and extract the candidate ZIP; preserve the root folder name. The package already includes the permitted frozen source CIFs. No network fetch is required for numerical replay. Check provenance/SOURCE_MANIFEST.csv and UPSTREAM_CHECK.json before substituting a source; current upstream revisions are not interchangeable with frozen hashes.
2. Run `python code/verify_distribution.py --out reproduction/distribution`. This checks the frozen checksum list, canonical data identity, table cells, figure data, links, exceptions and rights/source manifests.
3. Run `python code/recompute_geometry.py --out reproduction/geometry`. It recalculates 105 RMSDs, the masks, all 480 contact rows and per-reference counts from the six original CIFs.
4. Run `python code/verify_independent.py --out reproduction/independent`. A separate CA parser and quaternion/eigenvalue fit independently checks all 105 RMSDs.
5. Run `python code/replay_auxiliary.py --out reproduction/auxiliary`. It recalculates H1/H2/H3, 30 local pairs and Tier0/1. It also checks saved DockQ outputs, FreeSASA arithmetic and five Tier2 triplets against saved rounded coordinates. No third-party engine is run by this command.
6. Run `python code/make_tables_figures.py --out-root reproduction/presentation`. It reproduces all table payloads and the two-panel Figure 1 from canonical CSVs without replacing the supplied manuscript.
7. Run `python code/build_documents.py --out-dir reproduction/pdfs`. It rebuilds the supplied editable Markdown using the distributed table metadata and Figure 1. DejaVu fonts default to Matplotlib's installed font directory; --font-dir can identify a complete installed DejaVu family.

The initial dependency command `python -m pip install --disable-pip-version-check -r requirements.txt` was executed successfully with all versions already installed; this is not a fresh-network-install validation. The tested checks depend on Python/NumPy/SciPy/Matplotlib/ReportLab/Pillow/pypdf/PyMuPDF, not on model weights or GPU libraries. Exact PDF/SVG bytes may depend on software/font environment; original distribution identity is always checked against supplied hashes. Scientific output equivalence is checked numerically.

## Verification levels

| Level | What readers can repeat | What is not claimed |
| --- | --- | --- |
| Identity/presentation | Hashes; selected numerical cells; README links; erratum/status; package identity | Scientific truth from a historical PASS label |
| Original-coordinate geometry | All 105 RMSDs, masks/contacts, H1/H2/H3 and 30 pairs | New prediction, state populations or mechanistic dynamics |
| Original normalized geometry | Tier0/1 all-observed atom screens | Hydrogen-bond experimental proof |
| Saved-engine inspection | DockQ/stdout consistency; FreeSASA arithmetic and radius metadata; accepted Tier2 snapshots | New DockQ/FreeSASA/OpenMM run, unrounded hydrogen placement or cryo-EM map reprocessing |

Historic Windows engine versions and assumptions are retained in manuscript/SI, code/archived and verification/historical. The development OpenMM build and stochastic hydrogen placement prevent promising a fully identical fresh hydrogen-placement run. Three experimental Tier2 screens remain NOT RUN; replaying other endpoints never fills their missing counts with zero.
