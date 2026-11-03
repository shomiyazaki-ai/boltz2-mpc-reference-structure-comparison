# Third-party source attribution and changes

**Experimental structures:** Sichrovsky M, Lacabanne D, Ruprecht JJ, et al., Science Advances (2025), doi:10.1126/sciadv.adw1489. Original PDB entries 9GIX/9GIV/9GIW/9GIY under wwPDB CC0. Original CIFs are unchanged. Normalized PDBs select target chains, rename chains by protein identity and round coordinates; the accepted 9GIV hydrogenated copy adds force-field-assumed H and terminal OXT as documented.

**Atlas prediction:** Ille AM, Markosian C, Burley SK, Pasqualini R, Arap W., Human PPI Atlas; fixed commit dc55acabb3da7f233def7a0668d86e1c0ecb8e8e, interaction_structures/O95563_P0DKB6_Boltz-2_v2-1-1.cif. Copyright (c) 2025 structural-interactome, MIT notice in licenses/Atlas_MIT.txt. The original CIF is unchanged. Normalized export swaps the source letters to A=MPC1L/B=MPC2 and rounds to PDB precision; the separately marked H snapshot adds model-dependent H/OXT.

**AlphaFold-derived prediction:** AlphaFold Protein Structure Database / NVIDIA collaborator complex dataset, AF-0000000204012512 v1, https://alphafold.ebi.ac.uk/entry/AF-0000000204012512 . CC-BY-4.0 as declared in the frozen CIF and AFDB reuse terms. This file's source legal/disclaimer text is preserved as supplied; source rights-holder wording is not replaced with an inferred legal entity. Original CIF is unchanged. Normalized export maps A=MPC1L/B=MPC2, excludes non-target content if any and rounds to PDB precision; the DERIVED H model adds assumed H and terminal OXT. These changes do not imply provider endorsement.

**Prediction method literature:** Boltz-2: S. Passaro et al., bioRxiv 2025, https://doi.org/10.1101/2025.06.14.659707. AlphaFold-Multimer: R. Evans et al., bioRxiv 2021, https://doi.org/10.1101/2021.10.04.463034. These are method attributions; fixed model source identities remain the Atlas and AFDB/NVIDIA entries above.

**Software:** DockQ 2.1.3 (Mirabello and Wallner, 2024); FreeSASA 2.2.1 (Mitternacht, 2016); MDAnalysis HELANAL definition (Bansal et al., 2000; official MDAnalysis 2.9.0 documentation); OpenMM recorded 8.2.0.dev-5377094 with PDBFixer 1.12.0 for historic hydrogen placement. Package source, binaries and checkpoints are not bundled. See the Technical Note references and reproducibility scope.

**Fonts:** PDF font subsets use DejaVu Sans from Matplotlib's installed font distribution. License notice is in licenses/DejaVu_Font_License.txt. Figure and PDF generation use installed fonts; no raw TTF is redistributed.
