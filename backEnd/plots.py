# Back end functions to create the various plots and figures throughout the deshboard
from os import name
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from plotly.graph_objs import layout
from plotly.subplots import make_subplots
from scipy.stats import kde
from scipy.stats.kde import gaussian_kde
import plotly.io as pio

# Colors
BG_WHITE = "#fbf9f4"
GREY_LIGHT = "#b4aea9"
GREY50 = "#7F7F7F"
BLUE_DARK = "#1B2838"
BLUE = "#2a475e"
BLACK = "#282724"
GREY_DARK = "#747473"
RED_DARK = "#850e00"
FIG_WIDTH = 500

# Colors taken from Dark2 palette in RColorBrewer R library
COLOR_SCALE = ["#1B9E77", "#D95F02", "#7570B3"]


pio.templates.default = pio.templates['seaborn']

# Set random seed
np.random.seed(7)

# TABLE SUMMARIES
def isQualitative(df:pd.DataFrame(), column):
    column_types = df.dtypes
    if column_types.loc[column] in ['object']:
        return True
    else:
        return False

def summaryDictionary(df:pd.DataFrame(), column):
    if isQualitative(df, column):
        statistics = ['Total Values', 'Null Values', 'Unique Values', 'Unique Values', 'Unique Counts', 'Mode']
        values = [df[column].count(), df[column].isnull().sum(), df[column].nunique(), df[column].unique(), df[column].value_counts(dropna=False).to_numpy(), df[column].mode().loc[0]]
        return pd.DataFrame({'Statistics':statistics, 'Values':values})
    else:
        statistics = ['Total Values', 'Null Values', 'Unique Values', 'Mode', 'Mean', 'Median', 'Standard Deviation', '25th Quantile', '75th Quantile', 'Minimum', 'Maximum']
        values = [df[column].count(), df[column].isnull().sum(), df[column].nunique(), df[column].mode().loc[0], round(df[column].mean(),2), df[column].quantile(q=0.5), round(df[column].std(),2), df[column].quantile(q=0.25), df[column].quantile(q=0.75), df[column].min(), df[column].max()]
        return pd.DataFrame({'Statistics':statistics, 'Values':values})

def tableStatistics(df:pd.DataFrame(), column):
    fig = go.Figure(layout={
        'autosize': False,
        'width': FIG_WIDTH,
        'height': FIG_WIDTH,
        'plot_bgcolor': BG_WHITE,
        'paper_bgcolor': BG_WHITE
    })
    data = summaryDictionary(df, column)
    fig.add_trace(go.Table(header=dict(values=[key for key in data.keys()], font=dict(size=10)), cells=dict(values=[data[key] for key in data.keys()])))
    fig.update_layout(
        width=FIG_WIDTH,
        showlegend=False
    )
    return fig   

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
        'autosize': False,
        'width': FIG_WIDTH,
        'height': FIG_WIDTH,
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

def distributionPlot(df=pd.DataFrame(), x='', y=''):
    if y:
        fig_data = []
        subgroups = []
        for subgroup in df[y].unique():
            temp_data = df.loc[df[y] == subgroup]
            fig_data.append(temp_data[x])
            subgroups.append(subgroup)
        fig = ff.create_distplot(hist_data=fig_data, group_labels=subgroups, curve_type='kde', show_rug=False)
        fig.update_layout({
            'autosize': False,
            'width': FIG_WIDTH,
            'height': FIG_WIDTH,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE,
            'yaxis_tickformat': ',.0%'          
        })
    else:
        fig = ff.create_distplot(hist_data=[df[x]], group_labels=[x], curve_type='kde', show_rug=False)
        fig.update_layout({
            'autosize': False,
            'width': FIG_WIDTH,
            'height': FIG_WIDTH,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE,
            'showlegend': False,
            'yaxis_tickformat': ',.0%'
        })
    return fig


def histogram(df=pd.DataFrame(), x='', group='', normal=False):
    fig = go.Figure(
        layout={
            'autosize': False,
            'width': FIG_WIDTH,
            'height': FIG_WIDTH,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE
    })
    if group:
        if normal:
            for subgroup in df[group].unique():
                fig.add_trace(go.Histogram(x=df[x][df[group]==subgroup], histnorm='probability', name=subgroup))
            fig.update_layout(barmode='overlay')
            fig.update_traces(opacity=0.5)
        else:
            for subgroup in df[group].unique():
                fig.add_trace(go.Histogram(x=df[x][df[group]==subgroup], name=subgroup))
            fig.update_layout(barmode='overlay')
            fig.update_traces(opacity=0.5)
    else:
        if normal:
            fig.add_trace(go.Histogram(x=df[x], histnorm='probability'))
        else:
            fig.add_trace(go.Histogram(x=df[x]))
    return fig
            
def boxPlot(df=pd.DataFrame(), x='', group=''):
    fig = go.Figure(
        layout={
            'autosize': False,
            'width': 500,
            'height': 500,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE
        }
    )
    if group:
        for subgroup in df[group].unique():
            fig.add_trace(
                go.Box(
                    y=df[x][df[group]==subgroup], 
                    name=subgroup, 
                    boxmean=True, 
                    fillcolor=BG_WHITE,
                    boxpoints='all', 
                    line={
                        'width': 1.5
                    },
                    jitter=0.3, 
                    pointpos=0
                ))
        fig.update_traces(opacity=0.5)
    else:
        fig.add_trace(
            go.Box(
                y=df[x],
                name=x,
                boxmean=True, 
                fillcolor=BG_WHITE,
                boxpoints='all', 
                line={
                    'color': 'black',
                    'width': 1.5
                },
                jitter=0.3, 
                pointpos=0
            ))
    return fig

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
def barPlot(df:pd.DataFrame(), column):
    unique = df[column].unique()
    counts = df[column].value_counts(dropna=False)
    fig = go.Figure(
        layout={
            'autosize': False,
            'width': 500,
            'height': 500,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE
        }
    )
    fig.add_trace(go.Bar(x=unique, y=counts))
    return fig 
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
def pieChart(df:pd.DataFrame(), column):
    fig = go.Figure(
        layout={
            'autosize': False,
            'width': 500,
            'height': 500,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE
        }
    )
    fig.add_trace(go.Pie(labels=df[column].unique(), values=df[column].value_counts(dropna=False).to_numpy()))
    return fig

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

# Sub Plots
def descriptiveStatistics(df:pd.DataFrame(), column):
    data = summaryDictionary(df, column)
    if isQualitative(df, column):
        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'table'},{'type':'bar'},{'type':'pie'}]])
        fig.add_trace(go.Table(header=dict(values=[key for key in data.keys()], font=dict(size=10)), cells=dict(values=[data[key] for key in data.keys()])), row=1, col=1)
        unique = df[column].unique()
        counts = df[column].value_counts(dropna=False)
        fig.add_trace(go.Bar(x=unique, y=counts, showlegend=False), row=1, col=2)
        fig.add_trace(go.Pie(labels=df[column].unique(), values=df[column].value_counts().to_numpy()), row=1, col=3)
        fig.update_layout(legend=dict(yanchor='middle'), title_text='Descriptive Statistics for '+ column)
        return fig
    else:
        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'table'},{'type':'scatter', 'type':'scatter'},{'type':'box'}]])
        fig.add_trace(go.Table(header=dict(values=[key for key in data.keys()], font=dict(size=10)), cells=dict(values=[data[key] for key in data.keys()])), row=1, col=1)
        dist = ff.create_distplot(hist_data=[df[column]], group_labels=[column], bin_size=round(df[column].std(),2)/3, show_rug=False)
        dist.update_layout({
            'autosize': False,
            'width': FIG_WIDTH,
            'height': FIG_WIDTH,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE,
            'showlegend': False,
            'yaxis_tickformat': ',.0%'
        })
        for item in dist['data']:
            item.pop('xaxis', None)
            item.pop('yaxis', None)
        fig.append_trace(dist['data'][0], 1, 2)
        fig.append_trace(dist['data'][1], 1, 2)
        fig.add_trace(go.Box(y=df[column],boxmean=True, fillcolor=BG_WHITE, boxpoints='all', line={'color': 'black','width': 1.5}, jitter=0.3, pointpos=0), row=1, col=3)
        fig.update_layout(showlegend=False, title_text='Descriptive Statistics for '+ column)
        return fig
    
def descriptiveDistributions(df:pd.DataFrame(), feature, groups):
    spec = [{'type':'scatter', 'type':'scatter'}]*len(groups)
    fig = make_subplots(rows=1, cols=len(groups), specs=[spec])
    for index, sub_feature in enumerate(groups):
        fig_data = []
        subgroups = []
        for subgroup in df[sub_feature].unique():
            temp_data = df.loc[df[sub_feature] == subgroup]
            fig_data.append(temp_data[feature])
            subgroups.append(subgroup)
        dist = ff.create_distplot(hist_data=fig_data, group_labels=subgroups, bin_size=round(df[feature].std(),2)/3, show_rug=False)
        dist.update_layout({
            'autosize': False,
            'width': FIG_WIDTH,
            'height': FIG_WIDTH,
            'plot_bgcolor': BG_WHITE,
            'paper_bgcolor': BG_WHITE,
            'yaxis_tickformat': ',.0%'          
        })
        for item in dist['data']:
            item.pop('xaxis', None)
            item.pop('yaxis', None)
        for count in range(len(dist['data'])):
            fig.append_trace(dist['data'][count], 1, index+1)
    fig.update_layout(title_text='Descriptive Statistics for '+ feature)
    return fig