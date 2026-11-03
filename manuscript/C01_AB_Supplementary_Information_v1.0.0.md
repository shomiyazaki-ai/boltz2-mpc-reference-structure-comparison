# Supplementary Information

## Experimental-Reference Sensitivity of a Fixed Boltz-2 MPC1L–MPC2 Complex Prediction, with an Exploratory AlphaFold Structural Comparison

**Sho Miyazaki**  
Independent researcher, Tokyo, Japan  
Correspondence: shomiyazaki98@gmail.com  
Technical Note supplement | Version 1.0.0 publication candidate | 3 November 2026  
Zenodo version DOI (reserved; unpublished): 10.5281/zenodo.23910491 (https://doi.org/10.5281/zenodo.23910491).

This supplement supplies the source-to-result chain for C01 A (Primary fixed Boltz comparison) and B (Exploratory fixed AlphaFold-derived comparison). It introduces no new prediction, state classification, simulation or scientific endpoint. References [1]–[9] refer to the Technical Note bibliography. Numerical CSVs retain their original identifiers and full stored precision; displayed tables are reproducibly selected views.

The Boltz-2 and AlphaFold-Multimer method-development papers are cited as [10] and [11] in the accompanying Technical Note; these do not replace the exact model-specific coordinate provenance below.

## S1. Structural sources, provenance and correspondence

### S1.1 Original inputs and upstream identity

The original-coordinate population comprises exactly six CIFs (Table S1). The Boltz-2 v2.1.1 file comes from atlas row 147, MPC2 O95563–MPC1L P0DKB6, at fixed repository commit dc55acabb3da7f233def7a0668d86e1c0ecb8e8e. On 3 November 2026 its complete upstream content was retrieved through the connected repository reader and matched the supplied 181,658 bytes and SHA-256 3ef95557b603f6c32bcf2193158ff3bfe621f92c60013cdec7c15438c3f4fe64. The MIT notice at the same commit was also retrieved. This checks source identity; it does not reconstruct the individual inference.

<!-- TABLE S1 START -->
**Table S1. Structural source identities and data scope**

| Input | Provider / version | Original CIF SHA-256 prefix | Role / source scope |
| --- | --- | --- | --- |
| Boltz-2 | Atlas / fixed dc55acabb3da | 3ef95557b603f6c3 | Primary A |
| 9GIX | wwPDB / frozen revision | 259122a5920a96ad | Experimental reference |
| 9GIV | wwPDB / frozen revision | f24c5284eb3f5e4c | Experimental reference |
| 9GIW | wwPDB / frozen revision | 3143bb38783b9901 | Experimental reference |
| 9GIY | wwPDB / frozen revision | 202a977dd1bf428e | Experimental reference |
| AlphaFold | AFDB/NVIDIA / v1 | cebf20bfa086949b | Exploratory B |

*Full hashes and original archive-member identities are in provenance/SOURCE_MANIFEST.csv. Short hashes are visual keys only, not replacements for full hashes.*
<!-- TABLE S1 END -->

Experimental state/condition assignments are 9GIX apo inward-open, 9GIV C7 outward-open, 9GIW zaprinast outward-open and 9GIY mitoglitazone outward-open, following Sichrovsky et al. [1]. Their EMDB entries are EMD-51380, EMD-51378, EMD-51379 and EMD-51381, respectively. All are human target complexes determined by single-particle cryo-EM. PMb25, inhibitors and other non-target components remain present in original CIFs but are excluded from target–target numerical geometry. Comparison does not equate the purified experimental construct with an entire cellular complex.

The experimental CIF revision dates recorded with the saved validation work are 7 May 2025 for 9GIX, 9GIW and 9GIY, and 15 April 2026 for 9GIV. Current web metadata are contextual and do not replace the frozen bytes. Coordinate/revision identity, not a freshly fetched “latest” coordinate set, defines this release.

### S1.2 Exploratory AlphaFold provenance and uncertainties

The fixed AlphaFold-derived CIF is AF-0000000204012512-model_v1.cif, 179,810 bytes, SHA-256 cebf20bfa086949b1dbe0d9137c12a36e06a8311b7f69e7b7ba6587eada485e1. It declares AlphaFold-Multimer v2.3.0 weights, OpenFold-TRT/cuEq acceleration and MMseqs2-GPU paired-MSA generation. Its protocol details declare no templates, one model, at most four recycles and an ipTM early-stopping threshold of 0.1. These are embedded source declarations, not independently reproduced inference settings. A seed and full individual paired MSA/selection trace are unavailable.

Date fields are not conflated: a historical source report recorded a displayed creation date of 20 February 2026; the frozen CIF initial-deposition field is 21 February 2026 and its revision-history date is 17 November 2025. None is treated as a verified inference timestamp. Likewise, the Boltz file's recorded first GitHub addition on 29 June 2025 is an upload event, not a proven prediction-generation date. The corresponding provenance uncertainty is retained; no leakage-free or matched-generation conclusion follows.

A saved 263×263 PAE matrix exists, with source SHA-256 c3960b35e52f0a0a04963c85482513f8984842eaf314d3778f4fc87de1d3bd84 and 364,438 bytes. It is not an input to a published C01 endpoint and is not redistributed. The CIF and provenance ledger suffice to identify the chosen structure; PAE omission reduces unused data duplication. Source entry and filename permit re-acquisition under AFDB terms. No new PAE analysis is reported.

### S1.3 Mapping and original-versus-derived coordinates

<!-- TABLE S2 START -->
**Table S2. Protein identity and chain correspondence**

| Input | Protein / UniProt | Source label chain; entity | Common label_seq positions | Source auth_seq positions |
| --- | --- | --- | --- | --- |
| Boltz-2 | MPC1L / P0DKB6 | B; 2 | 22-105 (84) | Same numeric positions |
| Boltz-2 | MPC2 / O95563 | A; 1 | 8-121 (114) | Same numeric positions |
| 9GIX | MPC1L / P0DKB6 | A; 1 | 22-105 (84) | Same numeric positions |
| 9GIX | MPC2 / O95563 | B; 2 | 8-121 (114) | Same numeric positions |
| 9GIV | MPC1L / P0DKB6 | A; 1 | 22-105 (84) | Same numeric positions |
| 9GIV | MPC2 / O95563 | B; 2 | 8-121 (114) | Same numeric positions |
| 9GIW | MPC1L / P0DKB6 | A; 1 | 22-105 (84) | Same numeric positions |
| 9GIW | MPC2 / O95563 | B; 2 | 8-121 (114) | Same numeric positions |
| 9GIY | MPC1L / P0DKB6 | A; 1 | 22-105 (84) | Same numeric positions |
| 9GIY | MPC2 / O95563 | B; 2 | 8-121 (114) | Same numeric positions |
| AlphaFold | MPC1L / P0DKB6 | B; 1 | 22-105 (84) | Same numeric positions |
| AlphaFold | MPC2 / O95563 | A; 2 | 8-121 (114) | Same numeric positions |

*Normalized auxiliary PDBs use A=MPC1L and B=MPC2 for all structures. Entity and label/auth namespaces remain separate. The full 1,188-row Cα crosswalk and primary observed-atom crosswalk are supplied as unchanged CSVs.*
<!-- TABLE S2 END -->

Common positions are established by sequence identity and Cα availability in each structure. The unchanged crosswalk has 6×198=1,188 rows. It records the source label chain, aligned label_seq position, amino-acid identity and author residue number; no missing or identity-discordant Cα occurs in the declared sets. Source entity assignments are checked separately. For these common positions the author and aligned numerical residue positions agree; that agreement is a verified property of these files, not a general rule for PDB data.

The primary observed-atom crosswalk retains source identifiers and atomic coordinates. A normalized two-chain PDB is a separate, rounded export, consistently A=MPC1L and B=MPC2. It is used for saved DockQ, FreeSASA and all-observed-atom Tier 0/1 screens. It is not substituted for the full-precision CIF in RMSD, mask or local-geometry replay. Original Boltz atom records include a comment inside the loop header and a few model-number tokens on following lines. The portable reader parses the CIF token stream without modifying those bytes.

Accepted hydrogenated PDBs are separately marked DERIVED and limited to Boltz, 9GIV and AF. Their added H/OXT atoms are never used to redefine original masks, original local geometry or SASA. The source manifest distinguishes unchanged copies from explicit excerpts or privacy-curated JSON; similarly named historical files with different contents are not treated as interchangeable.

## S2. Fixed interface masks and alignment definitions

### S2.1 Heavy-atom contact union

Within the 198 common positions, the shortest observed heavy-atom distance is computed for every cross-chain residue pair in each experimental reference. Heavy atoms are determined by element, excluding H/D. The 5.0 Å and 4.0 Å inequalities are strict. A residue enters the relevant mask if it occurs in any selected pair in any of the four experimental references. Different per-reference pair counts therefore contribute to one fixed union, rather than creating four separate fitted masks.

<!-- TABLE S3 START -->
**Table S3. Frozen residue masks**

| Mask | MPC1L aligned residue positions | MPC2 aligned residue positions |
| --- | --- | --- |
| 73 residues | 25, 26, 27, 28, 30, 31, 32, 34, 35, 37, 38, 41, 44, 45, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 63, 64, 67, 68, 70, 71, 74, 75, 76, 77, 79, 82, 93 | 39, 40, 41, 42, 44, 45, 46, 48, 49, 51, 52, 55, 56, 58, 59, 62, 65, 66, 67, 68, 70, 71, 74, 75, 77, 78, 81, 82, 84, 85, 88, 89, 90, 93, 96, 110 |
| 62 residues | 27, 28, 30, 31, 32, 34, 35, 37, 38, 41, 44, 45, 51, 52, 53, 54, 56, 57, 60, 61, 64, 67, 68, 70, 71, 74, 75, 76, 79, 82 | 40, 41, 42, 45, 46, 48, 49, 51, 52, 55, 56, 58, 59, 62, 65, 66, 68, 70, 71, 74, 75, 77, 78, 81, 82, 84, 85, 88, 89, 90, 93, 96 |
| 198 residues | 22-105 inclusive (84) | 8-121 inclusive (114) |

*Masks are unions of contacting residue identities from the four experimental structures, restricted to the common sequence region. The 73-residue mask comprises 37 MPC1L + 36 MPC2 sites; the 62-residue mask has 30 + 32 sites. No prediction defines or modifies either mask.*
<!-- TABLE S3 END -->

<!-- TABLE S3a START -->
**Table S3a. Reference-specific contact-pair counts (separate from the mask union)**

| Reference | Heavy-atom pair-of-residues <5 Å | Heavy-atom pair-of-residues <4 Å |
| --- | --- | --- |
| 9GIX | 57 | 31 |
| 9GIV | 84 | 43 |
| 9GIW | 82 | 45 |
| 9GIY | 86 | 52 |

*Per-reference pairs are unique cross-chain residue pairs selected by their closest observed heavy atoms. Union/intersection counts over all references are 107/37 at <5 Å and 69/13 at <4 Å. These pair counts differ from residue-mask sizes.*
<!-- TABLE S3a END -->

The pair unions/intersections are 107/37 for <5.0 Å and 69/13 for <4.0 Å. The corresponding Cα site unions are 73 and 62; these are different counting units. All 480 threshold/reference/contact rows, closest atom names and distances are supplied in experimental_contacts.csv. They were replayed from the original CIFs and matched the stored rows and distances. A threshold is an operational geometric convention, not proof of physiological interaction.

### S2.2 Proper rigid-body fit and evaluation sets

For corresponding site vectors x and y, translation removes their centroids and a proper rotation (determinant +1) minimizes the sum of squared residuals on the declared fit set. RMSD is the square root of the mean squared Euclidean residual over the declared evaluation set. No reflection, scaling, per-atom weight or flexible fitting is used. Primary and sensitivity same-mask results fit/evaluate exactly 73/73, 62/62 or 198/198 sites.

An independent MPC1L fit uses 84/84 sites and an independent MPC2 fit uses 114/114. Cross-chain “fit MPC1L; evaluate MPC2” uses 84 fitted sites and 114 evaluated sites; the reverse uses 114 and 84. The opposite chain is transformed once and is not refitted. Source/target ordering remains in the canonical CSV, even though a same-mask optimal RMSD is symmetric. Cross-chain evaluation is direction-specific. This is an RMS displacement measure under a chosen fit, not a decomposition into translation, rotation and internal deformation.

## S3. Complete structural comparison results

### S3.1 All 70 Primary/control values

Tables S4 and S5 together contain the full ten-comparison, seven-metric Primary/control roster. The exact values, fit/evaluation mask identifiers, dimensions and source/target IDs remain in primary_70_metrics.csv. Fitting transforms and Primary squared residuals are distributed for direct inspection.

<!-- TABLE S4 START -->
**Table S4. All ten Primary/control comparisons: mask fits**

| Source vs target | 73 residues (Å) | 62 residues (Å) | 198 residues (Å) |
| --- | --- | --- | --- |
| Boltz-2 vs 9GIX | 3.853976 | 3.727117 | 4.478252 |
| Boltz-2 vs 9GIV | 0.964115 | 0.804675 | 1.482408 |
| Boltz-2 vs 9GIW | 1.217374 | 0.948745 | 1.662196 |
| Boltz-2 vs 9GIY | 1.077057 | 0.872235 | 1.638168 |
| 9GIX vs 9GIV | 3.879390 | 3.791126 | 4.105163 |
| 9GIX vs 9GIW | 3.848898 | 3.758054 | 4.100730 |
| 9GIX vs 9GIY | 3.769616 | 3.651809 | 4.016776 |
| 9GIV vs 9GIW | 0.605305 | 0.528742 | 0.700510 |
| 9GIV vs 9GIY | 0.572130 | 0.587691 | 0.673923 |
| 9GIW vs 9GIY | 0.510085 | 0.470499 | 0.552616 |

*Thirty of the 70 Primary/control RMSD values. Each same-mask value uses its own optimal proper rotation.*
<!-- TABLE S4 END -->

<!-- TABLE S5 START -->
**Table S5. All ten Primary/control comparisons: chain fits**

| Source vs target | MPC1L own fit (Å) | MPC2 own fit (Å) | Fit MPC1L; eval MPC2 (Å) | Fit MPC2; eval MPC1L (Å) |
| --- | --- | --- | --- | --- |
| Boltz-2 vs 9GIX | 0.858598 | 4.172290 | 8.303083 | 6.251804 |
| Boltz-2 vs 9GIV | 1.189383 | 1.503577 | 1.941535 | 1.689469 |
| Boltz-2 vs 9GIW | 1.469730 | 1.499637 | 2.264895 | 2.135073 |
| Boltz-2 vs 9GIY | 1.260680 | 1.641993 | 2.261337 | 1.879886 |
| 9GIX vs 9GIV | 1.493826 | 3.428245 | 7.431628 | 6.420725 |
| 9GIX vs 9GIW | 1.826467 | 3.201234 | 7.220475 | 6.759895 |
| 9GIX vs 9GIY | 1.613325 | 3.031900 | 7.350533 | 6.718717 |
| 9GIV vs 9GIW | 0.697552 | 0.568581 | 0.918934 | 1.021969 |
| 9GIV vs 9GIY | 0.537053 | 0.693418 | 0.834145 | 0.805590 |
| 9GIW vs 9GIY | 0.504219 | 0.533695 | 0.814933 | 0.604768 |

*The remaining 40 Primary/control RMSD values. Direction follows the source/target fields of primary_70_metrics.csv; cross-chain evaluation remains directional.*
<!-- TABLE S5 END -->

### S3.2 All 35 Exploratory AlphaFold values

Tables S6a and S6b split one functional table for readability; no AF comparison or metric has been removed. The first four target rows are experimental references, and the fifth is the direct fixed AlphaFold–Boltz contrast. The latter is not included in main Table 2's 14 experiment-related comparisons. Canonical AF_35_metrics.csv also retains original independent/permutation checks and determinants.

<!-- TABLE S6a START -->
**Table S6a. Exploratory AF comparisons: all mask fits**

| AF vs target | 73 residues (Å) | 62 residues (Å) | 198 residues (Å) |
| --- | --- | --- | --- |
| 9GIX | 4.045460 | 3.898180 | 4.494276 |
| 9GIV | 1.794373 | 1.613407 | 2.780255 |
| 9GIW | 1.966428 | 1.685311 | 2.858654 |
| 9GIY | 1.837599 | 1.621598 | 2.617355 |
| Boltz-2 | 1.477727 | 1.345477 | 3.198991 |

*Part of Table S6: all 15 mask-fit values. AF-9GIX 62-residue value is the canonical corrected 3.898180 Å.*
<!-- TABLE S6a END -->

<!-- TABLE S6b START -->
**Table S6b. Exploratory AF comparisons: all chain fits**

| AF vs target | MPC1L own fit (Å) | MPC2 own fit (Å) | Fit MPC1L; eval MPC2 (Å) | Fit MPC2; eval MPC1L (Å) |
| --- | --- | --- | --- | --- |
| 9GIX | 0.836249 | 2.167649 | 9.564685 | 8.608025 |
| 9GIV | 1.291156 | 2.344830 | 5.463853 | 4.636346 |
| 9GIW | 1.572645 | 2.220871 | 5.421768 | 5.068413 |
| 9GIY | 1.366558 | 1.919534 | 5.299891 | 4.878237 |
| Boltz-2 | 0.374431 | 3.174292 | 6.062724 | 4.969347 |

*Part of Table S6: all 20 chain-fit values. Together S6a/S6b show all 35 AF RMSD values. AF-Boltz is a fixed-coordinate contrast, with Boltz as operational target.*
<!-- TABLE S6b END -->

## S4. DockQ and solvent-accessible surface area

### S4.1 Directional DockQ descriptors

DockQ 2.1.3 was historically run on two-chain normalized exports with explicit AB:AB mapping. The original source model has reversed protein chain letters relative to experiment; normalization resolves that difference before DockQ. Applying AB:BA again to the normalized coordinates would instead create an erroneous protein mapping. The source and normalized namespaces must not be combined.

DockQ combines native-contact recovery and standard interface/ligand RMSD terms. Its contact denominators and model/native roles are directional. We preserve each saved role and do not replace the custom 73-Cα RMSD with DockQ iRMSD or interpret a DockQ score as a probability of accuracy. The AF-versus-Boltz score uses Boltz only as the operational native argument, not as experimental truth.

<!-- TABLE S7 START -->
**Table S7. DockQ directional saved-engine outputs**

| Model vs native | DockQ | Standard iRMSD (Å) | LRMSD (Å) | Fnat |
| --- | --- | --- | --- | --- |
| Boltz-2 vs 9GIX | 0.465 | 2.839 | 6.229 | 0.526 |
| Boltz-2 vs 9GIV | 0.798 | 1.137 | 1.700 | 0.798 |
| Boltz-2 vs 9GIW | 0.738 | 1.416 | 2.956 | 0.793 |
| Boltz-2 vs 9GIY | 0.767 | 1.240 | 2.553 | 0.791 |
| 9GIX vs 9GIV | 0.406 | 3.891 | 6.590 | 0.464 |
| 9GIX vs 9GIW | 0.406 | 3.908 | 6.742 | 0.476 |
| 9GIX vs 9GIY | 0.408 | 3.851 | 6.387 | 0.453 |
| 9GIV vs 9GIW | 0.926 | 0.683 | 1.027 | 0.963 |
| 9GIV vs 9GIY | 0.928 | 0.598 | 0.830 | 0.930 |
| 9GIW vs 9GIY | 0.932 | 0.518 | 1.055 | 0.919 |
| AlphaFold vs 9GIX | 0.333 | 3.026 | 9.061 | 0.333 |
| AlphaFold vs 9GIV | 0.576 | 2.211 | 4.487 | 0.631 |
| AlphaFold vs 9GIW | 0.522 | 2.437 | 6.294 | 0.646 |
| AlphaFold vs 9GIY | 0.543 | 2.082 | 6.261 | 0.640 |
| AlphaFold vs Boltz-2 | 0.437 | 2.790 | 13.349 | 0.797 |

*DockQ 2.1.3. These iRMSDs are DockQ definitions, not the frozen 73-Cα endpoint. All normalized files use identity mapping AB:AB. Full canonical CSVs also retain fnonnat, F1, clashes or run status; all 15 stdout numerical excerpts are supplied. Engine not rerun for this production.*
<!-- TABLE S7 END -->

Full parsed CSVs preserve additional fnonnat, F1, clash and/or run fields. Fifteen saved numerical stdout excerpts are included with original source hashes and transformations in SOURCE_MANIFEST. Nonessential local paths and program banners were removed from those excerpts. Fresh QC compared all tabulated core DockQ scalars with these saved outputs; no DockQ engine rerun is claimed.

### S4.2 FreeSASA definitions, coverage and radius audit

FreeSASA 2.2.1 used observed heavy atoms of the two target proteins only, with Lee–Richards integration, probe radius 1.4 Å, 20 slices and the standard ProtOr classifier. Macrobody, ligand, lipid, detergent, water and modeled OXT/H atoms are excluded. Atom inclusion within a structure is identical for isolated-chain and complex calculations. Delta SASA is the sum of isolated-chain areas minus complex area; half-BSA is its half. Values are neither corrected for a membrane environment nor converted into energy.

<!-- TABLE S8 START -->
**Table S8. FreeSASA areas and observed heavy-atom coverage**

| Structure | MPC1L SASA (Å²) | MPC2 SASA (Å²) | Complex SASA (Å²) | ΔSASA (Å²) | Half-BSA (Å²) | Atoms |
| --- | --- | --- | --- | --- | --- | --- |
| Boltz-2 | 10332.611 | 9277.923 | 17181.463 | 2429.070 | 1214.535 | 2070 |
| 9GIX | 7940.768 | 8138.269 | 14121.913 | 1957.124 | 978.562 | 1754 |
| 9GIV | 6319.902 | 9040.670 | 12588.426 | 2772.147 | 1386.073 | 1628 |
| 9GIW | 7080.892 | 8624.325 | 12809.873 | 2895.344 | 1447.672 | 1662 |
| 9GIY | 8138.453 | 8571.708 | 13860.980 | 2849.181 | 1424.590 | 1764 |
| AlphaFold | 11383.102 | 9441.265 | 18516.066 | 2308.302 | 1154.151 | 2070 |

*Lee-Richards; 1.4 Å probe; 20 slices; ProtOr radii. Within each structure the same atom policy is used for isolated chains and complex. Cross-structure heavy-atom coverage differs; no energy or affinity interpretation follows. Primary columns A/B here refer to normalized chains A=MPC1L/B=MPC2. Engine not rerun for this production.*
<!-- TABLE S8 END -->

The five Primary inputs retain 2,070, 1,754, 1,628, 1,662 and 1,764 observed heavy atoms for Boltz, 9GIX, 9GIV, 9GIW and 9GIY; AF retains 2,070. Canonical rows contain per-chain atom counts and translation-invariance differences. Historical per-atom ProtOr audits recorded positive classified radii, no unknown/bad or zero-radius atoms, and agreement between explicit and loaded/default radii. Those complete audit CSVs are supplied, including all 2,070 AF atom rows. The release rechecks areas algebraically and inspects radius records; it does not rerun the surface-area engine.

## S5. Local geometry and interaction candidate analyses

### S5.1 H1 local axes, sensitivity and rejected method

The frozen windows are MPC1L 26–48 with nominated hinge 33, and MPC2 40–61 with nominated hinge 53. A four-Cα window supplies a local axis normal to adjacent second-difference vectors, using the HELANAL-type definition [7,8]. Each unit axis is oriented to have positive dot product with the full-window endpoint displacement. Local-axis starts ≤hinge−4 form the left set; starts ≥hinge+1 form the right set. Intervening axes are excluded from the two mean vectors. The bend proxy is the directed angle between normalized mean axes; at least two axes per side are required.

The endpoint sensitivity considers full, first-axis-dropped and last-axis-dropped variants on each side, retaining at least two axes. The largest absolute angle change from the full estimate is compared with the strict >5° sensitivity flag. This flag is computational, not a statistical test or an angular confidence interval. The full local-axis and mean-resultant records remain in the canonical CSVs.

<!-- TABLE S9 START -->
**Table S9. H1 local-axis proxy and endpoint sensitivity**

| Structure | Protein | Bend (°) | Max endpoint change (°) | Left / right axes | Flag |
| --- | --- | --- | --- | --- | --- |
| AlphaFold | MPC1L | 13.372 | 2.322 | 4 / 12 | No >5° flag |
| AlphaFold | MPC2 | 6.835 | 1.615 | 10 / 5 | No >5° flag |
| Boltz-2 | MPC1L | 19.598 | 3.029 | 4 / 12 | No >5° flag |
| Boltz-2 | MPC2 | 10.671 | 2.413 | 10 / 5 | No >5° flag |
| 9GIX | MPC1L | 17.329 | 4.144 | 4 / 12 | No >5° flag |
| 9GIX | MPC2 | 25.970 | 5.019 | 10 / 5 | >5° sensitivity |
| 9GIV | MPC1L | 26.949 | 3.079 | 4 / 12 | No >5° flag |
| 9GIV | MPC2 | 6.359 | 2.844 | 10 / 5 | No >5° flag |
| 9GIW | MPC1L | 35.030 | 3.863 | 4 / 12 | No >5° flag |
| 9GIW | MPC2 | 13.086 | 2.905 | 10 / 5 | No >5° flag |
| 9GIY | MPC1L | 29.263 | 2.714 | 4 / 12 | No >5° flag |
| 9GIY | MPC2 | 6.105 | 3.012 | 10 / 5 | No >5° flag |

*MPC1L window 26-48, hinge 33; MPC2 40-61, hinge 53. Left starts ≤hinge-4; right starts ≥hinge+1. Mean resultant lengths and every local axis remain in the unchanged CSVs. The 9GIX MPC2 flag is retained, not relabeled PASS.*
<!-- TABLE S9 END -->

9GIX MPC2 has max endpoint change 5.018945552639998° (display 5.019°), retaining H1_NUMERIC_SENSITIVITY_GT5. It cannot support a claim of robust quantitative hinge magnitude across unrestricted window choices. Absence of this one flag does not establish global robustness for the other estimates.

The earlier short-window PCA construction (MPC1L 26–30 versus 38–45; MPC2 40–47 versus 57–61) failed endpoint sensitivity checks. The supplied historical table records 54 variants per input/protein and maximum changes from 16.54018° to 70.03196°; every one of its ten rows has a >5° flag. These rejected estimates are retained only as negative qualification evidence and are not mixed into Table S9. The portable replay independently recalculated the accepted local-axis proxy without requiring an MDAnalysis installation; it does not redistribute MDAnalysis package code.

### S5.2 H2/H3 within-structure geometry and unqualified between-state rotation

Longer H2/H3 segments are fitted independently to centered Cα PCA axes within each structure. Axis direction follows the N-to-C endpoint vector. Both the directed angle and its acute equivalent are retained, alongside eigenvalue anisotropy and segment coverage. All inputs have the declared H2/H3 segment sites.

<!-- TABLE S10 START -->
**Table S10. H2/H3 within-structure axis angles**

| Structure | Protein | Directed angle (°) | Acute angle (°) | H2 anisotropy | H3 anisotropy |
| --- | --- | --- | --- | --- | --- |
| AlphaFold | MPC1L | 159.698 | 20.302 | 27.797 | 40.184 |
| AlphaFold | MPC2 | 155.025 | 24.975 | 26.486 | 55.767 |
| Boltz-2 | MPC1L | 160.068 | 19.932 | 26.382 | 37.632 |
| Boltz-2 | MPC2 | 153.699 | 26.301 | 29.547 | 51.045 |
| 9GIX | MPC1L | 160.764 | 19.236 | 29.220 | 43.890 |
| 9GIX | MPC2 | 157.045 | 22.955 | 29.049 | 55.474 |
| 9GIV | MPC1L | 157.830 | 22.170 | 26.117 | 45.062 |
| 9GIV | MPC2 | 152.034 | 27.966 | 31.997 | 49.261 |
| 9GIW | MPC1L | 159.558 | 20.442 | 27.630 | 46.706 |
| 9GIW | MPC2 | 152.997 | 27.003 | 31.444 | 54.166 |
| 9GIY | MPC1L | 159.348 | 20.652 | 26.008 | 45.108 |
| 9GIY | MPC2 | 153.520 | 26.480 | 29.089 | 52.797 |

*MPC1L H2 54-75 and H3 79-105; MPC2 H2 68-89 and H3 93-121. Anisotropy is the largest/second-largest centered-Cα scatter eigenvalue ratio. Directed axes face N to C; acute angle is min(θ,180-θ). Between-state rigid bundle rotation is NOT QUALIFIED / NOT RUN for all structures.*
<!-- TABLE S10 END -->

These within-structure angles do not reproduce the original paper's between-state bundle rotations. No outcome-independent stable reference frame was qualified for the latter endpoint, so between-state bundle rotation remains NOT QUALIFIED / NOT RUN. A numerical self-fit of a helix bundle is not substituted for the missing physical reference frame, and the published mechanistic rotation is not claimed as a C01 result.

### S5.3 Predefined local residue pairs

Five pairs were evaluated for each structure: MPC1L Glu51–MPC2 Lys66; MPC2 Trp82–MPC1L Ser35; MPC2 Trp82–MPC1L Gly31; MPC2 Ile90–MPC1L Gln76; and MPC2 Tyr85–MPC1L Asn79. For each, the full Cα distance, closest observed inter-residue heavy-atom distance/names and strict <4/<5 Å flags are retained. No protonation or alignment is required for these within-structure scalar distances.

<!-- TABLE S11 START -->
**Table S11. All 30 predefined local residue-pair geometries**

| Structure | Residue pair | Cα distance (Å) | Minimum heavy distance (Å) | Closest observed atoms | <4 / <5 Å |
| --- | --- | --- | --- | --- | --- |
| AlphaFold | MPC1L 51 - MPC2 66 | 5.955 | 3.633 | O - CB | True / True |
| AlphaFold | MPC2 82 - MPC1L 35 | 9.379 | 3.551 | NE1 - OG | True / True |
| AlphaFold | MPC2 82 - MPC1L 31 | 7.615 | 3.148 | CZ2 - CA | True / True |
| AlphaFold | MPC2 90 - MPC1L 76 | 12.644 | 8.313 | O - O | False / False |
| AlphaFold | MPC2 85 - MPC1L 79 | 16.302 | 10.128 | CD2 - ND2 | False / False |
| Boltz-2 | MPC1L 51 - MPC2 66 | 6.202 | 3.914 | O - CB | True / True |
| Boltz-2 | MPC2 82 - MPC1L 35 | 9.147 | 2.836 | NE1 - OG | True / True |
| Boltz-2 | MPC2 82 - MPC1L 31 | 6.878 | 3.181 | CZ2 - C | True / True |
| Boltz-2 | MPC2 90 - MPC1L 76 | 12.597 | 8.220 | O - O | False / False |
| Boltz-2 | MPC2 85 - MPC1L 79 | 14.598 | 6.050 | OH - ND2 | False / False |
| 9GIX | MPC1L 51 - MPC2 66 | 22.632 | 19.906 | O - CE | False / False |
| 9GIX | MPC2 82 - MPC1L 35 | 9.326 | 4.096 | CZ2 - CB | False / True |
| 9GIX | MPC2 82 - MPC1L 31 | 5.607 | 2.905 | NE1 - O | True / True |
| 9GIX | MPC2 90 - MPC1L 76 | 5.323 | 3.046 | N - O | True / True |
| 9GIX | MPC2 85 - MPC1L 79 | 11.291 | 3.238 | OH - ND2 | True / True |
| 9GIV | MPC1L 51 - MPC2 66 | 6.316 | 2.777 | OE1 - NZ | True / True |
| 9GIV | MPC2 82 - MPC1L 35 | 9.425 | 3.113 | NE1 - OG | True / True |
| 9GIV | MPC2 82 - MPC1L 31 | 5.956 | 3.138 | CZ2 - C | True / True |
| 9GIV | MPC2 90 - MPC1L 76 | 15.107 | 10.940 | O - O | False / False |
| 9GIV | MPC2 85 - MPC1L 79 | 14.681 | 7.094 | OH - ND2 | False / False |
| 9GIW | MPC1L 51 - MPC2 66 | 5.967 | 2.738 | OE1 - NZ | True / True |
| 9GIW | MPC2 82 - MPC1L 35 | 9.234 | 3.140 | NE1 - OG | True / True |
| 9GIW | MPC2 82 - MPC1L 31 | 5.839 | 3.404 | CZ2 - C | True / True |
| 9GIW | MPC2 90 - MPC1L 76 | 13.926 | 9.614 | O - O | False / False |
| 9GIW | MPC2 85 - MPC1L 79 | 13.967 | 5.170 | OH - ND2 | False / False |
| 9GIY | MPC1L 51 - MPC2 66 | 6.256 | 2.942 | OE2 - NZ | True / True |
| 9GIY | MPC2 82 - MPC1L 35 | 9.076 | 3.155 | NE1 - OG | True / True |
| 9GIY | MPC2 82 - MPC1L 31 | 5.826 | 3.147 | CZ2 - O | True / True |
| 9GIY | MPC2 90 - MPC1L 76 | 12.409 | 8.248 | O - O | False / False |
| 9GIY | MPC2 85 - MPC1L 79 | 14.407 | 5.837 | OH - ND2 | False / False |

*Distances use original CIF heavy atoms, not hydrogenated copies. E51-K66 minimum observed distance need not use charged side-chain atoms; the Tier0 functional-atom criterion is distinct. Closest atom names and exact distances are preserved in local_geometry_6.csv.*
<!-- TABLE S11 END -->

The smallest E51–K66 heavy-atom distance may involve backbone atoms or a noncharged side-chain atom and is not the Tier0 salt criterion. For example, the AF source's closest E51–K66 pair uses E51 backbone O and K66 CB; calling it a salt bridge would change the endpoint. Full local_pair_quality_crosswalk.csv joins the Primary local geometries to available experimental residue quality; prediction rows explicitly mark experimental fields unavailable.

### S5.4 Tier 0 functional-atom salt-bridge candidates

The all-observed-atom normalized screen accepts a unique interchain residue pair if a Lys NZ or Arg NE/NH1/NH2 atom lies strictly below 4.0 Å from Asp OD1/OD2 or Glu OE1/OE2. Histidine and artificial terminal OXT atoms are excluded from this criterion. A nearest qualifying atom pair is retained per residue pair. This differs from the earlier common-198 exploratory screen; final public Tier0/1 tables use the later all-observed-atom canonical results and retain the earlier algorithm only as historical source.

<!-- TABLE S12 START -->
**Table S12. All Tier0 functional-atom salt-bridge candidates**

| Structure | Cation residue / atom | Anion residue / atom | Distance (Å) |
| --- | --- | --- | --- |
| 9GIV | MPC2 LYS66 NZ | MPC1L GLU51 OE1 | 2.776624 |
| 9GIW | MPC2 LYS66 NZ | MPC1L GLU51 OE1 | 2.738296 |
| 9GIY | MPC1L ARG56 NH2 | MPC2 ASP59 OD1 | 3.002596 |
| 9GIY | MPC2 LYS66 NZ | MPC1L GLU51 OE2 | 2.941783 |

*Four observed structure/pair instances, two different residue-pair types. Successful Tier0 screens found zero qualifying functional-atom pairs in Boltz, AlphaFold and 9GIX under the fixed definition; this is not a thermodynamic absence statement.*
<!-- TABLE S12 END -->

### S5.5 Tier 1 typed heavy-atom proximity

Donors include backbone N except Pro; Asn ND2, Gln NE2; Lys/Arg side-chain N; Trp NE1; and eligible Ser/Thr/Tyr hydroxyl O. Acceptors include backbone carbonyl O; Asn/Gln carbonyl O; Asp/Glu carboxyl O; and eligible hydroxyl O. Peptide amide N is not an acceptor. Histidine, Cys thiol and ambiguous terminal groups are excluded from the fixed tally. A candidate requires an oriented donor-heavy/acceptor-heavy separation ≤3.0 Å. Roles can matter even for the same residue pair. Missing/untypeable sites are not treated as chemically absent.

<!-- TABLE S13 START -->
**Table S13. All Tier1 donor/acceptor heavy-atom proximity candidates**

| Structure | Donor residue / atom | Acceptor residue / atom | D-A (Å) |
| --- | --- | --- | --- |
| 9GIV | MPC1L SER54 OG | MPC2 ASP59 OD2 | 2.662178 |
| 9GIV | MPC2 LYS66 NZ | MPC1L GLU51 OE1 | 2.776624 |
| 9GIV | MPC2 SER68 OG | MPC1L ASP45 OD2 | 2.653029 |
| 9GIW | MPC1L SER54 OG | MPC2 ASP59 OD1 | 2.532334 |
| 9GIW | MPC2 ARG62 NH1 | MPC1L ILE52 O | 2.897561 |
| 9GIW | MPC2 ARG62 NH1 | MPC1L ILE53 O | 2.884672 |
| 9GIW | MPC2 ARG62 NH2 | MPC1L ILE53 O | 2.993032 |
| 9GIW | MPC2 LYS66 NZ | MPC1L GLU51 OE1 | 2.738296 |
| 9GIW | MPC2 SER68 OG | MPC1L ASP45 OD2 | 2.657492 |
| 9GIX | MPC2 TRP82 NE1 | MPC1L GLY31 O | 2.905028 |
| 9GIY | MPC2 LYS66 NZ | MPC1L GLU51 OE2 | 2.941783 |
| 9GIY | MPC2 SER68 OG | MPC1L ASP45 OD2 | 2.746334 |
| Boltz | MPC1L SER54 OG | MPC2 ASP59 OD1 | 2.724099 |
| Boltz | MPC1L SER54 OG | MPC2 ASP59 OD2 | 2.775107 |
| Boltz | MPC2 ARG62 NH2 | MPC1L GLU51 O | 2.841779 |
| Boltz | MPC2 SER68 OG | MPC1L ASP45 OD2 | 2.339384 |
| Boltz | MPC2 TRP82 NE1 | MPC1L SER35 OG | 2.837107 |
| AF | MPC1L SER54 OG | MPC2 ASP59 OD1 | 2.732439 |
| AF | MPC1L SER54 OG | MPC2 ASP59 OD2 | 2.856427 |
| AF | MPC2 ARG62 NH2 | MPC1L GLU51 O | 2.905682 |
| AF | MPC2 SER68 OG | MPC1L ASP45 OD2 | 2.560530 |

*All 21 atom-level candidates, representing eight different residue-pair types across structures. Criterion D-A ≤3.0 Å on all observed normalized protein atoms; no hydrogens or D-H-A angle is evaluated in Tier1. These are not demonstrated hydrogen bonds.*
<!-- TABLE S13 END -->

All 21 atom-level rows are printed. Counting unique residue-pair types across all inputs yields eight; this is distinct from the sum of per-structure residue-pair occurrences. The four AF atom-level rows comprise three AF residue pairs. Fresh replay checked candidate identities, thresholds and distances on the saved normalized PDBs; a 2e−5 Å distance tolerance accommodates the historical Biopython float32 representation without altering source coordinates or thresholds.

### S5.6 Conditional Tier 2 hydrogenated model and status

Historical Tier 2 used OpenMM 8.2 (recorded Windows build 8.2.0.dev-5377094), PDBFixer 1.12.0, amber14-all.xml and pH 7.0, with histidines represented as HIE. Asp/Glu and Lys/Arg followed force-field charge assumptions. Missing-residue insertion was disabled, no internal observed heavy atoms were rebuilt or minimized, and only required terminal OXT completion was permitted before adding hydrogens. Positive/negative distance-angle detector controls and per-structure original-heavy preservation were prerequisites.

The core candidate screen requires D–A≤3.0 Å and D–H–A≥150°, excluding artificial-terminus and histidine-involving contacts from the core tally. The angle is at H. Original-heavy displacement must be ≤1e−5 Å; a derived hydrogenated model is not an independent experimental observation of a hydrogen or protonation microstate.

<!-- TABLE S14a START -->
**Table S14a. All accepted Tier2 atom triplets**

| Structure | Donor / hydrogen | Acceptor | D-A (Å) | D-H-A (°) |
| --- | --- | --- | --- | --- |
| Boltz | MPC1L SER54 OG / HG | MPC2 ASP59 OD2 | 2.775107 | 154.550 |
| Boltz | MPC2 SER68 OG / HG | MPC1L ASP45 OD2 | 2.339384 | 167.895 |
| 9GIV | MPC2 LYS66 NZ / HZ2 | MPC1L GLU51 OE1 | 2.776619 | 164.644 |
| 9GIV | MPC2 SER68 OG / HG | MPC1L ASP45 OD2 | 2.653022 | 170.698 |
| AF | MPC2 SER68 OG / HG | MPC1L ASP45 OD2 | 2.560530 | 168.459 |

*All five atom triplets and all three residue-pair types. These counts are conditional on accepted historical protonation/hydrogen placement. No new OpenMM calculation was performed for this production.*
<!-- TABLE S14a END -->

<!-- TABLE S14b START -->
**Table S14b. Tier2 structure status and preservation gate**

| Structure | Screen status | Accepted triplets | Max original-heavy displacement (Å) |
| --- | --- | --- | --- |
| Boltz | PASS | 2 | 2.44813528e-06 |
| 9GIX | NOT RUN | NOT RUN | 1.38381991e-05 (diagnostic) |
| 9GIV | PASS | 2 | 7.94987302e-06 |
| 9GIW | NOT RUN | NOT RUN | 1.26287199e-05 (diagnostic) |
| 9GIY | NOT RUN | NOT RUN | 1.33283317e-05 (diagnostic) |
| AF | PASS | 1 | 2.7856017e-06 |

*Gate: original-heavy displacement ≤1e-5 Å. 9GIX/9GIW/9GIY exceeded the gate; their H-bond screens remain NOT RUN. Diagnostic displacement values do not restore screening eligibility. Counts are not zero for these rows.*
<!-- TABLE S14b END -->

The earlier API failure produced an empty triplet file; it is not the final canonical four-row Primary file. The final Primary/AF triplet files are preserved unchanged. For 9GIX, 9GIW and 9GIY, later diagnostic runs measured original-heavy displacements of about 1.38e−5, 1.26e−5 and 1.33e−5 Å, respectively, exceeding the fixed gate. Diagnostic completion did not authorize a threshold change or restore those H-bond screens. Their status remains NOT RUN, with no candidate count assigned.

Production checked all five accepted triplets against the saved rounded hydrogenated PDBs, allowing 0.002 Å in distance and 0.15° in angle for that export precision. This validates consistency of saved snapshots and printed triplets; it does not reproduce stochastic hydrogen placement, verify all unrounded displacement measurements anew, or prove a biological hydrogen-bond network. The historical per-structure gate records and diagnostic summary retain those verification limits.

## S6. Experimental structural quality

### S6.1 Source and meaning of quality fields

Saved wwPDB validation-derived scalar tables record entry resolution, reported contour, map-inclusion fields, residue Q-score, residue map inclusion, rotamer codes and source-coordinate B-factor summaries. Resolutions are 3.65 Å (9GIX), 3.65 Å (9GIV), 3.92 Å (9GIW) and 3.79 Å (9GIY). The entry-summary CSV retains EMDB identifiers and revision dates. The original reports are available through the linked RCSB entries [9]; report PDFs/XML are not copied into the public package.

Residue inclusion and Q-score are map-fit context rather than direct error bars on a particular interatomic distance. Source experimental B factors describe the deposited refinement/displacement field; prediction B-like fields may encode confidence and are not compared as equivalent physical quantities. Text rotamer codes are retained as reported rather than converted into a new good/bad classification. Exact map-input byte identity and cryo-EM refinement were not independently reproduced.

<!-- TABLE S15 START -->
**Table S15. Local experimental quality for interaction and coverage examples**

| PDB | Protein / residue | Q-score | Residue map inclusion | Mean source B (Å²) | Rotamer code |
| --- | --- | --- | --- | --- | --- |
| 9GIX | MPC1L ASP45 | 0.399 | 0.5000 | 132.072 | m-30 |
| 9GIX | MPC1L GLU51 | 0.249 | 0.4444 | 140.026 | tt0 |
| 9GIX | MPC1L SER54 | 0.371 | 0.8333 | 120.150 | p |
| 9GIX | MPC1L ARG56 | 0.504 | 0.7273 | 114.955 | mtm-85 |
| 9GIX | MPC2 ASP59 | 0.360 | 0.5000 | 107.725 | t70 |
| 9GIX | MPC2 LYS66 | 0.332 | 0.4444 | 121.777 | mmmt |
| 9GIX | MPC2 SER68 | 0.537 | 0.8333 | 107.960 | t |
| 9GIX | MPC2 ILE90 | 0.487 | 0.7500 | 60.501 | mp |
| 9GIV | MPC1L ASP45 | 0.541 | 0.8750 | 99.601 | m-30 |
| 9GIV | MPC1L GLU51 | 0.501 | 0.8889 | 103.913 | mm-30 |
| 9GIV | MPC1L SER54 | 0.493 | 0.8333 | 89.965 | t |
| 9GIV | MPC1L ARG56 | 0.524 | 0.9091 | 86.211 | mtt90 |
| 9GIV | MPC2 ASP59 | 0.559 | 1.0000 | 102.734 | m-30 |
| 9GIV | MPC2 LYS66 | 0.453 | 0.7778 | 110.609 | mttm |
| 9GIV | MPC2 SER68 | 0.464 | 0.6667 | 99.730 | t |
| 9GIV | MPC2 ILE90 | 0.459 | 0.6250 | 110.560 | mt |
| 9GIW | MPC1L ASP45 | 0.516 | 0.7500 | 163.004 | m-30 |
| 9GIW | MPC1L GLU51 | 0.328 | 0.5556 | 163.482 | mm-30 |
| 9GIW | MPC1L SER54 | 0.413 | 0.6667 | 124.810 | t |
| 9GIW | MPC1L ARG56 | 0.522 | 0.9091 | 120.154 | mpt180 |
| 9GIW | MPC2 ASP59 | 0.324 | 0.5000 | 160.930 | m-30 |
| 9GIW | MPC2 LYS66 | 0.342 | 0.6667 | 151.552 | mttm |
| 9GIW | MPC2 SER68 | 0.514 | 1.0000 | 118.533 | t |
| 9GIW | MPC2 ILE90 | 0.245 | 0.2500 | 197.550 | mt |
| 9GIY | MPC1L ASP45 | 0.319 | 0.5000 | 109.183 | m-30 |
| 9GIY | MPC1L GLU51 | 0.409 | 0.5556 | 105.993 | tt0 |
| 9GIY | MPC1L SER54 | 0.444 | 0.8333 | 90.523 | p |
| 9GIY | MPC1L ARG56 | 0.378 | 0.6364 | 85.611 | mtm-85 |
| 9GIY | MPC2 ASP59 | 0.409 | 0.7500 | 119.239 | m-30 |
| 9GIY | MPC2 LYS66 | 0.325 | 0.3333 | 127.338 | mttm |
| 9GIY | MPC2 SER68 | 0.471 | 0.6667 | 107.070 | t |
| 9GIY | MPC2 ILE90 | 0.371 | 0.3750 | 114.643 | mt |

*32 selected residue/structure rows supporting the local interpretation; the full 308-row residue-quality CSV and 25-row local-pair quality crosswalk are supplied. Raw wwPDB PDF/XML reports are linked, not redistributed. B is a source coordinate displacement/refinement field for experiment; prediction B-like confidence fields are not treated as experimental B factors.*
<!-- TABLE S15 END -->

### S6.2 Coverage of the printed quality selection

Table S15 prints every experimental occurrence of the seven residues in the distinct Tier 0/Tier 2 pairs (MPC1L D45, E51, S54, R56; MPC2 D59, K66, S68), plus MPC2 I90 as an additional local-quality example: 8 residues×4 references=32 rows. The complete 308-row quality table (77 sites×4 references) remains unchanged in residue_validation_with_model_B.csv, with all fields, source B ranges and atom counts. Each reference has all 73 interface sites plus four additional quality-context positions: MPC1L 86 and 105, and MPC2 50 and 91. The local-pair crosswalk supplies the five Primary pair geometries per structure and their paired quality fields. This separation prevents a repeated 308-row PDF table from obscuring the local observations while preserving every saved row in a machine-readable source.

## S7. Numerical verification, exceptions and corrections

### S7.1 Fresh verification versus historical execution

Fresh production checks on 3 November 2026 verified all 344 PACK-provenance records of A+B, including duplicate source mappings, against file size and SHA-256. The three PACKs contain 70, 138 and 99 unique evidence files, respectively, in addition to their provenance/readme files; they overlap across PACKs. This is not a new verification of every raw historical archive named in the 72-source global register. All supplied ZIPs passed CRC inspection.

The primary portable replay recalculated 70 Primary/control and 35 AF RMSDs from original coordinates. A separately written Cα parser and Horn quaternion/eigenvalue fit independently recalculated all 105 metrics with a tolerance of 1e−5 Å; its maximum absolute discrepancy was 2.2870594307278225e−14 Å. Rotation determinants, a known rigid transform, identity/order invariance and negative protein/residue mapping controls were checked. Matching arithmetic does not experimentally validate a prediction.

The deterministic replay also rebuilt the 73/62 masks, 480 contact rows and per-reference counts, all six structures' H1/H2/H3 proxies, 30 local pairs and the all-observed Tier0/1 candidates. Engine-specific verification is deliberately narrower: saved DockQ scalar/stdout comparison, FreeSASA arithmetic and radius-record inspection, and five accepted Tier2 triplets against rounded saved snapshots. No new DockQ, FreeSASA, OpenMM/PDBFixer or cryo-EM engine execution is asserted.

### S7.2 Exception ledger

- Historical short-window H1 PCA: FAIL; rejected for interpreting H1, with all ten failed sensitivity rows retained.
- Accepted H1 local-axis proxy: 9GIX MPC2 retains H1_NUMERIC_SENSITIVITY_GT5 (5.018945552639998°). It is not converted to an unqualified robustness PASS.
- Between-state H2/H3 bundle rotation: NOT QUALIFIED / NOT RUN; within-structure angles are a separate executed endpoint.
- Tier2 Boltz, 9GIV and AF: historically PASS at the per-structure preservation gate, five saved triplets total.
- Tier2 9GIX, 9GIW and 9GIY: NOT RUN; no zero or negative bonding result assigned.
- Initial Tier2 API exception and empty candidate file: superseded historical implementation attempt, not canonical final evidence.
- Source inference replay and controlled AF/Boltz comparison: unavailable, not claimed.

The machine-readable analysis_status.csv, historical quality JSONs and erratum retain these distinctions. The archive-code directory is explicitly historical and includes original hardcoded layouts; only the portable commands in the reproduction guide are asserted to have succeeded in the distribution environment.

### S7.3 Historical AF–9GIX 62-site correction

The historical Session B narrative reported 3.897919 Å for AF–9GIX on the 62-site mask. The original canonical 35-value CSV contains 3.8981798013974487 Å, correctly displayed as 3.898180 Å. Fresh coordinate recomputation matches the canonical value. This is a historical narrative transcription discrepancy, not a changed coordinate, mask or computation. It is recorded in verification/ERRATUM.md with an extracted original line and source hash. The original private historical report is not silently overwritten. This first public candidate uses the correct value throughout.

## S8. File manifest and reproduction guide

### S8.1 Locating a result and its source

The English README is the entry point. CLAIM_EVIDENCE_MAP.csv connects each major claim to the Technical Note/SI location, unchanged canonical data, fresh verification and source-coordinate/protocol evidence. SOURCE_MANIFEST.csv gives original source-pack and archive-member identities for selected public evidence; unchanged copies have matching original/public SHA-256. Curated numerical excerpts or JSONs are marked as transformations, not original files. RIGHTS_MANIFEST.csv and LICENSE_SCOPE.md distinguish the applicable material classes.

RELEASE_MANIFEST.json is the candidate's fixed-version correspondence record. It intentionally excludes self-hashing, a future public commit SHA and containing archive hashes from immutable self-referential assertions. Reserved Zenodo version DOI 10.5281/zenodo.23910491 is recorded as an identifier, not a public release. SHA256SUMS.txt lists all declared distribution files except itself. A separate outer release checksum identifies the two top-level PDFs and reproducibility ZIP. The actual GitHub release commit and tag remain pending; publication follows the non-circular release procedure and separate author approval.

### S8.2 Tested reproduction levels

Level 1 checks frozen file hashes, selected data-to-presentation cells and package links. Level 2 recalculates all 105 RMSDs, masks, contacts and selected deterministic auxiliary geometry. Level 3 inspects the saved outputs and accepted hydrogenated snapshots for third-party engines; it does not regenerate those engines' results. Prediction-generation replay and cryo-EM map processing are outside these levels. Dependencies and exact successful commands are in the README, requirements files and REPRODUCIBILITY_GUIDE.

Both editable Markdown sources, the ReportLab PDF builder, generated table data, Figure 1 generation code and font/dependency instructions are included. Figure 1 is supplied as a 300-dpi PNG and an SVG. A separate Figure PDF was unnecessary: this PDF build uses the PNG, and SVG already supports vector reuse. The Technical Note and SI PDFs are retained in the reproducibility ZIP as well as the Zenodo top level so that README document links work in a standalone extracted package; their byte identities are verified. This small intentional duplication avoids nonportable links to files outside the extracted root.

### S8.3 Table presentation decisions

All ten Primary/control chain comparisons are printed in Table S5. All 35 AF values are printed by splitting Table S6 into mask and chain subparts. Table S3a separates per-reference contact counts from mask-union definitions. All 30 local pairs, 21 Tier1 atom pairs and five accepted Tier2 triplets are printed. Table S14 is split into accepted triplets and a complete per-structure status table. No scientific result is removed by these splits.

For DockQ, the printed table contains four principal descriptors for all 15 comparisons; extra parsed fields remain in the two canonical CSVs. FreeSASA prints all six structures' areas and total atom coverage, while per-chain counts, translation differences and large per-atom radius audits remain in CSVs. H1 and H2/H3 tables retain principal angles/sensitivity; per-axis vectors, resultant lengths and detailed eigenvalue fields remain in their full CSVs. The experimental quality selection and full-table mapping are defined in S6.2. TABLE_PRESENTATION_DECISIONS.csv lists the exact files, retained row selectors and reasons for these choices.

### S8.4 Release and rights boundary

This is a locally assembled publication candidate, not a published GitHub/Zenodo record. Zenodo version DOI 10.5281/zenodo.23910491 has been reserved for the draft but is not yet published; public GitHub tag and commit are pending. The author has confirmed ownership/publication authority, funding and competing-interest declarations, affiliation, and the planned CC BY 4.0 / MIT rights split for original materials. These approvals do not constitute an external release. No model checkpoint, MSA, third-party article/SI or validation-report original is included. Experimental CIFs remain CC0; atlas and AFDB materials retain their upstream notices. The DOI reservation was performed by the author. GitHub repository creation, tagging and external publication remain separate actions requiring author instruction.
