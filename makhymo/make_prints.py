"""
Foto vere 'a stampa' per i caroselli Makhymo in stile ritaglio.

Le foto scattate sul campo (assets/photos/<serie>/foto/*.jpg) non si possono scontornare come gli
oggetti su fondo verde: diventano stampe fotografiche in bianco e nero (stesso trattamento dei
ritagli: contrasto e grana), con bordo bianco, leggera rotazione e ombra morbida.
Prima del taglio si sfocano le zone indicate (scritte, marchi o numeri di terzi).
Uscita: assets/photos/<serie>/print/*.png in scala di grigi + alfa (LA).

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


def make_print(src, dst, crop, blur=(), rotate=0, seed=0):
    rng = np.random.default_rng(seed)
    im = Image.open(src).convert("RGB")
    for box in blur:
        region = im.crop(box).filter(ImageFilter.GaussianBlur(18))
        im.paste(region, box[:2])
    im = im.crop(crop)
    k = MAX_SIDE / max(im.size)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    bw = to_bw(np.asarray(im).astype(float), rng)
    # stampa: foto dentro un bordo bianco
    h, w = bw.shape
    lum = np.full((h + 2 * FRAME, w + 2 * FRAME), 250.0)
    lum[FRAME:FRAME + h, FRAME:FRAME + w] = bw
    pl = Image.fromarray(lum.astype("uint8"), "L")
    pa = Image.new("L", pl.size, 255)
    # rotazione con margine per l'ombra
    pl = pl.rotate(rotate, Image.BICUBIC, expand=True, fillcolor=0)
    pa = pa.rotate(rotate, Image.BICUBIC, expand=True, fillcolor=0)
    pad = SHADOW[2] * 2 + max(SHADOW[:2]) + 4
    H, W = pl.height + 2 * pad, pl.width + 2 * pad
    a = np.zeros((H, W))
    a[pad:pad + pl.height, pad:pad + pl.width] = np.asarray(pa) / 255.0
    l = np.zeros((H, W))
    l[pad:pad + pl.height, pad:pad + pl.width] = np.asarray(pl)
    dx, dy, s = SHADOW
    sh = np.zeros((H, W))
    sh[dy:, dx:] = a[:H - dy, :W - dx]
    sh = gaussian_filter(sh, s) * 0.42
    out_a = a + sh * (1 - a)
    out_l = np.where(out_a > 0, l * a / np.maximum(out_a, 1e-6), 0)
    out = np.dstack([np.clip(out_l, 0, 255), np.clip(out_a * 255, 0, 255)]).astype("uint8")
    Image.fromarray(out, "LA").save(dst, optimize=True)
    return dst, (W, H)


def main(series):
    base = os.path.join(HERE, "assets", "photos", series)
    out_dir = os.path.join(base, "print")
    os.makedirs(out_dir, exist_ok=True)
    for i, (name, spec) in enumerate(PRINTS[series].items()):
        dst = os.path.join(out_dir, name + ".png")
        p, size = make_print(os.path.join(base, "foto", name + ".jpg"), dst, seed=i, **spec)
        print(p, size, f"{os.path.getsize(p) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "finevita")
