import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
from ..utils.firebase import firebaseAPI


def draw_barchart(year):
    dff = df[df['year'].eq(year)].sort_values(by='value', ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['name'], dff['value'], color=[colors[group_lk[x]] for x in dff['name']])
    dx = dff['value'].max() / 200
    for i, (value, name) in enumerate(zip(dff['value'], dff['name'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
        ax.text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
    # ... polished styles
    ax.text(1, 0.4, year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Population (thousands)', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, 'The most populous cities in the world from 1500 to 2018',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by @pratapvardhan; credit @jburnmurdoch', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)




if __name__ == "__main__":

    # Import data
    df = pd.read_csv('https://gist.githubusercontent.com/johnburnmurdoch/4199dbe55095c3e13de8d5b2e5e5307a/raw/fa018b25c24b7b5f47fd0568937ff6c04e384786/city_populations', 
                    usecols=['name', 'group', 'year', 'value'])

    current_year = 2018
    dff = (df[df['year'].eq(current_year)]
        .sort_values(by='value', ascending=True)
        .head(10))

    # Color used in plot
    colors = dict(zip(
        ['India', 'Europe', 'Asia', 'Latin America',
        'Middle East', 'North America', 'Africa'],
        ['#adb0ff', '#ffb3ff', '#90d595', '#e48381',
        '#aafbff', '#f7bb5f', '#eafb50']
    ))
    # Map name to group
    group_lk = df.set_index('name')['group'].to_dict()

    
    fig, ax = plt.subplots(figsize=(15, 8))

    animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1968, 2019))
    HTML(animator.to_jshtml()) 
    # or use animator.to_html5_video() or animator.save()
