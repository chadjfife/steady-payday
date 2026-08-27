from pathlib import Path
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="Prepare storefront WebP images from approved listing art")
parser.add_argument("source_dir", type=Path, help="Directory containing approved 01.jpg, 03.jpg, and 04.jpg listing images")
args = parser.parse_args()
source_dir = args.source_dir
out = Path(__file__).resolve().parents[1] / "public" / "images"
out.mkdir(parents=True, exist_ok=True)
items = [
    (source_dir / "01.jpg", "planner-hero.webp", (1600, 1200)),
    (source_dir / "03.jpg", "dashboard-closeup.webp", (1600, 1200)),
    (source_dir / "04.jpg", "connected-workflow.webp", (1600, 1200)),
    (Path("/tmp/payday-map.png"), "free-payday-map.webp", (900, 1200)),
]
for source, name, bounds in items:
    image = Image.open(source).convert("RGB")
    image.thumbnail(bounds, Image.Resampling.LANCZOS)
    target = out / name
    image.save(target, "WEBP", quality=84, method=6)
    print(name, image.size, target.stat().st_size)
