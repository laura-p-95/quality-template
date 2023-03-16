import pandas as pd
import plotly as pl
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.figure_factory as ff
import missingno as msno
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np


# nomicolonne = list(df.select_dtypes(include='int64').columns)
# contenutocolonne = df.select_dtypes(include='int64')

# nomecolonnadue = nomicolonne[2]
# contenutocolonnadue = contenutocolonne[contenutocolonne.columns[2]]

def boxPlot(df,typeNUMlist):
    numeric_cols_content = df.select_dtypes(include=['int64','float64'])
    numeric_cols_names = list(numeric_cols_content.columns)
    num = len(typeNUMlist)
    
    html_files = []

    for i in range(num):
        fig=go.Figure(data=go.Box(
                x=numeric_cols_content[numeric_cols_content.columns[i]], 
                name="",
                boxpoints="outliers"
            ))
        fig.update_layout(
        autosize=True,
        height = 90,
        showlegend=False,
        margin=dict(
            l=5,
            r=10,
            b=5,
            t=30
        ),
        font = dict(color = '#ced4da'),
        paper_bgcolor="#27293d",
        )
        filename = f"apps/templates/home/Plots/boxPlot_{i}.html"
        name = f"home/Plots/boxPlot_{i}.html"
        pl.offline.plot(fig, filename = filename, auto_open=False)
        html_files.append(name)

    return html_files





def distributionPlot(df,typeNUMlist):
    numeric_cols_content = df.select_dtypes(include=['int64','float64'])
    numeric_cols_names = list(numeric_cols_content.columns)
    num = len(typeNUMlist)
    # Create a list to hold the figures
    fig_list = []
    
    
    # Loop through each variable in the DataFrame
    for var in  df.select_dtypes(include=['int64','float64']):
        #Filter out Nans and infs
        data = df[var][~df[var].isin([float('nan'), float('inf'), -float('inf')])]

        # Create a new figure
        fig = ff.create_distplot([data], [var])

        # Update the layout of the figure
        fig.update_layout(xaxis_title='Value', yaxis_title='Density', width=600, autosize=True,)

        # Add the figure to the list
        fig_list.append(fig)

    # Add each figure to the appropriate subplot
    for i, fig in enumerate(fig_list):
        fig.update_layout(showlegend=False, font = dict(color = '#ced4da'), paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30))
        fig_json = fig.to_plotly_json()
        fig_obj = go.Figure(fig_json['data'], fig_json['layout'])
        fig_obj.update_layout(height=300, width=600)
        fig_obj.update_traces(marker=dict(color='#1f77b4'))
        fig_obj.update_yaxes(title_text='Density')
        fig_obj.update_xaxes(title_text='Value')

    html_files = []
        
    for i in range(num):
        filename = f"apps/templates/home/Plots/distributionPlot_{i}.html"
        name = f"home/Plots/distributionPlot_{i}.html"
        plot = pl.offline.plot(fig_list[i], filename = filename, auto_open=False)
        html_files.append(name)
    
    return html_files




def distributionCategorical(df,typeCATlist):
    # Read in the JSON file created by pandas profiling
    html_files = []
    num=0

    for var in typeCATlist:
            vc = df[var].value_counts()
            vc_df = pd.DataFrame({'var': vc.index, 'count': vc.values})
            fig = px.bar(vc_df, x='var', y='count')
            fig.update_layout(xaxis_title='Value', yaxis_title='Count', width=600, autosize=True, font = dict(color = '#ced4da'), paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30))
            
            filename = f"apps/templates/home/Plots/barCATPlot_{num}.html"
            name = f"home/Plots/barCATPlot_{num}.html"
            pl.offline.plot(fig, filename = filename, auto_open=False)
            html_files.append(name)
            num=num+1
    
    return html_files



def heatmap(df):
     # correlation data
    h_table = df.corr(method ='pearson')
    h_table = round(h_table,2)
    context = {'h_table': h_table}

    # Create the heatmap trace using Plotly
    fig = px.imshow(h_table, x=h_table.index, y=h_table.columns, text_auto=True, aspect="auto")
    fig.update_xaxes(side="top")
    fig.update_layout(font = dict(color = '#ced4da'), paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30))
    pl.offline.plot(fig, filename = 'apps/templates/home/Plots/heatmap.html', auto_open=False)
    return fig
    

    
    # trace = go.Heatmap(x=h_table.index, y=h_table.columns, z=h_table.values)
    # annotations = go.Annotations()

    # # Create the layout
    # layout = go.Layout(yaxis=dict(autorange="reversed"), xaxis=dict(side="top"),
    #                    annotations=annotations, 
    #                    margin=dict(l=5,r=10,b=5,t=30),font = dict(color = '#ced4da'),
    #                     paper_bgcolor="#27293d")

    # fig = go.Figure(data=[trace], layout=layout)
    

def missing_data(df):

    # Generate missing data visualization using missingno
    fig_matrix = msno.matrix(df, color=(0.329, 0.059, 0.286),  fontsize=12)
    # fig_bar = msno.bar(df, color=(0.329, 0.059, 0.286),  fontsize=12)

    img_url = []

    # Generate the plot from the missingness matrix
    # fig_b = fig_bar.get_figure()
    # img_b = 'apps/static/assets/img/bars.png'
    # fig_b.savefig(img_b, format='png')

    fig_m = fig_matrix.get_figure()
    img_m = 'apps/static/assets/img/matrix.png'
    fig_m.savefig(img_m, format='png')

    #for the heatmap
    df = df.iloc[:, [i for i, n in enumerate(np.var(df.isnull(), axis='rows')) if n > 0]]
    corr_mat = df.isnull().corr()
    corr_mat = round(corr_mat,2)
    fig_heat = px.imshow(corr_mat, x=corr_mat.index, y=corr_mat.columns, text_auto=True, aspect="auto", color_continuous_scale='bupu')
    fig_heat.update_xaxes(side="top")
    fig_heat.update_layout(font = dict(color = '#ced4da'), paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30))
    pl.offline.plot(fig_heat, filename = 'apps/templates/home/Plots/heatmap_missing_values.html', auto_open=False)


def treePlot(df, typeCATlist):
    html_files = []
    num=0
      

    for var in typeCATlist:
            vc = df[var]
            vc_df = pd.DataFrame({'var': vc.index, 'info': vc.values})
            fig = px.treemap(vc_df.head(30), path=['var'], values='info')
            fig.update_layout(width=500, autosize=True, font=dict(color='#ced4da'), paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30))
    
            filename = f"apps/templates/home/Plots/barCATPlot_{num}.html"
            name = f"home/Plots/barCATPlot_{num}.html"
            pl.offline.plot(fig, filename = filename, auto_open=True)
            html_files.append(name)
            num=num+1
    
    return html_files


def table_df(df):
    
    num_cols = df.shape[1]

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#db2dc0',
                    align='left',
                    font=dict(color='white', size=12)), 
        cells=dict(values=[df.iloc[:, i] for i in range(num_cols)],
                fill_color='lavender',
                align='left',
                font = dict(color = '#555')))
    ])
    fig.update_layout(autosize=True, height=700,
                      paper_bgcolor="#27293d", margin=dict(l=5, r=10, b=5, t=30)
                    
                      )
    pl.offline.plot(fig, filename = 'apps/templates/home/Plots/table_df.html', auto_open=False)