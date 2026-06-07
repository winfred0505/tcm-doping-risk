import sys
from pathlib import Path
from PIL import Image

def main():
    img_path = Path("images/icon_sheet.png")
    if not img_path.exists():
        print("Error: images/icon_sheet.png not found!")
        sys.exit(1)
        
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    n = 6
    icons = ["icon_complex", "icon_label", "icon_process", "icon_mahuang", "icon_lotus", "icon_globe"]
    
    DARK_THRESHOLD = 45
    FADE_THRESHOLD = 80
    
    for i, name in enumerate(icons):
        x0 = i * (w // n)
        x1 = (i + 1) * (w // n) if i < n-1 else w
        col_w = x1 - x0
        sq = min(col_w, h)
        cx, cy = x0 + col_w // 2, h // 2
        crop = img.crop((cx - sq // 2, cy - sq // 2, cx + sq // 2, cy + sq // 2))
        crop = crop.resize((256, 256), Image.Resampling.LANCZOS)
        
        # Remove background (luminance threshold)
        data = crop.load()
        cw, ch = crop.size
        for y in range(ch):
            for x in range(cw):
                r, g, b, a = data[x, y]
                lum = r * 0.299 + g * 0.587 + b * 0.114
                if lum < DARK_THRESHOLD:
                    data[x, y] = (r, g, b, 0)
                elif lum < FADE_THRESHOLD:
                    ratio = (lum - DARK_THRESHOLD) / (FADE_THRESHOLD - DARK_THRESHOLD)
                    data[x, y] = (r, g, b, int(255 * ratio))
                    
        out_path = Path(f"images/{name}.png")
        crop.save(out_path)
        print(f"Cropped and removed bg for: {out_path.name}")

if __name__ == "__main__":
    main()
