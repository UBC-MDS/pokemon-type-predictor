# author: Tsz Fung Ho
# date: 2022-11-25

"""Creates eda plots for the pre-processed training data from the pokemon.csv 
(from https://gist.github.com/HansAnonymous/56d3c1f8136f7e0385cc781cf18d486c).
Saves the plots as a png file.
Usage: src/pokemon_eda.py --train=<train> --out_dir=<out_dir>
  
Options:
--train=<train>     Path (including filename) to training data 
--out_dir=<out_dir> Path to directory where the plots should be saved
"""

import pandas as pd
import altair as alt
import vl_convert as vlc
# import dataframe_image as dfi
# import  df2img
import os
from docopt import docopt
import matplotlib.pyplot as plt
from pandas.plotting import table


def save_chart(chart, filename, scale_factor=1):
    '''
    Save an Altair chart using vl-convert
    
    Parameters
    ----------
    chart : altair.Chart
        Altair chart to save
    filename : str
        The path to save the chart to
    scale_factor: int or float
        The factor to scale the image resolution by.
        E.g. A value of `2` means two times the default resolution.
    '''
    if filename.split('.')[-1] == 'svg':
        with open(filename, "w") as f:
            f.write(vlc.vegalite_to_svg(chart.to_dict()))
    elif filename.split('.')[-1] == 'png':
        with open(filename, "wb") as f:
            f.write(vlc.vegalite_to_png(chart.to_dict(), scale=scale_factor))
    else:
        raise ValueError("Only svg and png formats are supported")

def main(train, out_dir):

  # check if eda folder exists
  if not os.path.exists(out_dir):
        os.makedirs(out_dir)
  #reads input file  
  train_df = pd.read_csv(train)

  #create data describe table
  describe = train_df.describe().round(3)
  # set up df to save
  fig, ax = plt.subplots(figsize=(30,2)) 
  # no axes
  ax.xaxis.set_visible(False)  
  ax.yaxis.set_visible(False)  
  # no frame
  ax.set_frame_on(False)  
  # plot table
  tab = table(ax, describe, loc='center', colLoc='center', cellLoc='center')  
  plt.savefig(os.path.join(out_dir, 'EDA_data_description.png'), bbox_inches="tight", transparent=True)

  #create png file : distribution of numerical columns
  num_dist = alt.Chart(train_df, title='Distribution of different numerical columns').mark_bar().encode(
     alt.X(alt.repeat(), type='quantitative', bin=alt.Bin(maxbins=40)),
     y='count()',
  ).properties(
    width=300,
    height=200
  ).repeat(
    ['NUMBER','CODE','GENERATION','LEGENDARY','MEGA_EVOLUTION', 'HEIGHT', 'WEIGHT','HP','ATK','DEF','SP_ATK','SP_DEF','SPD','TOTAL'], columns=3
  )
  save_chart(num_dist, os.path.join(out_dir, 'EDA_dist_of_num.png'))

  #create png file : distribution of categorical columns 
  cat_dist = alt.Chart(train_df, title='Distribution of different categorical columns').mark_bar().encode(
     x='count()',
     y=alt.X(alt.repeat()),
  ).properties(
    width=300,
    height=1500
  ).repeat(
    ['TYPE1','TYPE2','COLOR', 'ABILITY1','ABILITY2','ABILITY HIDDEN' ],
    columns=3
  )
  save_chart(cat_dist, os.path.join(out_dir, 'EDA_dist_of_cat.png'))

  #create png file : ABILITY1 vs TYPE1  
  ability_vs_type = alt.Chart(train_df, title='Abilities of Pokemons versus Types of Pokemons').mark_square().encode(
    x='ABILITY1',
    y='TYPE1',
    color='count()',
    size='count()')
  save_chart(ability_vs_type, os.path.join(out_dir, 'EDA_ability_vs_type1.png'))

  #create png file : TYPE1 vs COLOR    
  type_vs_color = alt.Chart(train_df, title='Types of Pokemons versus Colors of Pokemons').mark_square().encode(
    x='TYPE1',
    y='COLOR',
    color='count()',
    size='count()')
  save_chart(type_vs_color, os.path.join(out_dir, 'EDA_type1_vs_color.png'))

  #create png file : Correlation Table
  corr_df = (
    train_df
    .corr('spearman')                   
    .stack()                    
    .reset_index(name='corr')) 

  base = alt.Chart(corr_df, title='Correlation Between Features').mark_rect().encode(
    x=alt.X('level_0', title='Feature'),
    y=alt.Y('level_1', title='Feature')
  ).properties(
    height=600,
    width=600
  )
  
  corr_plot = base.mark_rect().encode(
    color=alt.Color('corr', scale=alt.Scale(scheme="redblue", domainMid=0), title='Correlation')
  )

  text = base.mark_text(color='black').encode( 
    text=alt.Text("corr:Q", format="0.2f")
  )
  corrMatrix_chart = (corr_plot + text)
  save_chart(corrMatrix_chart, os.path.join(out_dir, 'EDA_correlation.png'))


if __name__ == "__main__":
  try:
    opt = docopt(__doc__)
    main(opt["--train"], opt["--out_dir"])
  except:
    print(__doc__)
