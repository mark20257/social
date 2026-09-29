"""
Foto scontornate 'a sticker' per i caroselli Makhymo in stile ritaglio.

Le foto sorgente (assets/photos/<serie>/src/*.jpg) sono generate su fondo verde pieno
(chroma key). Qui il verde diventa trasparenza, il soggetto passa in bianco e nero con un
po' di contrasto e grana, e intorno si aggiunge il bordo bianco da adesivo con un'ombra
morbida. Uscita: assets/photos/<serie>/cut/*.png in scala di grigi + alfa (LA).

Uso: python3 make_stickers.py barcode
"""

import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import (binary_fill_holes, binary_opening, distance_transform_edt,
                           gaussian_filter, label)

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_SIDE = 1100          # lato massimo del soggetto (px) nella PNG finale
BORDER = 22              # spessore del bordo bianco (px, alla scala finale)
SHADOW = (10, 14, 16)    # ombra: dx, dy, sfocatura (px)


def key_green(rgb):
    """Alfa dal chroma key verde + rimozione dell'alone verde sui bordi."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    greenness = g - np.maximum(r, b)
    alpha = np.clip((115 - greenness) / (115 - 45), 0, 1)
    # pulizia: via puntini isolati, tieni le componenti grandi
    solid = alpha > 0.5
    solid = binary_opening(solid, iterations=2)
    lab, n = label(solid)
    if n > 1:
        sizes = np.bincount(lab.ravel())
        sizes[0] = 0
        keep = sizes >= sizes.max() * 0.02
        solid = keep[lab]
    alpha = np.where(solid | (alpha < 0.5), alpha, 0) * (gaussian_filter(solid.astype(float), 1.5) > 0.02)
    g2 = np.minimum(g, np.maximum(r, b))                       # despill
    return np.dstack([r, g2, b]), alpha


def to_bw(rgb, rng):
    lum = 0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
    lo, hi = np.percentile(lum, 1.5), np.percentile(lum, 99.5)
    x = np.clip((lum - lo) / max(hi - lo, 1), 0, 1)
    x = x + 0.12 * np.sin(2 * np.pi * x) / (2 * np.pi) * 2      # leggera curva a S
    x = np.clip(x, 0, 1) * 255
    x += gaussian_filter(rng.normal(0, 1, x.shape), 0.6) * 5   # grana
    return np.clip(x, 0, 255)


def sticker(src, dst, seed=0):
    rng = np.random.default_rng(seed)
    im = Image.open(src).convert("RGB")
    rgb = np.asarray(im).astype(float)
    rgb, alpha = key_green(rgb)
    ys, xs = np.where(alpha > 0.05)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb, alpha = rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
    # scala finale
    k = MAX_SIDE / max(rgb.shape[:2])
    size = (round(rgb.shape[1] * k), round(rgb.shape[0] * k))
    rgb = np.asarray(Image.fromarray(rgb.astype("uint8")).resize(size, Image.LANCZOS)).astype(float)
    alpha = np.asarray(Image.fromarray((alpha * 255).astype("uint8")).resize(size, Image.LANCZOS)) / 255.0
    bw = to_bw(rgb, rng)
    # tela con margine per bordo e ombra
    pad = BORDER + SHADOW[2] * 2 + max(SHADOW[:2]) + 4
    h, w = alpha.shape
    H, W = h + 2 * pad, w + 2 * pad
    a = np.zeros((H, W))
    a[pad:pad + h, pad:pad + w] = alpha
    lum = np.zeros((H, W))
    lum[pad:pad + h, pad:pad + w] = bw
    # bordo bianco solo attorno al profilo esterno: i vuoti interni (rete di una sedia,
    # anse di un manico) restano trasparenti come nella foto
    filled = binary_fill_holes(a > 0.5)
    dist = distance_transform_edt(~filled)
    border = np.clip(BORDER + 0.5 - dist, 0, 1) * (~filled)
    border = np.maximum(border, a)
    # ombra morbida del bordo
    sh = np.zeros((H, W))
    dx, dy, blur = SHADOW
    sh[dy:, dx:] = border[:H - dy, :W - dx]
    sh = gaussian_filter(sh, blur) * 0.42
    # composizione: ombra (nera) -> bordo (bianco) -> soggetto
    out_a = border + sh * (1 - border)
    out_l = np.where(out_a > 0, (255 * border * (1 - a) + lum * a) / np.maximum(out_a, 1e-6), 0)
    out = np.dstack([np.clip(out_l, 0, 255), np.clip(out_a * 255, 0, 255)]).astype("uint8")
    Image.fromarray(out, "LA").save(dst, optimize=True)
    return dst, (W, H), pad


def main(series):
    base = os.path.join(HERE, "assets", "photos", series)
    src_dir, cut_dir = os.path.join(base, "src"), os.path.join(base, "cut")
    os.makedirs(cut_dir, exist_ok=True)
    for i, f in enumerate(sorted(os.listdir(src_dir))):
        if not f.lower().endswith((".jpg", ".png")):
            continue
        dst = os.path.join(cut_dir, os.path.splitext(f)[0] + ".png")
        p, size, pad = sticker(os.path.join(src_dir, f), dst, seed=i)
        print(p, size, f"{os.path.getsize(p) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "barcode")
