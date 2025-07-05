from pathlib import Path
from PIL import Image, ImageDraw
import math, argparse

# Hex to wool
HEX2WOOL = {
    '0': ('minecraft:white_wool',      (235,236,236)),
    '1': ('minecraft:light_gray_wool', (142,142,134)),
    '2': ('minecraft:gray_wool',       (62, 68, 71)),
    '3': ('minecraft:black_wool',      (29, 29, 33)),
    '4': ('minecraft:brown_wool',      (83, 51, 28)),
    '5': ('minecraft:red_wool',        (161, 39, 34)),
    '6': ('minecraft:orange_wool',     (240,118, 19)),
    '7': ('minecraft:yellow_wool',     (249,198, 40)),
    '8': ('minecraft:lime_wool',       (94, 168,24)),
    '9': ('minecraft:green_wool',      (55, 76, 25)),
    'a': ('minecraft:cyan_wool',       (21,137,145)),
    'b': ('minecraft:light_blue_wool', (58,175,217)),
    'c': ('minecraft:blue_wool',       (60, 68,170)),
    'd': ('minecraft:purple_wool',     (137, 50,184)),
    'e': ('minecraft:magenta_wool',    (199,88,198)),
    'f': ('minecraft:pink_wool',       (237,141,172)),
}
# Build a reverse palette. This ends up going mostly unused, though allows for the decoder to be integrated with the encoder in a single tool
RGB = {v[0]: v[1] for v in HEX2WOOL.values()}
WOOL2HEX = {name: h for h,(name,_) in HEX2WOOL.items()}

def nearest_hex(rgb):
    # Tiny Euclidean distance in RGB
    r,g,b = rgb
    def dist(c): return (c[0]-r)**2 + (c[1]-g)**2 + (c[2]-b)**2
    wool_name = min(RGB, key=lambda n: dist(RGB[n]))
    return WOOL2HEX[wool_name]

# Parse columns and setblock Y level for automated block placement
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--cols', type=int, default=64)
parser.add_argument('--y', type=int, default=64, help='Y level for setblock')
args = parser.parse_args()

# Reading bytes from file to a hex string
data = Path(args.file).read_bytes().hex()
cols = args.cols
rows = math.ceil(len(data)/cols)
print(f'Encoding {len(data)//2} bytes as {rows}×{cols} wool blocks')

# Creating an image to show the placement of wool blocks
img = Image.new('RGB', (cols, rows))
draw = ImageDraw.Draw(img)
for idx, char in enumerate(data):
    x, y = idx % cols, idx // cols
    draw.point((x, y), HEX2WOOL[char][1])
img = img.resize((cols*8, rows*8), Image.NEAREST)  # scale for visibility
img.save('layout.png')

# Building the mcfunction file to set wool blocks
with open('build.mcfunction', 'w') as f:
    for idx, char in enumerate(data):
        x, z = idx % cols, idx // cols
        block = HEX2WOOL[char][0]
        f.write(f'setblock ~{x} {args.y} ~{z} {block}\n')
print('layout.png and build.mcfunction written.')