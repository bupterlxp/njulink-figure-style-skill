"""Measured T2AV-inspired composition with original vectors and simulated data.

Data and labels live in assets/compass-demo.json. Panels share a subject,
model order and score table. Chalkboard is preferred when installed; bundled
OFL Comic Neue fonts provide a portable alternative.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import to_rgb
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle, Wedge
import numpy as np
from scipy.stats import gaussian_kde

ROOT = Path(__file__).resolve().parents[1]
INK, MUTED, GRID = '#252C3B', '#666E7C', '#E5E8ED'


def load_data():
    data = json.loads((ROOT / 'assets/compass-demo.json').read_text())
    scores = np.array(data['scores'])
    if scores.shape != (len(data['models']), len(data['axes'])):
        raise ValueError('scores need one row per model and one column per axis')
    if not np.isfinite(scores).all() or np.any((scores < 0) | (scores > 100)):
        raise ValueError('scores must be finite percentages in [0, 100]')
    if len(data['models']) != len(data['model_colors']):
        raise ValueError('each model needs one stable color')
    dimensions = [d['name'] for g in data['taxonomy'] for d in g['dimensions']]
    if dimensions != data['axes']:
        raise ValueError('taxonomy and scores must describe the same dimensions')
    return data


def style(font='reference'):
    for path in sorted((ROOT / 'assets/fonts').glob('ComicNeue-*.ttf')):
        fm.fontManager.addfont(str(path))
    family = 'Comic Neue'
    if font == 'reference':
        try:
            fm.findfont(fm.FontProperties(family='Chalkboard'), fallback_to_default=False)
            family = 'Chalkboard'
        except ValueError:
            pass
    plt.rcParams.update({
        'font.family': family, 'font.size': 6.7, 'text.color': INK,
        'axes.labelcolor': INK, 'axes.edgecolor': '#9CA4B0', 'axes.linewidth': 0.45,
        'axes.grid': False, 'axes.facecolor': 'white', 'figure.facecolor': 'white',
        'savefig.facecolor': 'white', 'xtick.color': MUTED, 'ytick.color': MUTED,
        'xtick.labelsize': 5.7, 'ytick.labelsize': 5.7,
        'xtick.major.size': 2, 'ytick.major.size': 2,
        'xtick.major.width': 0.4, 'ytick.major.width': 0.4,
        'legend.frameon': False, 'legend.fontsize': 6.0,
        'pdf.fonttype': 42, 'svg.fonttype': 'path', 'hatch.linewidth': 0.35,
    })
    return family


def tint(color, amount=0.2):
    return tuple(np.array(to_rgb(color)) * (1 - amount) + amount)


def upright(angle):
    """Never put a rotated label upside down."""
    return (angle + 90) % 180 - 90


def label(ax, x, y, text, size=6.7, weight='normal', color=INK, **kwargs):
    return ax.text(x, y, text, fontsize=size, fontweight=weight, color=color,
                   ha=kwargs.pop('ha', 'center'), va=kwargs.pop('va', 'center'), **kwargs)


def card(ax, x, y, w, h, fill='white', edge='#B5BCC5', radius=8, lw=0.75, **kwargs):
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={radius}',
                          facecolor=fill, edgecolor=edge, linewidth=lw, **kwargs)
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, color='#879BBE', lw=1.0, **kwargs):
    patch = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=6.5,
                            linewidth=lw, color=color, shrinkA=0, shrinkB=0, **kwargs)
    ax.add_patch(patch)
    return patch


def wave(ax, x, y, w, h, color='#649EA5'):
    """Schematic waveform glyph; not a measured audio signal."""
    t = np.linspace(0, 1, 55)
    amp = (0.2 + 0.8 * np.sin(np.pi*t)**2) * (0.3 + 0.7*np.abs(np.sin(t*35)))
    ax.vlines(x+t*w, y-amp*h/2, y+amp*h/2, colors=color, linewidth=0.45)


def filmstrip(ax, x, y, w, h):
    """Original vector scene: a cart moves across three frames."""
    card(ax, x, y, w, h, fill=INK, edge=INK, radius=3, lw=0.4)
    for s in np.linspace(x+4, x+w-9, 16):
        for yy in (y+3, y+h-7):
            ax.add_patch(Rectangle((s, yy), 5, 3, color='white', lw=0))
    for i in range(3):
        xx, yy = x+5+i*(w-7)/3, y+11
        fw, fh = (w-19)/3, h-22
        ax.add_patch(Rectangle((xx, yy), fw, fh, facecolor='#DCE9EA', lw=0))
        ax.add_patch(Rectangle((xx, yy), fw, fh*0.32, facecolor='#B9D0B5', lw=0))
        ax.add_patch(Circle((xx+fw*0.76, yy+fh*0.78), fh*0.11, color='#F1D99A', lw=0))
        cart_x = xx+7+i*7
        ax.add_patch(Rectangle((cart_x, yy+fh*0.30), 20, fh*0.34, facecolor='#D49078', lw=0))
        for cx in (cart_x+4, cart_x+16):
            ax.add_patch(Circle((cx, yy+fh*0.30), 3, facecolor=INK, lw=0))


def database(ax, x, y, w, h, color='#8C9FD0'):
    ax.add_patch(Rectangle((x, y+8), w, h-16, color=tint(color, 0.16), lw=0))
    for yy in (y+8, y+h*0.37, y+h*0.64, y+h-8):
        ax.add_patch(Ellipse((x+w/2, yy), w, 17, facecolor=tint(color, 0.16),
                             edgecolor='white', linewidth=1.0))
    ax.add_patch(Ellipse((x+w/2, y+h-8), w, 17, facecolor=tint(color, 0.4),
                         edgecolor='white', linewidth=0.8))


def pipeline(ax,data):
    ax.set(xlim=(0, 1400), ylim=(0, 235))
    ax.axis('off')
    card(ax, 2, 3, 1396, 217, edge='#A5AAB3', radius=20, lw=0.65, linestyle=(0,(4,3)))
    ax.plot([951,951], [16,216], color='#C1C6CE', lw=0.65, dashes=(4,3))
    for num,x,title in [(1,31,'Source material'), (2,333,'Curate'),
                         (3,649,'Compose'), (4,995,'Audit & evaluate')]:
        ax.scatter([x], [220], s=54, c=INK, zorder=10)
        label(ax,x,220,str(num),size=6.0,weight='bold',color='white',zorder=11)
        label(ax,x+24,220,title,size=7.4,ha='left',weight='bold',
              bbox={'facecolor':'white','edgecolor':'none','pad':1.2},zorder=9)
    # Input lanes communicate modalities with their shapes, not identical boxes.
    card(ax,22,116,212,76,fill='#EFF5E9',edge='#88AB70',radius=8)
    label(ax,128,177,'Text prompts',weight='bold',color='#46693F')
    label(ax,128,145,'"A cart rolls past\na ringing bell."',size=6.5)
    filmstrip(ax,22,39,212,58)
    wave(ax,29,23,198,14)
    label(ax,127,105,'Video + audio',size=6.0,color='#996542')
    arrow(ax,(245,150),(310,150),color='#9ABD89',lw=2.5)
    arrow(ax,(245,66),(310,66),color='#D8A07E',lw=2.5)
    rng=np.random.default_rng(11)
    for xx,yy,c in [(351,145,'#94B989'),(394,163,'#87BFC3'),(397,129,'#BBA9D3')]:
        pts=rng.normal([xx,yy],[9,7],(8,2))
        ax.scatter(pts[:,0],pts[:,1],s=5.5,c=c,edgecolors='white',linewidths=0.2)
    label(ax,489,162,'Cluster',size=6.8,weight='bold')
    label(ax,489,141,'& balance',size=6.5)
    label(ax,382,108,'semantic groups',size=5.7,color=MUTED)
    for shift in (12,6,0):
        card(ax,336+shift,27+shift,56,48,fill='#F8EDE3',edge='#D6A982',radius=3,lw=0.6)
    wave(ax,343,49,41,24,'#C5926A')
    label(ax,489,70,'Deduplicate',size=6.8,weight='bold')
    label(ax,489,47,'& align clips',size=6.5)
    # Two non-crossing paths merge at the structured description.
    ax.plot([554,578,578,618],[150,150,111,111],lw=0.8,color='#90AA86')
    ax.plot([554,578,578],[63,63,111],lw=0.8,color='#CF997B')
    arrow(ax,(596,111),(619,111),color='#879AAE')
    card(ax,625,32,283,160,fill='#F4F3FA',edge='#ACA2C8',radius=10)
    label(ax,766,174,'Structured description',size=6.8,weight='bold',color='#665887')
    for i,(name,c) in enumerate([('scene','#B6CADD'),('event','#D9BAD4'),('sound','#AED2C5')]):
        card(ax,641+i*86,133,78,23,fill=tint(c,0.42),edge=c,radius=5,lw=0.55)
        label(ax,680+i*86,144,name,size=6.0)
    label(ax,766,105,'Actor + action + timing',size=6.4)
    ax.plot([644,889],[88,88],color='#D7D2E5',lw=0.55)
    label(ax,766,68,'Rewrite & cross-check',size=6.5,weight='bold')
    label(ax,766,47,'preserve all three modalities',size=5.7,color=MUTED)
    arrow(ax,(915,111),(980,111),color='#94A9C8',lw=2.5)
    card(ax,987,57,239,133,fill='#F0F5FB',edge='#98AECF',radius=9)
    for j,text in enumerate(['Visual constraint','Sound event','Temporal match']):
        yy=163-j*37
        ax.plot([1006,1011,1021],[yy,yy-6,yy+7],color='#619D86',lw=1.2,
                solid_capstyle='round',solid_joinstyle='round')
        label(ax,1036,yy,text,ha='left',size=6.6)
    label(ax,1105,32,'Human spot-check',size=6.2,color='#5C7195')
    arrow(ax,(1234,117),(1261,117),color='#92A5C7')
    database(ax,1270,82,99,103)
    cases=data['trials_per_axis']*len(data['axes'])
    label(ax,1319,61,f'{cases:,} cases',size=7.1,weight='bold')
    label(ax,1319,34,f"{len(data['models'])} models",size=6.5)


def emblem(ax):
    """Original modality glyph; does not reuse the source project's logo."""
    for radius,width in [(0.34,0.65),(0.40,1.0)]:
        ax.add_patch(Circle((0,0.07),radius,facecolor='white',edgecolor='#475A82',linewidth=width))
    for angle,glyph,col in [(90,'T','#8C9DDC'),(210,'V','#89C5BA'),(330,'A','#E5B69C')]:
        t=np.deg2rad(angle)
        p=(0.4*np.cos(t),0.07+0.4*np.sin(t))
        ax.plot([0,p[0]],[0.07,p[1]],color='#A9B2C2',linewidth=0.55,zorder=2)
        ax.add_patch(Circle(p,0.095,facecolor=col,edgecolor='#475A82',linewidth=0.55,zorder=3))
        label(ax,*p,glyph,size=5.8,weight='bold',zorder=4)
    label(ax,0,0.12,'AV',size=8.8,weight='bold',zorder=5,
          bbox={'facecolor':'white','edgecolor':'none','pad':0.7})
    label(ax,0,-0.16,'study',size=5.3,zorder=5)


def radial(ax,data):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set(xlim=(-2.12,2.12),ylim=(-2.10,2.13))
    values=np.array(data['scores'])
    centers=90-np.arange(len(data['axes']))*360/len(data['axes'])
    inner,scale,span=0.91,1.08,32
    for axis_i,(center,name) in enumerate(zip(centers,data['axes'])):
        for m,(model,color) in enumerate(zip(data['models'],data['model_colors'])):
            a1=center-span/2+m*span/len(data['models'])
            a2=a1+span/len(data['models'])-0.45
            value=values[m,axis_i]
            outer=inner+scale*value/100
            ax.add_patch(Wedge((0,0),inner+scale,a1,a2,width=scale,
                               facecolor='#F2F3F5',edgecolor='white',linewidth=0.45))
            ax.add_patch(Wedge((0,0),outer,a1,a2,width=outer-inner,
                               facecolor=color,edgecolor='white',linewidth=0.45,
                               hatch='///' if m==0 else None))
            a=(a1+a2)/2
            t=np.deg2rad(a)
            label(ax,(outer-0.16)*np.cos(t),(outer-0.16)*np.sin(t),f'{value:.0f}',
                  size=5.4,rotation=upright(a),rotation_mode='anchor',weight='bold')
        ax.add_patch(Arc((0,0),1.72,1.72,theta1=center-span/2,theta2=center+span/2,
                         linewidth=0.55,color='#8C94A1'))
        angle=np.deg2rad(center)
        short={'Video match':'V-match','Audio match':'A-match',
               'Visual quality':'V-quality','Audio quality':'A-quality'}.get(name,name)
        label(ax,0.76*np.cos(angle),0.76*np.sin(angle),short,size=5.4,
              rotation=upright(center-90),rotation_mode='anchor',linespacing=0.95)
    emblem(ax)
    handles=[Rectangle((0,0),1,1,facecolor=c,edgecolor='white',hatch='///' if i==0 else None)
             for i,c in enumerate(data['model_colors'])]
    ax.legend(handles,data['models'],loc='upper center',bbox_to_anchor=(0.5,-0.015),
              ncol=3,fontsize=6.4,handlelength=1.4,handleheight=0.85,
              columnspacing=1.2,labelspacing=0.25,handletextpad=0.35,borderaxespad=0)


def sunburst(ax,data):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set(xlim=(-2.03,2.03),ylim=(-2.03,2.03))
    leaves=sum(len(d['leaves']) for g in data['taxonomy'] for d in g['dimensions'])
    step,cursor=360/leaves,90
    for group in data['taxonomy']:
        gspan=sum(len(d['leaves']) for d in group['dimensions'])*step
        ax.add_patch(Wedge((0,0),0.99,cursor-gspan,cursor,width=0.54,
                           facecolor=group['color'],edgecolor='white',linewidth=0.7))
        ga=cursor-gspan/2
        label(ax,0.71*np.cos(np.deg2rad(ga)),0.71*np.sin(np.deg2rad(ga)),group['name'],
              size=6.5,weight='bold',rotation=upright(ga-90),rotation_mode='anchor')
        for dim in group['dimensions']:
            span=len(dim['leaves'])*step
            ax.add_patch(Wedge((0,0),1.43,cursor-span,cursor,width=0.44,
                               facecolor=dim['color'],edgecolor='white',linewidth=0.7))
            da=cursor-span/2
            label(ax,1.20*np.cos(np.deg2rad(da)),1.20*np.sin(np.deg2rad(da)),
                  dim['name'].replace(' ','\n'),size=5.9,weight='bold',
                  rotation=upright(da-90),rotation_mode='anchor',linespacing=1.0)
            for i,leaf in enumerate(dim['leaves']):
                a1,a2=cursor-(i+1)*step,cursor-i*step
                ax.add_patch(Wedge((0,0),1.94,a1,a2,width=0.51,
                                   facecolor=tint(dim['color'],0.19+i*0.09),
                                   edgecolor='white',linewidth=0.7))
                angle=(a1+a2)/2
                t=np.deg2rad(angle)
                label(ax,1.69*np.cos(t),1.69*np.sin(t),leaf,size=5.1,
                      rotation=upright(angle),rotation_mode='anchor')
            cursor-=span
    label(ax,0,0.06,'AV',size=10.0,weight='bold')
    label(ax,0,-0.19,'evaluation',size=5.7)


def density(ax,data):
    rng=np.random.default_rng(data['seed'])
    x=np.linspace(0,300,601)
    samples={}
    for corpus in data['corpora']:
        v=np.maximum(1,np.rint(rng.lognormal(corpus['log_mean'],corpus['log_sigma'],corpus['n'])))
        samples[corpus['name']]=v.tolist()
        kde=gaussian_kde(v,bw_method='scott')
        # Reflection at zero gives a proper density on the positive token domain.
        y=kde(x)+kde(-x)
        ax.fill_between(x,y,color=corpus['color'],alpha=0.28,linewidth=0)
        ax.plot(x,y,color=corpus['color'],lw=0.85,label=corpus['name'])
    ax.set(xlim=(0,280),ylim=(0,0.032),xticks=[0,70,140,210,280],yticks=[0,0.015,0.03])
    ax.set_yticklabels(['0','.015','.030'])
    ax.grid(color=GRID,lw=0.35)
    ax.set_axisbelow(True)
    ax.spines[['top','right']].set_visible(False)
    ax.set_xlabel('Prompt length (tokens)',fontsize=6.4,labelpad=1)
    ax.set_ylabel('Density',fontsize=6.0,labelpad=1)
    ax.legend(loc='upper right',fontsize=5.8,handlelength=1.0,handletextpad=0.35,
              labelspacing=0.15,borderaxespad=0.05)
    return samples


def ranking(ax,data,column,title):
    # These values and colors are exactly the ones used by the radial panel.
    v=np.array(data['scores'])[:,column]
    ax.set(xlim=(0,103),ylim=(len(v)-0.45,-0.65),xticks=[0,50,100],yticks=np.arange(len(v)))
    for i,color in enumerate(data['model_colors']):
        ax.barh(i,100,height=0.66,color=tint(color,0.9),zorder=1)
        ax.barh(i,v[i],height=0.66,color=color,zorder=2)
        ax.text(v[i]-3,i,str(v[i]),ha='right',va='center',fontsize=5.8,weight='bold',zorder=3)
    ax.set_yticklabels(data['models'],fontsize=6.0)
    ax.tick_params(axis='y',length=0,pad=2)
    ax.tick_params(axis='x',labelsize=5.7,pad=1)
    ax.set_xlabel('Pass rate (%)',fontsize=6.1,labelpad=1)
    ax.set_title(title,fontsize=6.8,fontweight='bold',pad=4)
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color('#CBD0D8')


def overview(fig,data,rect,letters=('b','c','d')):
    """Panel coordinates measured against the reference's roughly 2.65:1 strip."""
    x,y,w,h=rect
    def add(box):
        xx,yy,ww,hh=box
        return fig.add_axes([x+xx*w,y+yy*h,ww*w,hh*h])
    ra=add((0.002,0.190,0.315,0.765))
    radial(ra,data)
    de=add((0.379,0.605,0.281,0.305))
    samples=density(de,data)
    ranking(add((0.373,0.160,0.116,0.260)),data,0,'Video match')
    ranking(add((0.548,0.160,0.116,0.260)),data,1,'Audio match')
    sunburst(add((0.695,0.14,0.305,0.79)),data)
    for xx,title in [(0.013,'Model capability profile'),(0.354,'Prompt coverage & alignment'),
                      (0.713,'Evaluation taxonomy')]:
        fig.text(x+xx*w,y+0.972*h,title,fontsize=7.4,fontweight='bold',va='center')
    families=len(data['taxonomy'])
    dimensions=len(data['axes'])
    checks=sum(len(d['leaves']) for g in data['taxonomy'] for d in g['dimensions'])
    for xx,caption in [(0.16,f'({letters[0]}) Scores 0–100; higher is better'),
                       (0.515,f'({letters[1]}) Prompt diversity & constraint matching'),
                       (0.849,f'({letters[2]}) {families} families · {dimensions} dimensions · {checks} checks')]:
        fig.text(x+xx*w,y+0.018*h,caption,fontsize=6.05,color=MUTED,ha='center',va='bottom')
    return samples


def build_figure(*,include_pipeline=True,font='reference'):
    data=load_data()
    family=style(font)
    height=4.12 if include_pipeline else 2.80
    fig=plt.figure(figsize=(7.2,height))
    if include_pipeline:
        fig.text(0.018,0.967,'(a) From multimodal sources to auditable tests',fontsize=8.0,fontweight='bold')
        fig.text(0.982,0.970,'SIMULATED DATA',fontsize=5.6,color=MUTED,ha='right')
        pipeline(fig.add_axes([0.014,0.691,0.972,0.250]),data)
        rect=(0.008,0.049,0.984,0.611)
    else:
        rect=(0.008,0.058,0.984,0.915)
    samples=overview(fig,data,rect,letters=('b','c','d') if include_pipeline else ('a','b','c'))
    fig.text(0.5,0.016,'INDEPENDENT REIMPLEMENTATION  ·  SIMULATED DATA  ·  T2AV-Compass layout study',
             fontsize=5.35,color=MUTED,ha='center',va='center')
    metadata={'data_status':data['data_status'],'font':family,'font_mode':font,
              'size_inches':[7.2,height],'reference_commit':'7575ae07cf969c3f5d439644ecb9979862370523',
              'data_file':'assets/compass-demo.json','seed':data['seed'],
              'data_sha256':hashlib.sha256((ROOT/'assets/compass-demo.json').read_bytes()).hexdigest(),
              'samples':samples,
              'notes':['Radial length encodes pass rate; baseline starts outside the center disk.',
                       'All seven radial axes use 0–100, higher is better; bar charts use the same table.',
                       'Sunburst allocates one equal angular slot per check; area is not sample frequency.',
                       'Density: 700 synthetic lengths per corpus, Gaussian KDE, Scott bandwidth, reflection at zero.',
                       'Filmstrip, waveform and database glyphs are original schematic vectors.']}
    return fig,metadata


def export(fig,metadata,stem,dpi=450):
    stem=Path(stem)
    stem.parent.mkdir(parents=True,exist_ok=True)
    saved=[]
    for ext in ('png','pdf','svg'):
        path=stem.with_suffix('.'+ext)
        fig.savefig(path,dpi=dpi,facecolor='white')
        saved.append(path)
    path=stem.with_suffix('.json')
    path.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    saved.append(path)
    return saved
