"""
Foto scontornate 'a sticker' per i caroselli Makhymo in stile ritaglio.

Le foto sorgente (assets/photos/<serie>/src/*.jpg) sono generate su fondo verde pieno
(chroma key). Qui il verde diventa trasparenza, il soggetto passa in bianco e nero con un
po' di contrasto e grana, e intorno si aggiunge il bordo bianco da adesivo con un'ombra
morbida. Uscita: assets/photos/<serie>/cut/*.png in scala di grigi + alfa (LA).

Per risparmiare crediti:
  1. prima si cerca nella libreria dei ritagli gia' fatti (assets/photos/libreria.jpg,
     rigenerata con `python3 make_stickers.py libreria`): nei caroselli si richiamano con
     mky_sticker.lib("serie", "nome");
  2. gli oggetti che mancano si generano 4 alla volta in una sola immagine 2x2 su fondo verde.
     Il file sorgente elenca i nomi con '+', in ordine di lettura (alto-sx, alto-dx, basso-sx,
     basso-dx): src/10_scrivania+11_lampada+12_pianta+13_cestino.jpg -> quattro ritagli.
     Ogni pezzo va al riquadro in cui cade il suo baricentro, quindi un oggetto fatto di
     parti staccate (poltrona + tavolino) resta intero se sta nel suo quarto.

Uso: python3 make_stickers.py barcode
     python3 make_stickers.py libreria
"""

import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import (binary_dilation, binary_fill_holes, binary_opening,
                           distance_transform_edt, gaussian_filter, label)

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_SIDE = 1100          # lato massimo del soggetto (px) nella PNG finale
BORDER = 22              # spessore del bordo bianco (px, alla scala finale)
SHADOW = (10, 14, 16)    # ombra: dx, dy, sfocatura (px)
# soggetti "pieni": tutto cio' che sta dentro il profilo e' soggetto, anche se verde
# (es. uno schermo che mostra piante: senza questo il chroma key bucherebbe l'immagine a video)
FILL_HOLES = {"08_schermo"}


def key_green(rgb, fill=False):
    """Alfa dal chroma key verde + rimozione dell'alone verde sui bordi.
    fill=True: i vuoti chiusi dentro il profilo restano pieni e con il loro colore."""
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
    if fill:
        inside = binary_fill_holes(solid) & ~solid
        alpha = np.where(inside, 1.0, alpha)
        g2 = np.where(inside, g, g2)
    return np.dstack([r, g2, b]), alpha


def to_bw(rgb, rng):
    lum = 0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
    lo, hi = np.percentile(lum, 1.5), np.percentile(lum, 99.5)
    x = np.clip((lum - lo) / max(hi - lo, 1), 0, 1)
    x = x + 0.12 * np.sin(2 * np.pi * x) / (2 * np.pi) * 2      # leggera curva a S
    x = np.clip(x, 0, 1) * 255
    x += gaussian_filter(rng.normal(0, 1, x.shape), 0.6) * 5   # grana
    return np.clip(x, 0, 255)


GRID_COLS = 2            # le griglie sono sempre su 2 colonne (2 oggetti = 1 riga, 4 = 2x2)


def grid_split(alpha, n, cols=GRID_COLS):
    """Maschere dei singoli oggetti di una griglia: ogni pezzo (dopo una piccola dilatazione,
    per tenere unite le parti vicine) va al riquadro che contiene il suo baricentro."""
    rows = -(-n // cols)
    H, W = alpha.shape
    lab, k = label(binary_dilation(alpha > 0.05, iterations=12))
    masks = [np.zeros_like(alpha, dtype=bool) for _ in range(n)]
    for i in range(1, k + 1):
        comp = lab == i
        ys, xs = np.nonzero(comp)
        r = min(int(ys.mean() / (H / rows)), rows - 1)
        c = min(int(xs.mean() / (W / cols)), cols - 1)
        cell = r * cols + c
        if cell < n:
            masks[cell] |= comp
    empty = [i for i, m in enumerate(masks) if not (m & (alpha > 0.5)).any()]
    if empty:
        raise ValueError(f"riquadri senza oggetto: {empty} (controlla l'immagine o i nomi)")
    return masks


def sticker(src, dst, seed=0, fill=False):
    rng = np.random.default_rng(seed)
    im = Image.open(src).convert("RGB")
    rgb = np.asarray(im).astype(float)
    rgb, alpha = key_green(rgb, fill)
    return _sticker_from(rgb, alpha, dst, rng)


def sticker_grid(src, dsts, seed=0, fill=False):
    """Una sorgente con piu' oggetti -> un ritaglio per oggetto (dsts in ordine di lettura)."""
    im = Image.open(src).convert("RGB")
    rgb, alpha = key_green(np.asarray(im).astype(float), fill)
    out = []
    for j, (dst, m) in enumerate(zip(dsts, grid_split(alpha, len(dsts)))):
        out.append(_sticker_from(rgb, alpha * m, dst, np.random.default_rng(seed * 10 + j)))
    return out


def _sticker_from(rgb, alpha, dst, rng):
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
        names = os.path.splitext(f)[0].split("+")
        dsts = [os.path.join(cut_dir, n + ".png") for n in names]
        fill = any(n in FILL_HOLES for n in names)
        if len(names) == 1:
            results = [sticker(os.path.join(src_dir, f), dsts[0], seed=i, fill=fill)]
        else:
            results = sticker_grid(os.path.join(src_dir, f), dsts, seed=i, fill=fill)
        for p, size, pad in results:
            print(p, size, f"{os.path.getsize(p) // 1024} KB")


def libreria(cell=300, cols=8):
    """Foglio con tutti i ritagli gia' pronti (serie/nome), per scegliere cosa riusare."""
    from PIL import ImageDraw, ImageFont
    root = os.path.join(HERE, "assets", "photos")
    items = []
    for series in sorted(os.listdir(root)):
        cut = os.path.join(root, series, "cut")
        if os.path.isdir(cut):
            items += [(series, f) for f in sorted(os.listdir(cut)) if f.endswith(".png")]
    rows = -(-len(items) // cols)
    font = ImageFont.truetype(os.path.join(HERE, "assets", "fonts", "LexendDeca-Medium.ttf"), 17)
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 34)), (18, 37, 73))
    draw = ImageDraw.Draw(sheet)
    for i, (series, f) in enumerate(items):
        im = Image.open(os.path.join(root, series, "cut", f)).convert("RGBA")
        im.thumbnail((cell - 24, cell - 24))
        x0, y0 = (i % cols) * cell, (i // cols) * (cell + 34)
        sheet.paste(im, (x0 + (cell - im.width) // 2, y0 + (cell - im.height) // 2), im)
        label_txt = f"{series}/{os.path.splitext(f)[0]}"
        tw = draw.textlength(label_txt, font=font)
        draw.text((x0 + (cell - tw) / 2, y0 + cell + 4), label_txt, font=font, fill=(242, 207, 155))
    dst = os.path.join(root, "libreria.jpg")
    sheet.save(dst, quality=86)
    print(dst, f"{len(items)} ritagli")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "barcode"
    libreria() if arg == "libreria" else main(arg)
