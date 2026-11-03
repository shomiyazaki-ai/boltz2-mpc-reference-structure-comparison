<!-- TABLE T1 START -->
**Table 1. Structures and conditions**

| Input | Source identifier | State | Condition | Role |
| --- | --- | --- | --- | --- |
| Boltz-2 | O95563_P0DKB6_Boltz-2_v2-1-1 | Not assigned | Protein-only fixed model | Primary A |
| 9GIX | PDB 9GIX | Inward-open | Apo | Experimental reference |
| 9GIV | PDB 9GIV | Outward-open | C7 (UK5099 derivative) | Experimental reference |
| 9GIW | PDB 9GIW | Outward-open | Zaprinast | Experimental reference |
| 9GIY | PDB 9GIY | Outward-open | Mitoglitazone | Experimental reference |
| AlphaFold | AF-0000000204012512-model_v1 | Not assigned | Protein-only fixed model | Exploratory B |

*State labels describe experimental conditions from Sichrovsky et al. [1]. No state is assigned to either prediction by this table. Boltz-2 source: Atlas row 147, version 2.1.1. AlphaFold source: AFDB/NVIDIA entry v1, AF-Multimer 2.3.0 weights.*
<!-- TABLE T1 END -->

<!-- TABLE T2 START -->
**Table 2. Principal structural comparisons**

| Comparison group | Source vs target | 73-residue RMSD (Å) |
| --- | --- | --- |
| Primary A | Boltz-2 vs 9GIX | 3.853976 |
| Primary A | Boltz-2 vs 9GIV | 0.964115 |
| Primary A | Boltz-2 vs 9GIW | 1.217374 |
| Primary A | Boltz-2 vs 9GIY | 1.077057 |
| Experimental control | 9GIX vs 9GIV | 3.879390 |
| Experimental control | 9GIX vs 9GIW | 3.848898 |
| Experimental control | 9GIX vs 9GIY | 3.769616 |
| Experimental control | 9GIV vs 9GIW | 0.605305 |
| Experimental control | 9GIV vs 9GIY | 0.572130 |
| Experimental control | 9GIW vs 9GIY | 0.510085 |
| Exploratory B | AlphaFold vs 9GIX | 4.045460 |
| Exploratory B | AlphaFold vs 9GIV | 1.794373 |
| Exploratory B | AlphaFold vs 9GIW | 1.966428 |
| Exploratory B | AlphaFold vs 9GIY | 1.837599 |

*All 14 comparisons use the same two-chain 73-Cα fit and evaluation set. Source/target direction identifies saved fits; the same-mask optimum RMSD is symmetric. These rows are not statistical replicates.*
<!-- TABLE T2 END -->

<!-- TABLE T3 START -->
**Table 3. Mask sensitivity of the fixed Boltz-2 structure**

| Reference | 73 residues (Å) | 62 residues (Å) | 198 residues (Å) |
| --- | --- | --- | --- |
| 9GIX | 3.853976 | 3.727117 | 4.478252 |
| 9GIV | 0.964115 | 0.804675 | 1.482408 |
| 9GIW | 1.217374 | 0.948745 | 1.662196 |
| 9GIY | 1.077057 | 0.872235 | 1.638168 |

*Each column is fitted and evaluated on its own indicated Cα set. Thresholds defining the masks are strictly <5 Å and <4 Å; the 198-residue set is sequence-common coverage.*
<!-- TABLE T3 END -->

<!-- TABLE T4 START -->
**Table 4. Chain-specific and cross-chain alignment: fixed Boltz-2**

| Reference | Fit/evaluate MPC1L (Å) | Fit/evaluate MPC2 (Å) | Fit MPC1L; evaluate MPC2 (Å) | Fit MPC2; evaluate MPC1L (Å) |
| --- | --- | --- | --- | --- |
| 9GIX | 0.858598 | 4.172290 | 8.303083 | 6.251804 |
| 9GIV | 1.189383 | 1.503577 | 1.941535 | 1.689469 |
| 9GIW | 1.469730 | 1.499637 | 2.264895 | 2.135073 |
| 9GIY | 1.260680 | 1.641993 | 2.261337 | 1.879886 |

*MPC1L: 84 Cα sites; MPC2: 114. Cross-chain evaluation applies the fitted transform without a second fit. It includes internal shape differences and relative arrangement; it is not a pure translation or a single rigid-body displacement.*
<!-- TABLE T4 END -->

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
