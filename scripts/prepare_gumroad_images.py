from pathlib import Path
from PIL import Image
import shutil

src = Path("/home/hermes/Projects/passive-income-lab/assets/listing/payday-reset-pack-v1.0")
out = Path(__file__).resolve().parents[1] / "public/gumroad/payday-reset-pack"
out.mkdir(parents=True, exist_ok=True)
for number in range(1, 7):
    shutil.copy2(src / f"{number:02d}.jpg", out / f"{number:02d}.jpg")
hero = Image.open(src / "01.jpg").convert("RGB")
hero.thumbnail((1160, 920), Image.Resampling.LANCZOS)
canvas = Image.new("RGB", (1200, 1200), "#F7F2E9")
canvas.paste(hero, ((1200 - hero.width) // 2, (1200 - hero.height) // 2))
canvas.save(out / "thumbnail.jpg", quality=92, subsampling=0, optimize=True)
print([(path.name, path.stat().st_size) for path in sorted(out.glob("*.jpg"))])
