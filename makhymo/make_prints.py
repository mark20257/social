"""
Foto vere 'a stampa' per i caroselli Makhymo in stile ritaglio.

Le foto scattate sul campo (assets/photos/<serie>/foto/*.jpg) non si possono scontornare come gli
oggetti su fondo verde: diventano stampe fotografiche con bordo bianco, leggera rotazione e ombra
morbida. Le serie in COLOR restano a colori (foto del cliente); le altre passano in bianco e nero
con lo stesso trattamento dei ritagli (contrasto e grana).
Prima del taglio si sfocano le zone indicate (scritte, marchi o numeri di terzi).
Uscita: assets/photos/<serie>/print/*.png, RGBA a colori oppure scala di grigi + alfa (LA).

Uso: python3 make_prints.py finevita
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

from make_stickers import MAX_SIDE, SHADOW, to_bw
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME = 24               # bordo bianco della stampa (px, alla scala finale)

COLOR = {"finevita"}     # foto fornite dal cliente: si tengono a colori

# serie -> foto -> taglio (x0, y0, x1, y1), zone da sfocare (coordinate della foto originale),
# rotazione in gradi
PRINTS = {
    "finevita": {
        # scritte e telefono del trasportatore sul camion: sfocati o fuori dal taglio
        "22_pinza_aperta_pila": dict(crop=(90, 0, 1200, 1450), blur=[(95, 570, 300, 710)], rotate=-3),
        "16_gru_cassone": dict(crop=(0, 150, 1200, 1170), rotate=2),
        "23_piazzale": dict(crop=(0, 330, 1200, 1480), rotate=-2),
        "12_pinza_stringe": dict(crop=(340, 120, 1200, 1350), rotate=2),
        "10_stampante_schiacciata": dict(crop=(330, 460, 1200, 1450), rotate=-2),
    },
}


def make_print(src, dst, crop, blur=(), rotate=0, seed=0, color=False):
    rng = np.random.default_rng(seed)
    im = Image.open(src).convert("RGB")
    for box in blur:
        region = im.crop(box).filter(ImageFilter.GaussianBlur(18))
        im.paste(region, box[:2])
    im = im.crop(crop)
    k = MAX_SIDE / max(im.size)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    rgb = np.asarray(im).astype(float)
    photo = rgb if color else to_bw(rgb, rng)[..., None]
    # stampa: foto dentro un bordo bianco
    h, w = photo.shape[:2]
    ch = photo.shape[2]
    img = np.full((h + 2 * FRAME, w + 2 * FRAME, ch), 250.0)
    img[FRAME:FRAME + h, FRAME:FRAME + w] = photo
    mode = "RGB" if color else "L"
    pi = Image.fromarray(img.astype("uint8") if color else img[..., 0].astype("uint8"), mode)
    pa = Image.new("L", pi.size, 255)
    # rotazione con margine per l'ombra
    pi = pi.rotate(rotate, Image.BICUBIC, expand=True, fillcolor=0)
    pa = pa.rotate(rotate, Image.BICUBIC, expand=True, fillcolor=0)
    pad = SHADOW[2] * 2 + max(SHADOW[:2]) + 4
    H, W = pi.height + 2 * pad, pi.width + 2 * pad
    a = np.zeros((H, W))
    a[pad:pad + pi.height, pad:pad + pi.width] = np.asarray(pa) / 255.0
    c = np.zeros((H, W, ch))
    c[pad:pad + pi.height, pad:pad + pi.width] = np.asarray(pi).reshape(pi.height, pi.width, ch)
    dx, dy, s = SHADOW
    sh = np.zeros((H, W))
    sh[dy:, dx:] = a[:H - dy, :W - dx]
    sh = gaussian_filter(sh, s) * 0.42
    out_a = a + sh * (1 - a)
    out_c = np.where(out_a[..., None] > 0, c * a[..., None] / np.maximum(out_a, 1e-6)[..., None], 0)
    out = np.dstack([np.clip(out_c, 0, 255), np.clip(out_a * 255, 0, 255)]).astype("uint8")
    Image.fromarray(out, "RGBA" if color else "LA").save(dst, optimize=True)
    return dst, (W, H)


def main(series):
    base = os.path.join(HERE, "assets", "photos", series)
    out_dir = os.path.join(base, "print")
    os.makedirs(out_dir, exist_ok=True)
    for i, (name, spec) in enumerate(PRINTS[series].items()):
        dst = os.path.join(out_dir, name + ".png")
        p, size = make_print(os.path.join(base, "foto", name + ".jpg"), dst, seed=i,
                             color=series in COLOR, **spec)
        print(p, size, f"{os.path.getsize(p) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "finevita")
