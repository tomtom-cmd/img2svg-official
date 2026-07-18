# img2svg

`img2svg` is a powerful, lightweight Command Line Interface (CLI) tool engineered for Windows and Linux. It is designed with a singular, hyper-focused purpose: to flawlessly convert standard images into scalable vector graphics (SVG) with pixel-perfect control.

---

## Features
* **Cross-Platform:** Full compatibility with 64-bit Windows and Linux architectures.
* **Granular Extraction:** Fine-tune image color mapping, edge curves, path precision, and speckle noise reduction.
* **Zero Dependencies for End Users:** Compiled binaries mean your users don't need Python installed to run it.

---

## Installation

### Linux (Ubuntu/Debian/Kali)
Download the latest `.deb` installer from the [Releases](https://github.com) page and run:
```bash
sudo apt install ./img2svg_1.0.1_amd64.deb
```
*Note: This automatically creates a global system link. You can invoke the tool anywhere using either `img2svg` or the rapid `i2s` shorthand alias.*

### Windows
1. Download the `setup.ps1` installer or executable from the [Releases](https://github.com) archive.
2. Run the installer to automatically configure your environment `%PATH%` variables.

---

## Usage & CLI Arguments

### Basic Conversion
```bash
img2svg input_image.png -o output_vector.svg
```

### Advanced Customization Options

| Argument | Description | Default / Options |
| :--- | :--- | :--- |
| `input` | Path to the source input image(s) | *Required* |
| `-o`, `--output` | Explicit target path for the output `.svg` | *Optional* |
| `--colormode` | Select tracing palette strategy | `color`, `binary` |
| `--hierarchical` | Controls layering behavior for transparent areas | `stacked`, `cutout` |
| `--mode` | Specifies vector edge generation algorithms | `spline`, `polygon`, `none` |

### Fine-Tuning Flags
* `--filter-speckle` : Eliminates small background noise artifacts and dust dots.
* `--color-precision` : Controls how aggressively distinct shades are grouped together.
* `--layer-difference` : Alters threshold overlap limits between vector color sheets.
* `--corner-threshold` : Determines how sharp edges must be to prevent rounding.
* `--path-precision` : Sets decimal placement accuracy for output path data coordinates.
* `--max-iterations` : Caps recursive optimization math loops for speed vs accuracy.

To view the exhaustive list of flags and internal adjustments directly inside your shell terminal, execute:
```bash
img2svg -h
```

---

## Development & Building from Source

If you want to clone this repository and build the executables or installer packages yourself:

1. Clone the project and install requirements:
   ```bash
   git clone https://github.com
   cd img2svg-official
   pip install -r requirements.txt
   ```
2. To compile into a single native binary file:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile img2svg.py
   ```
3. To package the Linux binary into the automated system `.deb` installer distribution, run your internal build script:
   ```bash
   python3 build_deb.py dist/img2svg
   ```

---

## Release Notes

### [Version 1.0.1]
* **Fixed:** Resolved placeholder input parsing bug.
* **Added:** Implemented native Linux installer build pipelines tailored for 64-bit environments.
