# Back end functions to create the various plots and figures throughout the deshboard
from os import name
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# Colors
BG_WHITE = "#fbf9f4"
GREY_LIGHT = "#b4aea9"
GREY50 = "#7F7F7F"
BLUE_DARK = "#1B2838"
BLUE = "#2a475e"
BLACK = "#282724"
GREY_DARK = "#747473"
RED_DARK = "#850e00"

# Colors taken from Dark2 palette in RColorBrewer R library
COLOR_SCALE = ["#1B9E77", "#D95F02", "#7570B3"]

# Distribution
def violinPlot(df=pd.DataFrame(), x='', y='', group_by=False, horizontal_lines=[]):
    shapes = []
    for hline in horizontal_lines:
        shapes.append({
            'type': 'line',
            'xref': 'paper',
            'x0': 0,
            'y0': hline,
            'x1': 1,
            'y1': hline,
            'opacity': 0.8,
            'line': {
                'color': GREY50,
                'dash': 'longdash'
            }
        })
    fig = go.Figure(layout={
        'plot_bgcolor': BG_WHITE,
        'paper_bgcolor': BG_WHITE,
        'shapes': shapes
    })
    
    if group_by:
        for subgroup in df[x].unique():
            fig.add_trace(go.Violin(
                x=df[x][df[x]==subgroup], 
                y=df[y][df[x]==subgroup], 
                box={
                    'visible':True,
                    'width': .3,
                    'fillcolor': BG_WHITE,
                    'line': {
                        'color': 'black',
                        'width': 1.4
                    }
                },
                fillcolor=BG_WHITE,
                bandwidth=0.75,
                meanline_visible=True, 
                name=subgroup, 
                line={
                    'width':1.45
                    },
                points='all',
                marker={
                    'size':8
                },
                jitter=0.3,
                pointpos=0
                ))
    else:
        fig.add_trace(go.Violin(
            x=df[x], 
            y=df[y], 
            box={
                'visible':True,
                'width': .3,
                'fillcolor': BG_WHITE,
                'line': {
                    'color': 'black',
                    'width': 1.4
                }
            },
            fillcolor=BG_WHITE,
            bandwidth=0.75,
            meanline_visible=True,
            line={
                'width':1.45
                },
            points='all',
            marker={
                'size':8
            },
            jitter=0.3,
            pointpos=0
            ))
    return fig

def densityPlot(df=pd.DataFrame(), x='', y=''):
    fig = ff.create_distplot(df[x], x)
    print(y)
    return fig

def histogram(df=pd.DataFrame(), x='', group_by=False, group='', normal=False):
    fig = go.Figure(layout={
        'plot_bgcolor': BG_WHITE,
        'paper_bgcolor': BG_WHITE
    })
    if group_by:
        if normal:
            for subgroup in df[group].unique():
                fig.add_trace(go.Histogram(x=df[x][df[group]==subgroup], histnorm='probability'))
            fig.update_layout(barmode='overlay')
            fig.update_traces(opacity=0.5)
        else:
            for subgroup in df[group].unique():
                fig.add_trace(go.Histogram(x=df[x][df[group]==subgroup]))
            fig.update_layout(barmode='overlay')
            fig.update_traces(opacity=0.5)
    else:
        if normal:
            fig.add_trace(go.Histogram(x=df[x], histnorm='probability'))
        else:
            fig.add_trace(go.Histogram(x=df[x]))
    return fig
            
def boxPlot():
    return
def ridgeLine():
    return

# Correlation
def scatterPlot():
    return
def heathMap():
    return
def correlogram():
    return
def bubblePlot():
    return
def densityPlot():
    return

# Ranking
def barPlot():
    return
def radarPlot():
    return
def wordCloud():
    return
def parallelPlot():
    return
def lollipop():
    return
def circularBarPlot():
    return

# Part of Whole
def treeMap():
    return
def vennDiagram():
    return
def donut():
    return
def pieChart():
    return
def dendrogram():
    return
def circularPacking():
    return

# Evolution
def lineChart():
    return
def areaChart():
    return
def stackedArea():
    return
def streamGraph():
    return
def timeSeries():
    return

