#!/usr/bin/env python3
"""
img2svg.py - Convert raster images (ICO, JPG, JPEG, PNG, HEIF, HEIC, BMP,
GIF, WEBP, TIFF) to SVG vector format.

Requirements:
    pip install vtracer pillow pillow-heif

Notes:
    Raster -> SVG conversion is a "tracing" process. Photographs will
    produce very large SVG files; line art, logos, and simple graphics
    work best. For best results, simplify/clean the image first.
    If the code editor gives an error or warning at line 110, it is likely because the code editor is on strict mode and does not recognize the vtracer module. You can ignore this warning, as the code will still run correctly if vtracer is installed in your Python environment.
"""

import sys
import argparse
import tempfile
from pathlib import Path

# --- Optional HEIF/HEIC support ---------------------------------------------
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_OK = True
except ImportError:
    HEIF_OK = False

# --- Image loading -----------------------------------------------------------
from PIL import Image

# --- Vector tracing ----------------------------------------------------------
try:
    import vtracer
    VTRACER_OK = True
except ImportError:
    vtracer = None
    VTRACER_OK = False


SUPPORTED_EXT = {
    ".ico", ".jpg", ".jpeg", ".png", ".heif", ".heic",
    ".bmp", ".gif", ".webp", ".tif", ".tiff",
}


def load_image_rgb(path: Path) -> Image.Image:
    """Open an image with PIL and return an RGB image.

    RGBA images are composited onto white so transparency doesn't
    become black when traced.
    """
    img = Image.open(path)
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        return bg
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def convert_to_svg(
    input_path,
    output_path=None,
    colormode="color",
    hierarchical="stacked",
    mode="spline",
    filter_speckle=4,
    color_precision=6,
    layer_difference=16,
    corner_threshold=60,
    length_threshold=4.0,
    max_iterations=10,
    splice_threshold=45,
    path_precision=8,
):
    """Convert a single raster image to SVG using vtracer."""
    if not VTRACER_OK:
        raise RuntimeError(
            "vtracer is not installed. Run: pip install vtracer"
        )

    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Input not found: {src}")

    ext = src.suffix.lower()
    if ext not in SUPPORTED_EXT:
        raise ValueError(f"Unsupported extension: {ext}")

    if ext in {".heif", ".heic"} and not HEIF_OK:
        raise RuntimeError(
            "HEIF/HEIC support requires pillow-heif. "
            "Run: pip install pillow-heif"
        )

    if output_path is None:
        out = src.with_suffix(".svg")
    else:
        out = Path(output_path)

    # Always normalize through PIL/PNG so vtracer gets a clean input,
    # regardless of source format (ICO, HEIC, etc.).
    with tempfile.TemporaryDirectory() as tmp:
        tmp_png = Path(tmp) / "input.png"
        img = load_image_rgb(src)
        img.save(tmp_png, "PNG")

        vtracer.convert_image_to_svg_py(
            str(tmp_png),
            str(out),
            colormode=colormode,
            hierarchical=hierarchical,
            mode=mode,
            filter_speckle=filter_speckle,
            color_precision=color_precision,
            layer_difference=layer_difference,
            corner_threshold=corner_threshold,
            length_threshold=length_threshold,
            max_iterations=max_iterations,
            splice_threshold=splice_threshold,
            path_precision=path_precision,
        )

    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="img2svg",
        description="Convert raster images (ICO/JPG/PNG/HEIF/...) to SVG.",
    )
    p.add_argument("input", nargs="+", help="Input image file(s).")
    p.add_argument(
        "-o", "--output",
        help="Output SVG path (only valid with a single input file).",
    )
    p.add_argument("--colormode", choices=["color", "binary"], default="color")
    p.add_argument("--hierarchical", choices=["stacked", "cutout"], default="stacked")
    p.add_argument("--mode", choices=["spline", "polygon", "none"], default="spline")
    p.add_argument("--filter-speckle", type=int, default=4,
                   help="Suppress speckles up to N pixels (default: 4).")
    p.add_argument("--color-precision", type=int, default=6,
                   help="Bits per channel for color quantization (default: 6).")
    p.add_argument("--layer-difference", type=int, default=16,
                   help="Color separation threshold (default: 16).")
    p.add_argument("--corner-threshold", type=int, default=60)
    p.add_argument("--length-threshold", type=float, default=4.0)
    p.add_argument("--max-iterations", type=int, default=10)
    p.add_argument("--splice-threshold", type=int, default=45)
    p.add_argument("--path-precision", type=int, default=8)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if not VTRACER_OK:
        print("ERROR: vtracer is not installed.\n"
              "       Install deps: pip install vtracer pillow pillow-heif",
              file=sys.stderr)
        return 2

    if not HEIF_OK:
        print("NOTE: pillow-heif not installed; HEIF/HEIC inputs will fail.\n"
              "      Install with: pip install pillow-heif",
              file=sys.stderr)

    if len(args.input) > 1 and args.output:
        print("ERROR: -o/--output can't be used with multiple inputs.",
              file=sys.stderr)
        return 2

    failures = 0
    for f in args.input:
        try:
            out = convert_to_svg(
                f,
                output_path=args.output if len(args.input) == 1 else None,
                colormode=args.colormode,
                hierarchical=args.hierarchical,
                mode=args.mode,
                filter_speckle=args.filter_speckle,
                color_precision=args.color_precision,
                layer_difference=args.layer_difference,
                corner_threshold=args.corner_threshold,
                length_threshold=args.length_threshold,
                max_iterations=args.max_iterations,
                splice_threshold=args.splice_threshold,
                path_precision=args.path_precision,
            )
            print(f"OK   {f}  ->  {out}")
        except Exception as e:
            print(f"FAIL {f}  :  {e}", file=sys.stderr)
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())