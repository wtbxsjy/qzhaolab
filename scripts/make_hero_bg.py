"""Generate an original crowded-cell style background (protein blobs + peptide bead chains).

Usage: python make_hero_bg.py OUT.svg [seed]
Flat fills with darker outlines, in the spirit of molecular landscape illustrations.
"""
import math
import random
import sys

W, H = 1600, 900
out = sys.argv[1]
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)

# palette families: (fill, outline)
TEAL = [("#2f8f8a", "#1d5f5c"), ("#3fa79a", "#226b63"), ("#57b8a6", "#2c7568")]
BLUE = [("#3b6fb6", "#244a80"), ("#4f86c9", "#2c5a94"), ("#6a9bd8", "#3a68a3"), ("#2d5596", "#1b3666")]
GREEN = [("#5f9e4f", "#3d6b31"), ("#7cb562", "#4e7c3b"), ("#4a8a5c", "#2f5e3c")]
VIOLET = [("#7b6fc0", "#4f468a"), ("#9184d1", "#5d5399")]
WARM = [("#b5654f", "#7a3d2e"), ("#c9a14a", "#8a6a28"), ("#8f2e3e", "#5e1b27")]

def zone_palette(x):
    # left greens/teals -> middle teals/blues -> right blues/violets, a few warm accents
    t = x / W + rng.gauss(0, 0.08)
    r = rng.random()
    if r < 0.06:
        return rng.choice(WARM)
    if t < 0.33:
        return rng.choice(GREEN + TEAL)
    if t < 0.66:
        return rng.choice(TEAL + BLUE)
    return rng.choice(BLUE + VIOLET)

def blob_path(cx, cy, r, lobes, wobble):
    pts = []
    n = 14
    phase = rng.random() * math.tau
    for i in range(n):
        a = i / n * math.tau
        rr = r * (1 + wobble * math.sin(lobes * a + phase) + 0.08 * (rng.random() - 0.5))
        pts.append((cx + rr * math.cos(a), cy + rr * 0.85 * math.sin(a)))
    # smooth closed curve via quadratic midpoints
    d = []
    for i in range(n):
        p0 = pts[i]
        p1 = pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        if i == 0:
            d.append(f"M{mx:.1f},{my:.1f}")
        else:
            d.append(f"Q{p0[0]:.1f},{p0[1]:.1f} {mx:.1f},{my:.1f}")
    p0 = pts[0]
    p1 = pts[1]
    d.append(f"Q{p0[0]:.1f},{p0[1]:.1f} {(p0[0]+p1[0])/2:.1f},{(p0[1]+p1[1])/2:.1f}Z")
    return " ".join(d)

shapes = []

# layer 1: dense background blobs
for _ in range(5200):
    x, y = rng.uniform(-40, W + 40), rng.uniform(-40, H + 40)
    fill, stroke = zone_palette(x)
    r = rng.uniform(9, 22)
    d = blob_path(x, y, r, rng.choice([2, 3, 4, 5]), rng.uniform(0.08, 0.28))
    shapes.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')

# layer 2: long fibres (bead chains along curves) - like cytoskeleton / peptide chains
def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

for _ in range(7):
    p0 = (rng.uniform(-100, W + 100), rng.uniform(-100, H + 100))
    p3 = (rng.uniform(-100, W + 100), rng.uniform(-100, H + 100))
    p1 = (p0[0] + (p3[0]-p0[0])/3 + rng.uniform(-250, 250), p0[1] + (p3[1]-p0[1])/3 + rng.uniform(-250, 250))
    p2 = (p0[0] + 2*(p3[0]-p0[0])/3 + rng.uniform(-250, 250), p0[1] + 2*(p3[1]-p0[1])/3 + rng.uniform(-250, 250))
    bead = rng.uniform(4.5, 7)
    fill, stroke = rng.choice([("#dfe9e4", "#9fb7ad"), ("#c7dbe8", "#86a4ba"), ("#e8e2c9", "#b1a77d")])
    steps = 420
    last = None
    for i in range(steps + 1):
        x, y = bezier(p0, p1, p2, p3, i / steps)
        if last and math.hypot(x - last[0], y - last[1]) < bead * 1.6:
            continue
        last = (x, y)
        shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{bead:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')

# layer 3: larger complexes with sub-units
for _ in range(160):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    fill, stroke = zone_palette(x)
    k = rng.randint(3, 6)
    base = rng.uniform(9, 15)
    for j in range(k):
        a = j / k * math.tau + rng.random() * 0.4
        cx, cy = x + math.cos(a) * base * 1.1, y + math.sin(a) * base * 1.1
        d = blob_path(cx, cy, base, rng.choice([2, 3]), 0.15)
        shapes.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')

# layer 4: short peptide chains (the lab's subject) in warm accent beads
for _ in range(40):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    a = rng.random() * math.tau
    n = rng.randint(5, 10)
    col = rng.choice([("#f1c75b", "#a8832a"), ("#e58e6b", "#a3563a"), ("#f3e6b0", "#b4a46a")])
    for j in range(n):
        a += rng.uniform(-0.7, 0.7)
        x += math.cos(a) * 8
        y += math.sin(a) * 8
        shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{col[0]}" stroke="{col[1]}" stroke-width="1.2"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
       f'<rect width="{W}" height="{H}" fill="#1c3a4a"/>' + "".join(shapes) + "</svg>")
with open(out, "w") as f:
    f.write(svg)
print(out, len(svg) // 1024, "KB", len(shapes), "shapes")
