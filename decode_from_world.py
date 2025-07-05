from pathlib import Path
from amulet import load_level
import argparse

p = argparse.ArgumentParser(description="Decode a wool data plate from world file")
p.add_argument("--world", required=True, help="path to world folder")

args = p.parse_args()

WORLD_DIR = Path(args.world)

# Get first block
X0 = int(input("Top left X: "))
Y0 = int(input("Top left Y: "))
Z0 = int(input("Top left Z: "))

# Get dimension
dim_raw = input("Dimension [overworld/nether/end] (default = overworld): ").strip().lower()
DIM = {
    "":          "minecraft:overworld",   # Just hit enter
    "overworld": "minecraft:overworld",
    "nether":    "minecraft:the_nether",
    "end":       "minecraft:the_end",
}.get(dim_raw, "minecraft:overworld")     # Fallback

# Get width and height
W = int(input("Width (cols): "))
H = int(input("height (rows): "))

# Get step direction
# CSTEP 1 0 means positively move along X axis, and not at all along Z axis, RSTEP 0 1 means not at all along X axis, and positively along Z axis.
CSTEP = tuple(map(int, input("col step dX dZ [1 0]: ").split() or "1 0".split()))
RSTEP = tuple(map(int, input("row step dX dZ [0 1]: ").split() or "0 1".split()))

# Enter padding length of white wool blocks, as these will be ignored and prevent writing trailing null data
PAD = int(input("Padding (trailing white-wool blocks to ignore, 0 for none): ") or "0")


level = load_level(str(WORLD_DIR))

# Hex map for our wool colours
HEX2WOOL = {
    '0':'white_wool','1':'light_gray_wool','2':'gray_wool','3':'black_wool',
    '4':'brown_wool','5':'red_wool','6':'orange_wool','7':'yellow_wool',
    '8':'lime_wool','9':'green_wool','a':'cyan_wool','b':'light_blue_wool',
    'c':'blue_wool','d':'purple_wool','e':'magenta_wool','f':'pink_wool',
}

# Reverse map for quick lookup
WOOL2HEX  = {v:k for k,v in HEX2WOOL.items()}

def wool_hex(block):
    # Return the hex digit for a wool block, and works for both old and new styles of wool block
    print(block)
    base = block.base_name
    if base == "wool":
        colour = block.properties.get("color", "white")
        name   = f"{colour}_wool"
    else:
        name = base
    return WOOL2HEX[name]

# Prepare to collect hex characters
hexchars = []

# Iterate over the grid of blocks using user specified variables
for row in range(H):
    base_x = X0 + row*RSTEP[0]
    base_z = Z0 + row*RSTEP[1]
    for col in range(W):
        gx = base_x + col*CSTEP[0]
        gz = base_z + col*CSTEP[1]
        block = level.get_block(gx, Y0, gz, DIM)
        try:
            hexchars.append(wool_hex(block))
        # If the block is not a wool block, it will raise KeyError and print to the user so they can see what went wrong
        except KeyError:
            print(f"Stopped at ({gx},{Y},{gz}) → {block.namespace}:{block.base_name} {block.properties}")
            raise

# If padding is specified, remove the last PAD hex characters
if PAD != 0:
    hexchars = hexchars[:-PAD] 

# Write the hex characters to a binary file, this can be renamed by the user based on the expected file type
Path("decoded.bin").write_bytes(bytes.fromhex(''.join(hexchars)))
print("Wrote decoded.bin,", len(hexchars)//2, "bytes")
level.close()