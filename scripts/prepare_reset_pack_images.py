from pathlib import Path
import argparse
from PIL import Image

parser=argparse.ArgumentParser(description="Prepare approved reset-pack listing images for the storefront")
parser.add_argument("source_dir",type=Path)
args=parser.parse_args()
out=Path(__file__).resolve().parents[1]/"public"/"images"/"reset-pack"; out.mkdir(parents=True,exist_ok=True)
for number,name in [(1,"hero"),(2,"five-jobs"),(4,"two-payday"),(5,"irregular-and-shifts")]:
    im=Image.open(args.source_dir/f"{number:02d}.jpg").convert("RGB")
    im.thumbnail((1600,1200),Image.Resampling.LANCZOS)
    path=out/f"{name}.webp"; im.save(path,"WEBP",quality=84,method=6)
    print(path,im.size,path.stat().st_size)
