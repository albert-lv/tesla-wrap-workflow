# Failure Modes and Safeguards

| Symptom | Unreliable handling | Correct safeguard |
|---|---|---|
| 07, 11, or fossil head upside down on the car | Rotate the whole canvas 180° | Locate the UV island, distinguish rotation vs. mirroring, verify against the mapping |
| Flat preview upright but side panel upside down on the car | Only view the flattened texture | Accept based on the actual on-car viewing angle; mark unverified when not tested |
| Lower half of image missing | Force-decode the truncated file or pad with white | Re-encode from the complete source; check IEND/CRC/full decode and the final file |
| Generation alters the template | Assume a prompt saying "keep the template" is enough | Compare against original boundaries and blank areas; use precise mask compositing when needed |
| Fossil head clipped by a wheel arch | Only check overall composition | Reserve panel safe zones for orientation-sensitive subjects |
| Theme badge disappears during logo removal | Delete every logo indiscriminately | Distinguish the Tesla T emblem/wordmark from themed artwork |
| File exceeds 1 MB | Estimate size by resolution | Check final bytes, optimize encoding, inspect compressed quality |
| Valid locally but corrupt inside the ZIP | Only test files before packaging | Re-read files inside the ZIP, fully decode, compare hashes |
| Delivery link broken | Reference old temp paths or nonexistent files | Deliver through the current tool's save flow; read back to verify when possible |
| One fix changes the overall style | Regenerate the whole image unconstrained | Keep the source image, constrain the edit region, compare the change scope |

These symptoms only prove an observed problem — they do not prove the root cause is encoding, transmission, or the model. Gather evidence first, then attribute the cause.

## Acceptance Record Template

- File / theme / version:
- Vehicle model, variant, template URL and retrieval date:
- Dimensions / bytes / SHA256:
- PNG and ZIP validation results:
- Template boundary and blank-area check method and results:
- Panel orientation evidence and unverified items:
- Real in-car testing: completed / not completed
- Post-save read-back: completed / unavailable

## Production checks added after an end-to-end trial

- A raw image requested at 1024 x 1024 arrived at 1254 x 1254 and over 1 MB. Requested settings are not acceptance evidence; validate the actual export.
- The official template contained hidden white and black RGB in pixels with zero alpha. Inspecting only the displayed image misidentified them as a border or background. Read alpha first.
- Generated transparency contained stray pixels and changed edges. Full PNG decoding cannot detect this. Compare the candidate alpha against the original template after compression.
- Matching alpha does not prove that paint fills every island correctly. Inspect internal dark slivers, subject cropping, and missing content separately, using light and dark preview backgrounds where supported.
- Avoid repeated whole-image regeneration just to fix export defects. Keep the approved artwork; use the permitted technical export path and repeat the relevant checks.

Run the checker regression cases with `python scripts/test_validate_template.py`. They exercise missing small islands, stray translucent pixels, changed antialiasing, opaque output, dimension mismatch, and unsupported opaque references. The tests do not establish on-car orientation.
