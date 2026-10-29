"""Extracao dos pontos da curva de linearizacao a partir da figura.

Le 'Figuras/linearizacao.png' (../Figuras relativo a este script), detecta as
gridlines tracejadas para calibrar os eixos e os marcadores pretos (flood
fill) dentro da area do grafico, e imprime as coordenadas X, Y de cada ponto.
Artefatos temporarios de apoio vao para /tmp (markers.npy, calib.txt).

Uso:  python3 extrair_pontos_linearizacao.py
Saida: lista de pontos no terminal + /tmp/markers.npy + /tmp/calib.txt
"""

from pathlib import Path

import numpy as np
from PIL import Image

IMAGEM_FONTE = Path(__file__).resolve().parent.parent / "Figuras" / "linearizacao.png"

img = np.array(Image.open(IMAGEM_FONTE).convert("RGB")).astype(int)
H, W, _ = img.shape
print("size", W, H)
gray = img.mean(axis=2)

# --- Calibragem via gridlines tracejadas cinzas ---
# gridlines: pixels quase cinza (R~G~B) e claros mas nao brancos
r, g, b = img[...,0], img[...,1], img[...,2]
grayish = (abs(r-g)<8) & (abs(g-b)<8) & (gray>150) & (gray<235)

colfrac = grayish.mean(axis=0)
rowfrac = grayish.mean(axis=1)

def peaks(frac, min_val, min_dist):
    idx = np.where(frac > min_val)[0]
    groups = []
    if len(idx):
        start = idx[0]; prev = idx[0]
        for i in idx[1:]:
            if i - prev > 3:
                groups.append((start+prev)//2); start = i
            prev = i
        groups.append((start+prev)//2)
    # merge close
    out = []
    for p in groups:
        if out and p - out[-1] < min_dist:
            out[-1] = (out[-1]+p)//2
        else:
            out.append(p)
    return out

vlines = peaks(colfrac, 0.25, 50)   # gridlines verticais X=0..6
hlines = peaks(rowfrac, 0.25, 50)   # gridlines horizontais Y=0..7
print("vlines px:", vlines, "hlines px:", hlines)

vx = np.array(vlines[0:7], float); xvals = np.arange(0, 7, dtype=float)   # X=0..6
hy = np.array(hlines[0:8], float); yvals = np.arange(7, -1, -1, dtype=float)  # Y=7..0 (topo->base)
ax, bx = np.polyfit(vx, xvals, 1)   # X = ax*px + bx
ay, by = np.polyfit(hy, yvals, 1)   # Y = ay*py + by
print("X = %.8f*px + %.4f" % (ax, bx))
print("Y = %.8f*py + %.4f" % (ay, by))

# plot area bounds from gridlines
x0px = -bx/ax          # X=0
x6px = (6-bx)/ax       # X=6
y0px = -by/ay          # Y=0
y7px = (7-by)/ay       # Y=7
print("plot px bounds: x[%.1f, %.1f] y[%.1f, %.1f]" % (x0px, x6px, y7px, y0px))

# --- Deteccao de componentes pretos (flood fill) ---
black = gray < 60
visited = np.zeros_like(black, bool)
comps = []
for yy in range(45, 845):
    for xx in np.where(black[yy] & ~visited[yy])[0]:
        if visited[yy, xx] or not black[yy, xx]:
            continue
        q = [(yy, xx)]; visited[yy, xx] = True
        pts = []
        while q:
            cy, cx = q.pop()
            pts.append((cy, cx))
            for ny in (cy-1, cy, cy+1):
                for nx in (cx-1, cx, cx+1):
                    if 0 <= ny < H and 0 <= nx < W and black[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True; q.append((ny, nx))
        comps.append(pts)

markers = []
for pts_ in comps:
    n = len(pts_)
    if n < 50 or n > 2000:
        continue
    ys = np.array([p[0] for p in pts_]); xs = np.array([p[1] for p in pts_])
    h = ys.max()-ys.min()+1; w = xs.max()-xs.min()+1
    fill = n/(h*w)
    cx, cy = xs.mean(), ys.mean()
    if cx < x0px+10 or cx > x6px-5 or cy < y7px+5 or cy > y0px-10:
        continue
    if cx < 340 and cy < 220:
        continue  # marcador da legenda
    if 0.5 < w/h < 2.0 and fill > 0.6:
        markers.append((cx, cy, n, w, h, fill))

markers.sort(key=lambda m: m[0])
print("found", len(markers))
for m in markers:
    cx, cy = m[0], m[1]
    print("px(%7.1f,%7.1f) n=%4d w=%2d h=%2d fill=%.2f -> X=%.3f Y=%.3f" %
          (cx, cy, m[2], m[3], m[4], m[5], ax*cx+bx, ay*cy+by))

np.save("/tmp/markers.npy", np.array([(m[0],m[1]) for m in markers]))
with open("/tmp/calib.txt","w") as f:
    f.write(f"{ax} {bx} {ay} {by} {x0px} {x6px} {y0px} {y7px}")
