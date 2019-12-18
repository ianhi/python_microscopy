%matplotlib widget
# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook as tqdm
from matplotlib import rc
rc("font", family = "serif",size=20)
rc("figure",figsize=(9,6))
rc("figure",facecolor="white")
%config InlineBackend.figure_format = 'retina'

# %load_ext autoreload
# %autoreload 2
import skimage.io as io
import re
import os
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from skimage import io
from skimage.color import rgb2grey
from skimage.filters import sobel

def imread_convert(f):
    return rgb2grey(io.imread(f))

def reduce(arr,column,function=np.mean):
    #calc new dtype
    dtype = dict(arr.dtype.fields) #make a shallow copy
    dtype.pop(column)
    dtype.pop('name')

    #which identifying columsn will survive
    remaining_identifiers = [i for i in dtype.keys()  if i not in [column,'name','image']]

    #get number of unique entries in output
    unique = np.unique(arr[remaining_identifiers])
    # i think that this will preserve order??

    col = arr[column]
    #need unique remaining indentify columns


    out = np.zeros(len(unique),dtype= dtype)
    print(dtype)
    for i,v in enumerate(unique):
        ind = arr[remaining_identifiers]==v
        #get indices ind = col == i
        im = function(arr['image'][ind])

        out[i] = (*v,im)
    return out
def pos_timelapse(arr,pos=0):
    """
    Assumes the first column is 'pos' and the second column is time steps
    """
    idx = arr['pos']==pos
    fig = plt.figure(f"position {pos}")
    im = plt.imshow(arr[idx][0]['image'])
    def on_value_change(change):
        i = change['new']
        im.set_data(arr[idx][i]['image'])
        fig.canvas.draw()
    slider = widgets.IntSlider(min=0, max=np.sum(idx)-1, step=1, continuous_update=True)
    play = widgets.Play(min=0,max=np.sum(idx)-1, interval=200,_repeat=True,_playing=True,step=1)

    slider.observe(on_value_change, 'value')
    widgets.jslink((play, 'value'), (slider, 'value'))
    return widgets.HBox([play,slider])

def choose_pos_timelapse(arr,pos=0):
    """
    Assumes the first column is 'pos' and the second column is time steps
    """
    idx = arr['pos']==pos
    fig = plt.figure(f"position {pos}")
    im = plt.imshow(arr[idx][0]['image'])
    positions = np.unique(arr['pos'])
    pos_widget = widgets.Dropdown(
        options=positions,
        value=positions[0],
        description='Position:',
        disabled=False,
    )
    t_slider = widgets.IntSlider(min=0, max=np.sum(idx)-1, step=1)#, continuous_update=True)
    t_play = widgets.Play(min=0, max=np.sum(idx)-1,interval=200,_repeat=True,step=1)
    def redraw(*args):
        idx = arr['pos']==pos_widget.value
        i = t_slider.value
        im.set_data(arr[idx][i]['image'])
        fig.canvas.draw()

    def on_value_change(change):
        redraw()
#         i = change['new']
#         idx = arr['pos']==pos_widget.value
# #         print(i)
#         im.set_data(arr[idx][i]['image'])
#         fig.canvas.draw()

    def update_t_range(*args):
#         print(np.sum(arr['pos']==pos_widget.value))
        t_slider.max = np.sum(arr['pos']==pos_widget.value)-1
        redraw()

    widgets.jslink((t_slider, 'value'),(t_play, 'value') )
    pos_widget.observe(update_t_range,'value')
    t_slider.observe(on_value_change, 'value')
    time_box = widgets.HBox([t_play,t_slider])
    ui = widgets.VBox([pos_widget, time_box])
    return ui
def int_imshow_interact(arr,title_col=None):
#     play = widget.Play()
    i_widget = widgets.IntSlider(min=0,max=len(arr)-1,value=0)
    fig = plt.figure()
    ax = plt.gca()
    im = plt.imshow(arr[0]['image'])

    def update(i):
        if title_col is not None:
            ax.set_title(f"{title_col} = {arr[i][title_col]}")
        im.set_data(arr[i]['image'])
        fig.canvas.draw()
    interact(update,i=i_widget)
def milli2min(ms):
    return ms/(1000*60)
def milli2hr(ms):
    return ms/(1000*60*60)
def min2hr(min):
    return min/60
# int_imshow_interact(out,title_col='time')

im = filters.gaussian(elevation_map,sigma=3)

tolerance = .01

# fig = plt.figure()
# ax = plt.gca()
class yikes:
    def __init__(self):
#         plt.imshow
        self.positions = []
        self.circles = []
        self.tolerance_widget = widgets.FloatText(
            value=tolerance,
            description='tolerance:',
            disabled=False,
            step=.1
        )
        recalc = widgets.Checkbox(
            value=False,
            description='Recalc on change',
            disabled=False
        )
        plt.clf()
        self.fig = plt.figure('yikes')
        self.ax = plt.gca()
        self.displayed = self.ax.imshow(im)

        self.tolerance_widget.observe(self.set_tol,'value')
        self.tolerance=.01
        self.ix = 0
        self.iy = 0

        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event)) # if you call self.onclick here the figure will render when object is created
    def onclick(self,event):
        print(self.tolerance)
        self.ix, self.iy = event.xdata, event.ydata
        self.filled = flood_fill(im,(int(self.iy),int(self.ix)),new_value=255,tolerance=self.tolerance)
        self.displayed.set_data(self.filled)

        c = plt.Circle((self.ix,self.iy),5,color='r')
        self.circles.append(c)
        self.ax.add_artist(c)
        self.positions.append((self.ix, self.iy))
        self.fig.canvas.draw()

    def set_tol(self,change):
        self.tolerance
        self.tolerance = change['new']
    def _ipython_display_(self):
        display(widgets.VBox([self.fig.canvas,self.tolerance_widget]))

plt.close('all')
y = yikes()
y
# plt.show()
# widgets.HBox([tolerance_widget,recalc])
