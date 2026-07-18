|img2svg Version 1.0 Release|
|---------------------------|

Patch notes:
  [Version 1.0.1]
    Fixed placeholder bug.
    Added Linux support for installer, works on 64 bit systems.

img2svg is a simple CLI (Command Line Interface) tool built for Windows and Linux operating systems.
img2svg is made for one task, to convert anyting to an svg file format.

|Usecases|
|--------|
img2svg [-h] [-o OUTPUT] [--colormode {color,binary}]
               [--hierarchical {stacked,cutout}]
               [--mode {spline,polygon,none}]
               [--filter-speckle FILTER_SPECKLE]
               [--color-precision COLOR_PRECISION]
               [--layer-difference LAYER_DIFFERENCE]
               [--corner-threshold CORNER_THRESHOLD]
               [--length-threshold LENGTH_THRESHOLD]
               [--max-iterations MAX_ITERATIONS]
               [--splice-threshold SPLICE_THRESHOLD]
               [--path-precision PATH_PRECISION]
               input [input ...]

