import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from itertools import cycle 
from mycolorpy import colorlist as mcp
import matplotlib.ticker as ticker
from sklearn.linear_model import LinearRegression

def set_style(context='talk'):
  sns.set_context(context)
  
def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"
  
def annotate(fg, df, x, y, **kwargs):
  countries = kwargs.pop('countries',None)
  if countries:
    sample = df.loc[countries,:]
    colors = cycle(mcp.gen_color(cmap="tab10", n=10))

    for id, row in sample.iterrows():
      fg.ax.scatter([row[x]],[row[y]],c=next(colors), label=id)

    plt.legend()
    sns.move_legend(fg.ax, "upper left", bbox_to_anchor=(1, 1))
    fg.ax.yaxis.set_major_formatter(ticker.EngFormatter())
    fg.ax.set_xlim(0,2)
  
def plot_correlation(df, x, y, fnc, corr=False, regfit=False, res=False, **kwargs):
  fg = sns.relplot(data=df, x=x, y=y, color='lightgrey', height=4, aspect=1.2)
  if corr:
    r, p = pearsonr(df[x], df[y])
    fg.ax.text(s=f"r={r:.2f}{convert_pvalue_to_asterisks(p)}\nn={df.shape[0]}", 
               x=.05, y=0.9, ha='left', va='top', transform=fg.ax.transAxes);
    
  p1, p0 = np.polyfit(df[x].values, df[y].values, deg=1)  # slope, intercept
  
  if regfit:  
    fg.ax.axline(xy1=(0, p0), slope=p1, color='r', lw=2)
    
    r2s = ''
    if res:
      residuals = []
      for i,(c,row) in enumerate(df.iterrows()):
        yhat = p0 + (p1 * row[x])
        fg.ax.plot([row[x],row[x]], [row[y],yhat], color='black', lw=1, ls='--')    
        residuals.append(row[y]-yhat)
      r2s = f"\n$R^2={1-(np.var(residuals)/np.var(df[y])):.2f}$"
      
    s = "\hat{y}"
    s = f'${s} = {p0:.1f}+{p1:.1f} x$'
    s = f"{s}{r2s}"
    fg.ax.set_title(s)
    
  fg.ax.set_ylim((p0-20e2,df[y].max()+20e2))
  fg.ax.set_xlim((0-0.1,df[x].max()+0.1))
    
  fnc(fg, df, x, y, **kwargs)
  return fg
