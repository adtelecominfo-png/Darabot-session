from pathlib import Path
from PIL import Image

source = Path('/home/ubuntu/upload/f72b7a0b-bd69-429c-ad47-43eda0b6f88d.jpg')
out = Path('/home/ubuntu/Darabot-session/public/assets')
out.mkdir(parents=True, exist_ok=True)

image = Image.open(source).convert('RGB')
if image.width != image.height:
    size = min(image.size)
    left = (image.width - size) // 2
    top = (image.height - size) // 2
    image = image.crop((left, top, left + size, top + size))

image.save(out / 'daratech-og.jpg', quality=95, optimize=True, progressive=True)
for name, size in [('favicon-16.png', 16), ('favicon-32.png', 32), ('favicon-64.png', 64), ('apple-touch-icon.png', 180)]:
    image.resize((size, size), Image.Resampling.LANCZOS).save(out / name, optimize=True)
print(f'Prepared logo assets in {out}')
for path in sorted(out.iterdir()):
    print(path.name, path.stat().st_size)
