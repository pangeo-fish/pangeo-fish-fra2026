"""Original educational WGS84 calculations; no fish/PR performance data.

Run from any directory: python make_healpix_figure.py
Requires numpy and matplotlib. SciPy is optional (meridional-distance checks).
The equations are documented in docs/science/09_ellipsoidal_healpix.md.
"""
from pathlib import Path
import csv
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "docs" / "science" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
EVIDENCE = HERE.parent / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
A = 6378137.0
F = 1.0 / 298.257223563
E2 = F * (2.0 - F)
E = np.sqrt(E2)


def q(phi):
    s = np.sin(phi)
    return (1.0 - E2) * (s / (1.0 - E2 * s**2) + np.arctanh(E * s) / E)


QP = float(q(np.pi / 2.0))
RQ = A * np.sqrt(QP / 2.0)


def authalic(phi):
    return np.arcsin(np.clip(q(phi) / QP, -1.0, 1.0))


def geocentric(phi):
    return np.arctan2((1.0 - E2) * np.sin(phi), np.cos(phi))


def meridional_radius(phi):
    return A * (1.0 - E2) / (1.0 - E2 * np.sin(phi)**2)**1.5


levels = []
for level in range(9, 14):
    npix = 12 * 4**level
    area = 4.0 * np.pi * RQ**2 / npix
    levels.append(dict(level=level, nside=2**level, global_cells=npix,
                       area_km2=float(area / 1e6),
                       sqrt_area_km=float(np.sqrt(area) / 1000.0),
                       global_float64_field_GiB=npix * 8 / 2**30))

latitudes = []
for degrees in [0, 25, 30, 35, 40, 45, 50, 60, 90]:
    phi = np.deg2rad(degrees)
    xi = authalic(phi)
    theta = geocentric(phi)
    record = dict(geodetic_deg=degrees, authalic_deg=float(np.rad2deg(xi)),
                  geocentric_deg=float(np.rad2deg(theta)),
                  phi_minus_authalic_deg=float(np.rad2deg(phi-xi)),
                  phi_minus_geocentric_deg=float(np.rad2deg(phi-theta)))
    try:
        from scipy.integrate import quad
        # Counterfactual: interpret the number xi as a geodetic latitude.
        # This is NOT the coordinate round-trip error or fish-location error.
        record["same_longitude_misinterpretation_km"] = float(quad(meridional_radius, float(xi), float(phi))[0] / 1000.0)
    except ImportError:
        pass
    latitudes.append(record)

numeric = dict(meaning="WGS84 mathematical illustration; not measured PR #333 errors or fish-location accuracy", a_m=A,
               inverse_flattening=1/F, eccentricity_squared=E2, qp=QP,
               authalic_radius_m=float(RQ), levels=levels, latitudes=latitudes)
(EVIDENCE / "healpix_numeric_table.json").write_text(json.dumps(numeric, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for filename, rows in [("healpix_levels.csv", levels), ("wgs84_latitudes.csv", latitudes)]:
    with (EVIDENCE / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

font_path = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
if font_path.exists():
    font_name = FontProperties(fname=str(font_path)).get_name()
    plt.rcParams["font.family"] = font_name
plt.rcParams.update({"font.size": 11, "axes.labelsize": 11, "axes.titlesize": 12,
                     "xtick.labelsize": 10, "ytick.labelsize": 10,
                     "svg.fonttype": "path", "pdf.fonttype": 42,
                     "axes.unicode_minus": False})
plum = "#603351"
pink = "#c34b84"
orange = "#e88c47"
muted = "#72676c"
cream = "#fffaf6"
grid = "#e7dedb"

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.4, 5.8), gridspec_kw={"width_ratios": [1.6, 1]})
fig.patch.set_facecolor(cream)
for axis in (ax, bx):
    axis.set_facecolor(cream)
    for spine in ("top", "right"):
        axis.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        axis.spines[spine].set_color(grid)
    axis.tick_params(colors=muted)
    axis.xaxis.label.set_color(plum)
    axis.yaxis.label.set_color(plum)
    axis.set_axisbelow(True)

degrees = np.linspace(-90.0, 90.0, 1801)
phi = np.deg2rad(degrees)
ax.plot(degrees, np.rad2deg(phi-authalic(phi)), color=pink, lw=2.7, label=r"測地緯度 $\varphi$ − 等積緯度 $\xi$")
ax.plot(degrees, np.rad2deg(phi-geocentric(phi)), color=orange, lw=2.7, label=r"測地緯度 $\varphi$ − 地心緯度 $\theta$")
ax.axhline(0, color=grid, lw=1)
ax.axvline(45, color=muted, lw=0.9, ls=(0, (3, 3)), alpha=0.65)
ax.set(xlim=(-90, 90), ylim=(-0.225, 0.265), xticks=np.arange(-90, 91, 30),
       xlabel=r"WGS84 の測地緯度 $\varphi$（度）", ylabel="緯度の数値差（度）")
ax.set_title("A　等積緯度と地心緯度は異なる", loc="left", color=plum, pad=17, fontweight="bold")
ax.grid(axis="y", color=grid, lw=0.6)
ax.legend(loc="lower right", frameon=False, fontsize=10)
for yvalue, label, color, xytext in [
    (float(np.rad2deg(np.pi/4-authalic(np.pi/4))), "0.1283°", pink, (9, 0.128)),
    (float(np.rad2deg(np.pi/4-geocentric(np.pi/4))), "0.1924°", orange, (6, 0.229)),
]:
    ax.scatter([45], [yvalue], s=34, color=color, zorder=5)
    ax.annotate(label, xy=(45,yvalue), xytext=xytext, color=color, fontsize=11,
                fontweight="bold", arrowprops={"arrowstyle": "-", "color": color, "lw": 1})

ys = np.arange(len(levels))
lengths = [row["sqrt_area_km"] for row in levels]
colors = ["#c6b1bd", pink, "#d6758d", orange, "#a96e61"]
bx.hlines(ys, 0, lengths, color=colors, lw=4, alpha=0.62)
bx.scatter(lengths, ys, s=70, c=colors, zorder=3)
for yy, xx in zip(ys, lengths):
    bx.text(xx+0.35, yy, f"{xx:.3f} km", va="center", fontsize=10, color=plum)
bx.set(yticks=ys, yticklabels=[f"level {row['level']}" for row in levels], xlim=(0,16.7),
       xticks=[0,4,8,12,16], ylim=(4.65,-0.7), xlabel=r"代表長 $\sqrt{A_{\rm cell}}$（km）")
bx.set_title("B　level とセルの代表長", loc="left", color=plum, pad=17, fontweight="bold")
bx.grid(axis="x", color=grid, lw=0.6)
bx.text(0.49,0.10,"面積の平方根です。\n辺長や検出半径、\n推定精度とは異なります。",transform=bx.transAxes,
        fontsize=10,color=muted,va="bottom")

fig.suptitle("楕円体 HEALPix：座標の意味と格子の細かさ", x=0.065, ha="left", y=0.97,
             fontsize=17,fontweight="bold",color=plum)
fig.text(0.065,0.905,"WGS84：a = 6,378,137 m、1/f = 298.257223563 ／ 等積球半径 = 6,371,007.181 m", fontsize=10.5,color=muted)
fig.text(0.065,0.06,"定義式から作成した数学的説明図。魚の位置推定結果や PR #333 の実測誤差を示すものではありません。",fontsize=10,color=muted)
fig.text(0.065,0.025,"式：Karney (2024), doi:10.1080/00396265.2023.2217604 ／ HEALPix：Górski et al. (2005), doi:10.1086/427976",fontsize=8.7,color=muted)
fig.subplots_adjust(left=0.08,right=0.97,top=0.78,bottom=0.19,wspace=0.32)
for ext in ("svg", "png"):
    fig.savefig(OUT / f"ellipsoidal_healpix_geometry.{ext}", dpi=220, facecolor=fig.get_facecolor())
plt.close(fig)
print(json.dumps({"authalic_radius_m":float(RQ),"figure":str(OUT / "ellipsoidal_healpix_geometry.png"),"levels":levels},ensure_ascii=False))
