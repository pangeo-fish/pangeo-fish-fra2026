"""Reproduce the synthetic Japanese observation-method illustration.

No fish observations or tracking outputs are used.
Run: python make_observation_figure.py --output figures
"""
from pathlib import Path
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'docs' / 'science' / 'figures')
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if Path(font_path).exists():
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()
else:
    plt.rcParams['font.family'] = ['Noto Sans CJK JP', 'sans-serif']
plt.rcParams.update({'font.size':10, 'axes.labelsize':10, 'axes.titlesize':12,
                     'axes.spines.top':False, 'axes.spines.right':False,
                     'axes.edgecolor':'#947F81', 'text.color':'#3E303A',
                     'axes.labelcolor':'#3E303A', 'xtick.color':'#5C4B54',
                     'ytick.color':'#5C4B54', 'svg.fonttype':'path'})
coral='#D96F55'; plum='#77455F'; muted='#AA9BA4'; light='#F8EEE9'
fig, axes = plt.subplots(1,3,figsize=(14.1,5.2),gridspec_kw={'wspace':0.33})
fig.patch.set_facecolor('#FFFDFC')
for ax in axes:
    ax.set_facecolor('#FFFDFC')
    ax.grid(axis='y', color='#E9DEDA', linewidth=.65)
    ax.set_axisbelow(True)

# 1. A fixed-depth datum and a candidate tide signal; demean both.
t=np.linspace(0,24,145)
eta=1.8*np.sin(2*np.pi*t/12.4206)+0.35*np.sin(2*np.pi*t/24)
depth=60+eta+0.12*np.sin(2*np.pi*t/2.9)
wrong=1.8*np.sin(2*np.pi*(t-3)/12.4206)+0.35*np.sin(2*np.pi*t/24)
axes[0].plot(t,depth-depth.mean(),color=plum,lw=2.3,label='合成タグ：平均を除去')
axes[0].plot(t,eta-eta.mean(),color=coral,lw=2,ls='--',label='候補A：同じ潮汐位相')
axes[0].plot(t,wrong-wrong.mean(),color=muted,lw=1.8,ls=':',label='候補B：異なる位相')
axes[0].set(title='1  潮汐：形を比較する',xlabel='時間（h）',ylabel='平均からの水深・海面高度偏差（m）',xlim=(0,24))
axes[0].set_xticks([0,6,12,18,24]); axes[0].set_ylim(-3.2,3.2)
axes[0].text(.04,.96,'d = D + η + 誤差\nDは候補セルごとに推定',transform=axes[0].transAxes,va='top',fontsize=9,bbox={'facecolor':light,'edgecolor':'none','pad':5})
axes[0].legend(loc='lower left',fontsize=8.6,frameon=True,facecolor='#FFFDFC',edgecolor='#E9DEDA')

# 2. Idealized subcell bathymetric support. This is not the implementation's bin lookup.
bottom=np.arange(25,100,10)
z=np.linspace(0,110,551)
support=np.mean(bottom[:,None]>=z[None,:],axis=0)
axes[1].plot(z,support,color=plum,lw=2.4,drawstyle='steps-post')
axes[1].fill_between(z,0,support,color=coral,alpha=.15,step='post')
axes[1].axvline(60,color=coral,lw=1.8,ls='--')
axes[1].scatter([60],[.5],s=45,color=coral,zorder=5)
axes[1].text(63,.57,'60 mより深い\n場所の割合 = 1/2',fontsize=9)
axes[1].text(.04,.96,'同一セル内に8地点\n底の水深：25〜95 m',transform=axes[1].transAxes,va='top',fontsize=9,bbox={'facecolor':light,'edgecolor':'none','pad':5})
axes[1].set(title='2  海底地形：深さの条件',xlabel='必要な水深 z（m）',ylabel='セル内で H ≥ z を満たす割合',xlim=(0,110),ylim=(-.02,1.2))
axes[1].set_yticks([0,.25,.5,.75,1]); axes[1].set_xticks([0,20,40,60,80,100])

# 3. A conceptual footprint versus a non-calibrated probability curve.
r=np.linspace(0,4,401)
binary=(r<=2).astype(float)
q=.9*np.exp(-.5*(r/1.5)**2)
axes[2].plot(r,binary,color=coral,lw=2.3,label='2 kmの二値範囲')
axes[2].plot(r,q,color=plum,lw=2.3,label='仮想の検出確率 q(r)')
axes[2].axvline(2,color=muted,lw=1,ls=':')
axes[2].text(.05,.51,'距離だけでなく稼働状況・\n環境・送信条件も検討する',transform=axes[2].transAxes,fontsize=9,bbox={'facecolor':light,'edgecolor':'none','pad':5})
axes[2].set(title='3  音響：範囲と検出確率',xlabel='受信機からの距離（km）',ylabel='範囲の重み／検出確率',xlim=(0,4),ylim=(-.02,1.2))
axes[2].set_yticks([0,.25,.5,.75,1]); axes[2].set_xticks([0,1,2,3,4])
axes[2].legend(loc='lower left',fontsize=8.7,frameon=True,facecolor='#FFFDFC',edgecolor='#E9DEDA')
fig.suptitle('観測ごとに「位置に合う」の意味が異なる',fontsize=17,fontweight='bold',y=.98)
fig.text(.5,.035,'全パネルは説明用の合成例。実測データ、魚の推定経路、測位精度の検証結果は含まない。',ha='center',fontsize=10,color='#695560')
fig.subplots_adjust(top=.82,bottom=.18,left=.065,right=.985)
for suffix in ('png','svg'):
    fig.savefig(args.output/f'observation_constraints.{suffix}',dpi=180,bbox_inches='tight',facecolor=fig.get_facecolor())
print('Saved observation_constraints.png and observation_constraints.svg')
