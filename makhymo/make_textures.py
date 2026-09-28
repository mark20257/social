"""
Texture raster per i caroselli Makhymo (generate, non fotografiche).

  assets/bg_navy.jpg      carta navy stropicciata, 1080x1350 (fondo di tutte le slide)
  assets/bg_cover.jpg     navy + striscia kraft strappata in basso (copertina)
  assets/bg_contatti.jpg  navy + fascia kraft strappata in basso (CTA finale)
  assets/bg_scene.jpg     parete navy con luce morbida e pannello caldo sfocato a destra
                          (fondo delle slide 'a scena': tavolo, oggetto, fumetto)

Le sfaccettature della carta sono una superficie triangolata con altezze casuali,
illuminata dall'alto a sinistra: e' la stessa geometria di un foglio accartocciato
e poi steso. Seed fisso, quindi i file sono riproducibili.
"""

import os

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.spatial import Delaunay

W, H = 1080, 1350
S = 2                                   # supersampling: si lavora a 2160x2700
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

NAVY = np.array([18, 37, 73], float)     # #122549
KRAFT = np.array([233, 208, 181], float)


def _facets(w, h, n, amp, rng):
    """Altezza a facce piane su una triangolazione di Delaunay di n punti casuali."""
    pts = np.column_stack([rng.uniform(-0.1, 1.1, n) * w, rng.uniform(-0.1, 1.1, n) * h])
    corners = np.array([[-w, -h], [2 * w, -h], [-w, 2 * h], [2 * w, 2 * h]], float)
    pts = np.vstack([pts, corners])
    z = rng.normal(0, amp, len(pts))
    tri = Delaunay(pts)
    yy, xx = np.mgrid[0:h, 0:w]
    q = np.column_stack([xx.ravel() + 0.5, yy.ravel() + 0.5])
    simp = tri.find_simplex(q)
    T = tri.transform[simp]
    b = np.einsum("nij,nj->ni", T[:, :2], q - T[:, 2])
    bary = np.column_stack([b, 1 - b.sum(1)])
    verts = tri.simplices[simp]
    return (z[verts] * bary).sum(1).reshape(h, w)


def _shade(height, light=(-0.55, -0.7, 0.45)):
    gy, gx = np.gradient(height)
    nx, ny, nz = -gx, -gy, np.ones_like(gx)
    norm = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    lx, ly, lz = np.array(light) / np.linalg.norm(light)
    return (nx * lx + ny * ly + nz * lz) / norm


def navy_paper(seed=11, w=W * S, h=H * S):
    rng = np.random.default_rng(seed)
    height = (_facets(w, h, 70, 150, rng)           # pieghe grandi
              + _facets(w, h, 260, 38, rng)          # pieghe medie
              + _facets(w, h, 900, 7, rng))          # grinze fini
    height = gaussian_filter(height, 1.2 * S)
    sh = _shade(height)
    sh = (sh - np.median(sh)) / (sh.std() + 1e-6)
    sh = np.clip(sh, -2.8, 2.8)
    # vignettatura leggera e grana
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.10 * (((xx / w - 0.5) ** 2 + (yy / h - 0.45) ** 2) / 0.5)
    grain = gaussian_filter(rng.normal(0, 1, (h, w)), 0.8) * 0.6
    k = 1 + 0.055 * sh + 0.012 * grain
    img = NAVY[None, None, :] * (k * vig)[..., None]
    return np.clip(img, 0, 255)


def _torn_edge(w, base_y, rng, amp_big=38, amp_small=1.3):
    """Profilo di uno strappo: onda lenta + irregolarita' a piu' scale. Ritorna y(x) in pixel."""
    x = np.arange(w)
    y = np.full(w, float(base_y))
    for f, a in ((1.1, amp_big), (2.7, amp_big * 0.45), (6.3, amp_big * 0.22)):
        y += a * np.sin(2 * np.pi * f * x / w + rng.uniform(0, 6.28))
    for sig, a in ((14, 4.0), (5, 2.0), (2.4, amp_small)):
        n = gaussian_filter(rng.normal(0, 1, w), sig * S)
        y += a * S * n / (n.std() + 1e-6)
    return y


def kraft_strip(bg, top_profile, rng, rim=16):
    """Incolla sul fondo una carta kraft dal profilo `top_profile` fino al bordo inferiore."""
    h, w, _ = bg.shape
    yy = np.mgrid[0:h, 0:w][0].astype(float)
    top = top_profile[None, :]
    d = yy - top                                    # >0 dentro la carta
    # ombra portata sul navy, solo in una fascia sopra lo strappo
    shadow = np.clip(1 - (-d) / (34 * S), 0, 1) * (d < 0)
    shadow = gaussian_filter(shadow, 5 * S)
    bg = bg * (1 - 0.45 * shadow)[..., None]
    # carta: fibre orientate + macchie morbide + grana
    fib = gaussian_filter(rng.normal(0, 1, (h, w)), (1.4 * S, 3.5 * S))
    blot = gaussian_filter(rng.normal(0, 1, (h, w)), 45 * S)
    mott = gaussian_filter(rng.normal(0, 1, (h, w)), 7 * S)
    grain = gaussian_filter(rng.normal(0, 1, (h, w)), 0.8 * S)
    tone = (1 + 0.02 * fib / (fib.std() + 1e-6) + 0.03 * blot / (blot.std() + 1e-6)
            + 0.018 * grain / (grain.std() + 1e-6) + 0.022 * mott / (mott.std() + 1e-6))
    paper = KRAFT[None, None, :] * tone[..., None]
    # fascia chiara dello strappo: larghezza variabile, bordo interno sfilacciato
    wv = gaussian_filter(rng.normal(0, 1, w), 18 * S)
    rimw = rim * S * (1 + 0.55 * wv / (wv.std() + 1e-6))[None, :]
    rimw = np.clip(rimw, 5 * S, None)
    fuzz = gaussian_filter(rng.normal(0, 1, (h, w)), (0.8 * S, 2.5 * S))
    fuzz = fuzz / (fuzz.std() + 1e-6)
    edge = np.clip((rimw + 3.5 * S * fuzz - d) / (3 * S), 0, 1) * (d >= 0)
    light = np.array([247, 239, 228], float)
    paper = paper * (1 - edge[..., None] * 0.85) + light[None, None, :] * (edge[..., None] * 0.85)
    # leggera ombra interna sotto la fascia chiara
    inner = np.clip((d - rimw) / (10 * S), 0, 1) * np.clip(1 - (d - rimw) / (70 * S), 0, 1)
    paper = paper * (1 - 0.07 * inner[..., None])
    # contorno antialias
    alpha = np.clip((d + 1.0 * S) / (2.0 * S), 0, 1)
    return bg * (1 - alpha[..., None]) + paper * alpha[..., None]


def scene_wall(base, seed=3):
    """
    Parete per le slide a scena, come uno sfondo fotografico fuori fuoco:
    texture ammorbidita, luce morbida da sinistra, pannello kraft molto sfocato a destra.
    """
    h, w, _ = base.shape
    soft = np.stack([gaussian_filter(base[..., c], 2.5 * S) for c in range(3)], -1)
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    light = np.exp(-(((xx - 0.30 * w) / (0.60 * w)) ** 2 + ((yy - 0.38 * h) / (0.50 * h)) ** 2))
    img = soft * (0.86 + 0.26 * light)[..., None]
    panel = np.zeros((h, w))
    panel[: int(0.62 * h), int(0.84 * w):] = 1.0
    panel = gaussian_filter(panel, 70 * S)
    panel *= np.clip(1.15 - yy / (0.75 * h), 0, 1)            # sfuma verso il basso
    warm = np.array([222, 190, 150], float)
    a = (0.62 * panel / panel.max())[..., None]
    return img * (1 - a) + warm[None, None, :] * a


def _save(arr, name, q=90):
    im = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    im = im.resize((W, H), Image.LANCZOS)
    p = os.path.join(ASSETS, name)
    im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
    return p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    base = navy_paper()
    print(_save(base, "bg_navy.jpg"))
    print(_save(scene_wall(base), "bg_scene.jpg"))

    rng = np.random.default_rng(5)
    # copertina: strappo che sale verso destra, come nella cover di riferimento
    prof = _torn_edge(W * S, 0, rng, amp_big=14 * S)
    ramp = np.interp(np.arange(W * S), [0, 0.45 * W * S, 0.62 * W * S, W * S],
                     [980 * S, 940 * S, 860 * S, 840 * S])
    print(_save(kraft_strip(base.copy(), prof + ramp, rng), "bg_cover.jpg"))

    rng = np.random.default_rng(9)
    prof = _torn_edge(W * S, 1150 * S, rng, amp_big=10 * S)
    print(_save(kraft_strip(base.copy(), prof, rng), "bg_contatti.jpg"))


if __name__ == "__main__":
    main()
