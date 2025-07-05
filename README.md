# Encode files to Minecraft

This program has been written for an XDA article.

This program encodes files to Minecraft, representing them as wool blocks. You can encode a file with encoder.py, and then decode it with decode_from_world.py. It can encode any file, though a 67 byte file will take up 144 blocks. The encoder will generate an mcfunction file which can be run to automatically place the blocks. 

This program requires `amulet` to be installed, as well as `Pillow` for image creation of layout.png. You can install these with pip.

## Usage

Run the encoder with the following command:

```bash
python encoder.py <file> --cols x --y y
```

* `File` is the file to encode.
* `--cols` is the number of columns to use. This is the number of blocks in a row.
* `--y` is the y coordinate to place the blocks at. This is the height of the blocks in the world.

Run the decoder with the following command:

```bash
python decode_from_world.py --world <world>
```

You will then be asked to specify the following:

* Top left X
* Top left Y
* Top left Z
* Dimension [overworld/nether/end] (default = overworld)
* Width (cols)
* Height (rows)
* Col step dX dZ [1 0]
* Row step dX dZ [0 1]
* Padding (trailing white-wool blocks to ignore, 0 for none)

By default, the decoder will assume that the blocks are placed in the overworld by default, and that reading from left to right and top to bottom will increase the X and Z coordinates respectively. If you have placed the blocks in a different dimension, or if you have placed them in a different order, you can specify this with the options above.

