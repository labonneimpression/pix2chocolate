# pix2chocolate
Render a low-relief chocolate from any image. This is especially useful for previewing a chocolate in an e-commerce flow.
For now, the chocolate chip model is a "Petit écolier"-like chocolate biscuit. This might help us save the world.

## Technical stack
- Inkscape is used to save a PNG heightmap from an SVG file.
- Blender 2.79 + Micro-displacement + GPU optimizations (the aim is to provide fast previews to future web or offline users)
- Tiny SH shell script - for Linux systems.
- Tiny analogous Python shell script - for Linux systems.

## Usage
Run `sh pix2chocolate.sh` (will use the LaBonneImpression logo).
Or provide an image of any time as first parameter: `sh pix2chocolate.sh smiley.png`.
(You can also use `python3 pix2chocolate.py` the same way).

## Example (Milestone 1) - single chocolate biscuit
1. Create a PNG heightmap (eg. greyscale image) by hand
![Image of Logo heightmap](https://github.com/labonneimpression/pix2chocolate/raw/master/LaBonneImpressionLogoHeightmapExample.png)
1. Run the `pix2chocolate.sh LaBonneImpressionLogoHeightmap.svg` script and observe console output like
```
...
Fra:1 Mem:104.49M (0.00M, Peak 108.99M) | Time:00:00.81 | Mem:74.38M, Peak:76.63M | Scene, RenderLayer | Path Tracing Tile 4/4
Fra:1 Mem:104.49M (0.00M, Peak 108.99M) | Time:00:00.81 | Mem:74.38M, Peak:76.63M | Scene, RenderLayer | Finished
Caching exr file, 357x270, /tmp/cached_RR_micro_displacement_test_Scene_f0b7e108e061b458286561a131417733.exr
Fra:1 Mem:77.84M (0.00M, Peak 108.99M) | Time:00:00.81 | Sce: Scene Ve:0 Fa:0 La:0
Saved: 'test0001.png'
 Time: 00:00.85 (Saving: 00:00.03)


Blender quit
1.09user 0.38system 0:01.09elapsed 136%CPU (0avgtext+0avgdata 299916maxresident)k
0inputs+4008outputs (0major+75356minor)pagefaults 0swaps
```
1. Observe the resulting image named test0001.png

![Image of Logo chocolate](https://github.com/labonneimpression/pix2chocolate/raw/master/test0001.png)

## Example 2 (out of roadmap) - multiple letter chocolate biscuits
Using [cli_example_multiletters.py](cli_example_multiletters.py) with the virtual-environment packages of [requirements.txt](requirements.txt), you can generate `Happy Birthday!` chocolate biscuit renderings. That script makes use of the command-line `pix2chocolate` tool.

See final result below:
![chocolate biscuit letter](generated/letter0001.png)
![chocolate biscuit letter](generated/letter0002.png)
![chocolate biscuit letter](generated/letter0003.png)
![chocolate biscuit letter](generated/letter0004.png)
![chocolate biscuit letter](generated/letter0005.png)
![chocolate biscuit letter](generated/letter0006.png)
![chocolate biscuit letter](generated/letter0007.png)
![chocolate biscuit letter](generated/letter0008.png)
![chocolate biscuit letter](generated/letter0009.png)
![chocolate biscuit letter](generated/letter0010.png)
![chocolate biscuit letter](generated/letter0011.png)
![chocolate biscuit letter](generated/letter0012.png)
![chocolate biscuit letter](generated/letter0013.png)
![chocolate biscuit letter](generated/letter0014.png)
![chocolate biscuit letter](generated/letter0015.png)

## Example 3 - multiple letter chocolate biscuits 
This example uses the G'MIC Python binding for post-processing the biscuit result with an engrave filter.

Usage:
```sh
python cli_example_multiletters.py --text="abc" --output-dir="alphabet" --gmic_command="fx_engrave 0.5,50,0,8,40,0,0,0,10,1,0,0,0,1,0"
```

See final result:
![chocolate biscuit letter](alphabet/letter0001.png)
![chocolate biscuit letter](alphabet/letter0002.png)
![chocolate biscuit letter](alphabet/letter0003.png)
![chocolate biscuit letter engraved](alphabet/letter_gmic0001.png)
![chocolate biscuit letter engraved](alphabet/letter_gmic0002.png)
![chocolate biscuit letter engraved](alphabet/letter_gmic0003.png)



## Milestones
1. Drop heightmap SVG file in directory, run manually Blender rendering, show chocolate render offline
1. Drop any image (logo (vector or raster), face, landscape, object), for logos (or low-color solid backgrounded images only) run auto-crop/center/rotate manually, generate heightmap generation manually, run manually Blender rendering, show chocolate render offline
1. (current) Drop an image, run 1 command only for the last step, show chocolate render offline
1. Same as before, but do a 3d rendering preview of multiple images on one circle path (ie. camera rotation only on the X-Y plan) (see [CloudImage](https://github.com/scaleflex/js-cloudimage-360-view))
1. In a different project:
    1. wrap this with an encrypted REST API,
    1. wrap this REST API with JS web form.
    1. generate and store 3d models for offline mold-making

## Installing
Download everything (ie. the [master.zip archive of the main branch](https://github.com/labonneimpression/pix2chocolate/archive/master.zip)).
Install [Blender 2.79 or maybe 2.8](https://www.blender.org/download/previous-versions/).
(Optionally) install imagemagick if you want to pass files instead of use the LaBonneImpression logo.
If you are not using Linux, you might want to alter the SH script first for your OS.
