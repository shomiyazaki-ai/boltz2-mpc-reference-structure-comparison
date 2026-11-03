# Non-circular release identity and publication procedure (version 1.0.0)

The version 1.0.0 payload identifies Zenodo version DOI `10.5281/zenodo.23910491`, GitHub repository `shomiyazaki-ai/boltz2-mpc-reference-structure-comparison`, and release tag `v1.0.0`. The DOI was initially reserved by the author in the Zenodo draft. This file is a procedural record and **does not assert that external publication has occurred**.

1. Confirm author-approved research scope, rights, data/figures, references and file checksums.
2. Build both PDFs from the editable Markdown sources; build `RELEASE_MANIFEST.json` over payload files excluding itself, `SHA256SUMS.txt`, and outer archives/receipts. Include the DOI but **do not include the SHA of the containing Git commit**.
3. Build `SHA256SUMS.txt` over all payload files plus manifest, excluding the checksum file itself. Reproduce numeric outputs and check all 105 RMSDs by two distinct paths, auxiliary analyses, table cells and links.
4. Commit and push the approved repository files, then create/fix tag `v1.0.0` to the precise commit. Compare the remote Git tree against the sealed payload. No files within the tag should be changed after fixation.
5. Package the exact tagged payload as the Zenodo reproducibility ZIP. Compute external SHA256 values for the Technical Note PDF, SI PDF and ZIP, and supply those three lines as a fourth file. Files included twice (top-level PDFs and within the ZIP) must match byte-for-byte.
6. In the existing Zenodo record with version DOI `10.5281/zenodo.23910491`, replace the previously uploaded four draft files with the verified final four. Independently compare the previewed file hashes and metadata against the local artifacts. Do **not** make a duplicate draft or reserve another DOI.
7. Record the real Git commit SHA, tag, DOI, and top-level archive checksums in a separate external release receipt. This receipt must not be inserted into its own sealed payload.
8. Public repository visibility and Zenodo Publish are separate author-authorized steps. Confirm all identity and file checks first. Once both are public, verify DOI resolution, Git tag target, and file accessibility.

The stored `RELEASE_MANIFEST.json` identifies the distribution's intended fixed payload and does not encode a mutable claim about current external publication status. Historical QC and staging logs may preserve their dated pre-publication statements as historical facts, rather than current status declarations.
