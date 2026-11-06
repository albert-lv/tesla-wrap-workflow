# Example wraps

[English README](../README.md) · [简体中文](../README.zh-CN.md)

These are complete PNG texture examples produced with this workflow, not photos or physical vinyl cutting patterns. They use the **Model Y (2025+) Premium** UV template. Do not assume the Standard, Performance, original Model Y, or Model Y L uses the same layout.

| Design | Download | Dimensions | File size |
| --- | --- | --- | --- |
| Jade Sword Array — a cultivation-fantasy design with jade clouds and a radial sword motif | [PNG](FanRen_JadeSword_Y25.png?raw=true) | 1024 × 1024 | 725,919 bytes |
| Midnight Pumpkin Parade — Halloween direction revision | [PNG](Halloween_Pumpkin_Y25_v2.png?raw=true) | 1024 × 1024 | 831,588 bytes |

Both omit Tesla logos and use original generated artwork. The fantasy illustration is inspired by cultivation fiction; no film stills or official character artwork are included.

## Validation

- PNG signature, chunk CRCs, final IEND, full decoding, dimensions, and the 1,000,000-byte limit: passed.
- Alpha compared against the original official template after export: 0 changed pixels for both images.
- Artwork: visually checked for complete panel coverage, separated islands, clipped motifs, and unwanted logos.
- Actual in-car mapping: **not tested**. These checks do not identify your exact trim or guarantee the vehicle preview.

The Jade Sword Array uses a radial motif and flowing cloud textures. The Halloween revision corrects the former flat-sheet-upright layout: the hood composition is rotated 180° for a front-of-car viewer; left-side motif tops point right on the atlas; right-side motif tops point left. These are template-specific visual checks against [Tesla's Rudi example](https://github.com/teslamotors/custom-wraps/blob/master/modely-2025-premium/example/Rudi.png) and [Doge example](https://github.com/teslamotors/custom-wraps/blob/master/modely-2025-premium/example/Doge.png), not a universal rotation rule or a substitute for checking on the vehicle. The previous Halloween PNG with the reported direction problem is not included.

## Reproduce the file checks

Download the unmodified [official Premium template](https://github.com/teslamotors/custom-wraps/blob/master/modely-2025-premium/template.png) as `template.png` outside the example folder. From the repository root:

```bash
python scripts/validate_wrap.py examples/FanRen_JadeSword_Y25.png --width 1024 --height 1024 --max-bytes 1000000
python scripts/validate_wrap.py examples/Halloween_Pumpkin_Y25_v2.png --width 1024 --height 1024 --max-bytes 1000000
python scripts/validate_template.py --template template.png --candidate examples/FanRen_JadeSword_Y25.png
python scripts/validate_template.py --template template.png --candidate examples/Halloween_Pumpkin_Y25_v2.png
```

Template SHA256: `336a738ffa7b11eaa4909fcaacc6d9066b38f9a06feba1fddf9634554f27e3b5`.

Tesla's reference files are linked for provenance; they are not bundled here. The repository is not an official Tesla project.
