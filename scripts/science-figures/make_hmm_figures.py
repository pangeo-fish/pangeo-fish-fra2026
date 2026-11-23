"""Generate original Japanese FRA teaching figures; no fish data are used.

Run: python make_hmm_figures.py
Requires NumPy, Matplotlib and Noto Sans CJK (fallback font list is provided).
All outputs are relative to this script and safe to regenerate.
The toy HMM uses textbook initial emission weighting pi * L[0], unlike the
initialization reported for Pangeo-Fish main@8fb0870. All 2**6 paths are
enumerated to verify forward/backward and Viterbi outputs independently.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "science" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
if FONT_PATH.exists():
    font_manager.fontManager.addfont(str(FONT_PATH))
    FONT = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
else:
    FONT = "Noto Sans CJK JP"

plt.rcParams.update(
    {
        "font.family": [FONT, "DejaVu Sans"],
        "font.size": 12,
        "axes.unicode_minus": False,
        "axes.edgecolor": "#D7CBC6",
        "text.color": "#40343D",
        "axes.labelcolor": "#40343D",
        "xtick.color": "#584B53",
        "ytick.color": "#584B53",
        "figure.facecolor": "#FFFDF9",
        "axes.facecolor": "#FFFDF9",
        "savefig.facecolor": "#FFFDF9",
        "svg.fonttype": "path",
    }
)

C = {
    "ink": "#40343D",
    "muted": "#7C6A73",
    "coral": "#D96B55",
    "pink": "#D277A1",
    "plum": "#6D426F",
    "peach": "#FBE7DB",
    "rose": "#F8E5ED",
    "lilac": "#EDE4F0",
    "cream": "#FFF5E5",
    "line": "#CBB9B2",
    "paper": "#FFFDF9",
}


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.18)
    fig.savefig(OUT / f"{name}.png", dpi=160, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def box(ax, xy, width, height, title, body="", fill="peach", edge="line", size=13):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        fc=C.get(fill, fill), ec=C.get(edge, edge), lw=1.2,
    )
    ax.add_patch(patch)
    if body:
        ax.text(x + width / 2, y + height * 0.68, title,
                ha="center", va="center", fontsize=size, fontweight="bold")
        ax.text(x + width / 2, y + height * 0.29, body,
                ha="center", va="center", fontsize=size - 2, color=C["muted"])
    else:
        ax.text(x + width / 2, y + height / 2, title,
                ha="center", va="center", fontsize=size, fontweight="bold")


def arrow(ax, start, end, *, color="plum", lw=1.7):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>",
                                mutation_scale=15, lw=lw,
                                color=C.get(color, color), shrinkA=3, shrinkB=3))


def workflow():
    fig, ax = plt.subplots(figsize=(14, 9.1))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    ax.set(xlim=(0, 14), ylim=(0, 9.3))
    ax.axis("off")
    ax.text(0.5, 9.0, "観測の情報を、時間につながる位置推定へ",
            fontsize=22, fontweight="bold", va="center")
    ax.text(0.5, 8.57, "科学的な役割と主な実装の対応  |  main@8fb0870 の調査報告に基づく概念図",
            fontsize=11, color=C["muted"])

    inputs = [
        (0.55, "水温・深度", "タグ温度 ＋ 海洋モデル"),
        (3.9, "音響観測", "検出記録 ＋ 受信局"),
        (7.25, "海底地形", "最大深度 ＋ bathymetry"),
        (10.6, "潮汐", "深度変動 ＋ 潮汐モデル"),
    ]
    for x, title, body in inputs:
        box(ax, (x, 7.2), 2.85, 0.95, title, body, size=13)
        arrow(ax, (x + 1.425, 7.17), (x + 1.425, 6.62), color="coral")

    box(ax, (0.55, 5.6), 12.9, 1.02,
        "各セル・各時刻の観測重み：どの場所が観測と整合するか",
        "水温 / 音響 / 海底地形 / 潮汐  →  尤度・適合度・制約", fill="rose", size=15)
    arrow(ax, (7.0, 5.57), (7.0, 5.0))
    box(ax, (4.05, 4.02), 5.9, 0.98,
        "位置合わせ・観測重みの組合せ",
        "combine_emission_pdf  /  終端情報は最終時刻へ", fill="rose", size=14)

    arrow(ax, (7, 3.99), (7, 3.4))
    box(ax, (4.05, 2.26), 5.9, 1.14,
        "HMM：時間方向に推論する",
        "forward / backward  ＋  viterbi_healpix", fill="lilac", edge="plum", size=15)
    box(ax, (0.55, 2.29), 2.85, 1.08,
        "初期分布", "放流位置と位置の幅", fill="cream", size=13)
    box(ax, (10.6, 2.29), 2.85, 1.08,
        "移動モデル", "σ・演算子・境界条件", fill="cream", size=13)
    arrow(ax, (3.42, 2.83), (4.02, 2.83))
    arrow(ax, (10.57, 2.83), (9.98, 2.83))
    arrow(ax, (7.0, 2.23), (7.0, 1.76))
    box(ax, (4.05, 0.93), 5.9, 0.83,
        "位置分布と経路の要約",
        "不確実性 / mean / mode / Viterbi", fill="lilac", size=14)

    # An underpinning bracket is deliberately not a downstream workflow arrow.
    ax.plot([0.24, 0.24], [0.72, 8.05], ls=(0, (4, 4)), color=C["coral"], lw=1.1)
    ax.plot([13.76, 13.76], [0.72, 8.05], ls=(0, (4, 4)), color=C["coral"], lw=1.1)
    box(ax, (0.22, 0.12), 13.56, 0.6,
        "全段階を支える空間表現：HEALPix のセルID・level・楕円体をそろえる",
        fill="cream", edge="coral", size=13)
    save(fig, "01_workflow")


def toy_hmm():
    states = np.array([-1.0, 1.0])
    pi = np.array([0.5, 0.5])
    # K[destination, source]. Both rows and columns sum to one here.
    K = np.array([[0.9, 0.1], [0.1, 0.9]])
    likelihood = np.array([[0.2, 0.8], [0.3, 0.7], [0.8, 0.2],
                           [0.8, 0.2], [0.3, 0.7], [0.2, 0.8]])
    nt = len(likelihood)
    forward = np.empty_like(likelihood)
    scales = np.empty(nt)
    raw = pi * likelihood[0]
    scales[0] = raw.sum()
    forward[0] = raw / scales[0]
    for t in range(1, nt):
        raw = (K @ forward[t - 1]) * likelihood[t]
        scales[t] = raw.sum()
        forward[t] = raw / scales[t]
    backward = np.ones_like(likelihood)
    for t in range(nt - 2, -1, -1):
        backward[t] = K.T @ (likelihood[t + 1] * backward[t + 1])
        backward[t] /= backward[t].sum()
    smoothed = forward * backward
    smoothed /= smoothed.sum(axis=1, keepdims=True)

    delta = np.empty_like(likelihood)
    backpointer = np.zeros((nt, 2), dtype=int)
    delta[0] = np.log(pi) + np.log(likelihood[0])
    for t in range(1, nt):
        candidate = np.log(K) + delta[t - 1][None, :]
        backpointer[t] = np.argmax(candidate, axis=1)
        delta[t] = np.max(candidate, axis=1) + np.log(likelihood[t])
    vpath = np.empty(nt, dtype=int)
    vpath[-1] = np.argmax(delta[-1])
    for t in range(nt - 2, -1, -1):
        vpath[t] = backpointer[t + 1, vpath[t + 1]]

    # Independent exact enumeration of all paths, including initial emission.
    allpaths = np.array(list(itertools.product(range(2), repeat=nt)))
    pathweights = np.array([
        pi[p[0]] * likelihood[0, p[0]] * np.prod([
            K[p[t], p[t - 1]] * likelihood[t, p[t]] for t in range(1, nt)
        ]) for p in allpaths
    ])
    evidence = pathweights.sum()
    posteriors = pathweights / evidence
    enum_marginals = np.array([
        [posteriors[allpaths[:, t] == s].sum() for s in range(2)]
        for t in range(nt)
    ])
    assert np.allclose(smoothed, enum_marginals, atol=1e-14)
    assert np.isclose(np.prod(scales), evidence, atol=1e-14)
    assert np.array_equal(vpath, allpaths[np.argmax(pathweights)])
    modes = np.argmax(smoothed, axis=1)
    assert len(set(modes)) == 2 and not np.array_equal(modes, vpath)

    return {
        "states": states.tolist(), "initial": pi.tolist(),
        "transition_destination_source": K.tolist(),
        "likelihoods": likelihood.tolist(),
        "filtered": forward.tolist(), "smoothed": smoothed.tolist(),
        "mode_indices": modes.tolist(), "mode_positions": states[modes].tolist(),
        "viterbi_indices": vpath.tolist(), "viterbi_positions": states[vpath].tolist(),
        "mean_positions": (smoothed @ states).tolist(),
        "viterbi_path_posterior": float(np.max(posteriors)),
        "evidence": float(evidence), "enumerated_paths": len(allpaths),
        "verification": "Forward/backward marginals and Viterbi exactly agree with complete enumeration to floating-point tolerance.",
        "initialization": "Textbook initial distribution is proportional to pi * likelihood[0]; not Pangeo-Fish's reported release-only forward initialization.",
    }


def summaries(model):
    q = np.array(model["smoothed"])
    l = np.array(model["likelihoods"])
    t = np.arange(1, 7)
    fig = plt.figure(figsize=(14, 9.2))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 2.4],
                          width_ratios=[10, 0.3],
                          left=0.13, right=0.9, top=0.84, bottom=0.21,
                          hspace=0.51, wspace=0.06)
    ax_l = fig.add_subplot(gs[0, 0])
    ax_q = fig.add_subplot(gs[1, 0])
    ax_track = fig.add_subplot(gs[2, 0])
    cax = fig.add_subplot(gs[0:2, 1])
    cmap = LinearSegmentedColormap.from_list("warm", ["#FFF7EF", "#EDA68B", C["plum"]])
    for ax, data, label in [(ax_l, l, "① 観測の重み"), (ax_q, q, "② 全観測を使った位置確率")]:
        im = ax.imshow(data.T, origin="lower", aspect="auto", vmin=0, vmax=1,
                       cmap=cmap, extent=[0.5, 6.5, -1.5, 1.5])
        ax.set_xticks(t, [])
        ax.set_yticks([-0.75, 0.75], ["南：−1", "北：＋1"])
        ax.set_title(label, loc="left", fontsize=13, fontweight="bold", pad=9)
        for j in range(6):
            for i in range(2):
                val = data[j, i]
                ax.text(j + 1, [-0.75, 0.75][i], f"{val:.3f}",
                        ha="center", va="center", fontsize=12,
                        color="white" if val > 0.67 else C["ink"])
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    cb = fig.colorbar(im, cax=cax)
    cb.set_ticks([0, 0.5, 1])
    cb.set_label("重み / 確率", labelpad=8)
    cb.outline.set_visible(False)

    ax_track.axhspan(-0.8, 0.8, color="#EEE9E3", alpha=0.65, zorder=0)
    ax_track.text(3.5, -0.47, "中間には候補セルを置いていない",
                  ha="center", va="center", fontsize=12, color=C["muted"])
    ax_track.plot(t, model["viterbi_positions"], "-", lw=7, alpha=0.48,
                  color=C["plum"], label="Viterbi：経路全体の最大", zorder=2)
    ax_track.plot(t, model["mode_positions"], "--^", ms=9, lw=2.3,
                  markerfacecolor=C["paper"], markeredgewidth=2,
                  color=C["coral"], label="mode：時刻ごとの最頻", zorder=4)
    ax_track.plot(t, model["mean_positions"], "-o", ms=7, lw=2.5,
                  color=C["pink"], label="mean：分布の重心", zorder=5)
    ax_track.set(xlim=(0.5, 6.5), ylim=(-1.25, 1.3), xticks=t,
                 yticks=[-1, 0, 1], yticklabels=["南：−1", "0", "北：＋1"], xlabel="時刻（任意の単位）")
    ax_track.set_title("③ 同じ HMM から得る、異なる要約", loc="left",
                       fontsize=13, fontweight="bold", pad=9)
    ax_track.spines[["top", "right"]].set_visible(False)
    ax_track.grid(axis="x", alpha=0.15)
    handles, labels = ax_track.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.125),
               ncol=3, frameon=False, fontsize=11, handlelength=2.4)

    fig.text(0.07, 0.955, "平均・時刻別最頻・Viterbi は、違う問いへの答え",
             fontsize=22, fontweight="bold")
    fig.text(0.07, 0.907,
             "教材用の厳密な2状態 HMM  |  同じ位置に残る確率 0.9、移る確率 0.1、初期確率は各0.5",
             fontsize=12, color=C["muted"])
    fig.text(0.07, 0.076,
             "t=3,4 の周辺確率は南がわずかに大きい。一方、経路全体では北にとどまる列が最大。",
             fontsize=11)
    fig.text(0.07, 0.038,
             "実際の魚・Pangeo-Fish の実行結果ではない。初期重みは教科書的な π×L₁。64通りの全経路列挙で検証。",
             fontsize=10.5, color=C["muted"])
    save(fig, "02_hmm_summaries")


def residual_data():
    residuals = np.array([[-2.0, 2.0], [0.5, 0.5]])
    sigma = 0.75
    per_log = -residuals**2 / (2 * sigma**2)
    return {
        "residuals_degC": residuals.tolist(), "sigma_degC": sigma,
        "mean_residual_degC": residuals.mean(axis=1).tolist(),
        "rmse_degC": np.sqrt((residuals**2).mean(axis=1)).tolist(),
        "mean_residual_gaussian_peak_ratio": np.exp(-residuals.mean(axis=1)**2 / (2 * sigma**2)).tolist(),
        "independent_product_peak_ratio": np.exp(per_log.sum(axis=1)).tolist(),
        "geometric_mean_peak_ratio": np.exp(per_log.mean(axis=1)).tolist(),
        "scaling": "Within each method, divide by the value when all residuals are zero; these are dimensionless relative weights, not probabilities over cells.",
        "variance_alternative_caveat": "Geometric-mean panel illustrates aggregation only with a common fixed variance sigma^2; the actual alternative code accepts depth-dependent variance and adds 0.01 degC^2.",
    }


def residuals(data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8.6),
                                  gridspec_kw={"width_ratios": [0.88, 1.25]})
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.32, top=0.8, wspace=0.31)
    r = np.array(data["residuals_degC"])
    x = np.arange(2)
    ax1.axhline(0, color=C["muted"], lw=1)
    for i, (label, color, dx) in enumerate([("候補 A", C["coral"], -0.18), ("候補 B", C["plum"], 0.18)]):
        bars = ax1.bar(x + dx, r[i], width=0.32, color=color, alpha=0.9, label=label)
        for bar, val in zip(bars, r[i]):
            ax1.text(bar.get_x() + bar.get_width()/2, val + (0.14 if val >= 0 else -0.16),
                     f"{val:+.1f}", ha="center", va="bottom" if val >= 0 else "top", fontsize=12)
    ax1.set(xticks=x, xticklabels=["観測 1", "観測 2"], ylim=(-2.65, 2.65), ylabel="タグ − モデルの水温差（°C）")
    ax1.set_title("① 符号付き残差", loc="left", fontsize=15, fontweight="bold", pad=14)
    ax1.legend(loc="upper left", frameon=False, ncol=2)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.grid(axis="y", color=C["line"], alpha=0.25)
    ax1.set_axisbelow(True)

    keys = ["mean_residual_gaussian_peak_ratio", "independent_product_peak_ratio", "geometric_mean_peak_ratio"]
    vals = np.array([data[k] for k in keys])
    labels = ["平均残差\n→ ガウス関数", "各サンプルの\nガウス密度の積", "各サンプルの\nガウス密度の\n幾何平均"]
    for i, (color, dx) in enumerate([(C["coral"], -0.17), (C["plum"], 0.17)]):
        bars = ax2.bar(np.arange(3)+dx, vals[:, i], width=0.3, color=color, alpha=0.9)
        for b, v in zip(bars, vals[:, i]):
            txt = f"{v:.3f}" if v >= 0.01 else f"{v:.6f}"
            ax2.text(b.get_x()+b.get_width()/2, v*1.22, txt, ha="center", va="bottom", fontsize=10.5)
    ax2.set(xticks=np.arange(3), xticklabels=labels, yscale="log", ylim=(1e-4, 2.2),
            ylabel="残差が全て0のときに対する重みの比")
    ax2.set_title("② 集約の仕方で、候補の順位が変わる", loc="left", fontsize=15, fontweight="bold", pad=14)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="y", which="major", color=C["line"], alpha=0.4)
    ax2.set_axisbelow(True)

    fig.text(0.07, 0.94, "平均の一致と、一つ一つの観測の一致は異なる",
             fontsize=22, fontweight="bold")
    fig.text(0.07, 0.884,
             "教材用の2サンプル  |  σ = 0.75 °C  |  A：平均差 0 / RMSE 2 °C    B：平均差 0.5 / RMSE 0.5 °C",
             fontsize=12, color=C["muted"])

    fig.text(0.07, 0.24, "主デモの集約", fontsize=13, fontweight="bold", color=C["coral"])
    fig.text(0.07, 0.195, "平均してから二乗するため、A の −2 と＋2 が相殺する。", fontsize=12)
    fig.text(0.07, 0.145, "独立積・幾何平均の比較", fontsize=13, fontweight="bold", color=C["plum"])
    fig.text(0.07, 0.10, "個々の差も評価するが、観測の相関・個数と、他の情報に対する重みを検討する必要がある。", fontsize=12)
    fig.text(0.07, 0.048,
             "実データではない。各方式でゼロ残差時の定数を除外。幾何平均は集約法だけの比較で、深度別分散の実装再現ではない。",
             fontsize=10.3, color=C["muted"])
    save(fig, "03_temperature_residuals")


if __name__ == "__main__":
    model = toy_hmm()
    temp = residual_data()
    workflow()
    summaries(model)
    residuals(temp)
    provenance = {
        "description": "Original teaching illustrations for the Japanese FRA documentation; all numerical data are synthetic.",
        "created_on": "2026-11-23",
        "pangeo_fish_notebooks_executed": False,
        "workflow_evidence": "User-supplied FRA 2026 scientific documentation review, main@8fb0870; conceptual relationships, not a statement of exact call order.",
        "toy_hmm": model,
        "temperature_example": temp,
    }
    evidence = ROOT.parent / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "hmm_figure_data.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Wrote three SVG/PNG figures and hmm_figure_data.json; exact enumeration verification passed.")
