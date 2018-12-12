import plotly.plotly as py
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.offline as offline
import plotly.graph_objs as go


#this generates a visualization of the world map based on the CSV file in this subfolder
#this CSV and JSON  were  obtained from the demo on README.md
#example from https://plot.ly/python/choropleth-maps/


iso2iso3=dict()
with open('iso2toiso3.csv', 'r') as f:
    lines=f.readlines()
    for  l in lines:
        sp=l.split(',')
        iso2iso3[sp[0]]= sp[1].strip()

tempFile = open('tempCSV.csv', 'w')
tempFile.write("country,medianRTT\n")

with open('20181212-stats.csv', 'r') as f:
    lines=f.readlines()
    for  l in lines:
        sp=l.split(',')
        cc=sp[0]
        if cc!="country":
            cc3=iso2iso3[cc]
            median=sp[4]
            tempFile.write(cc3+","+median+"\n")


tempFile.close()


df=pd.read_csv('tempCSV.csv',sep=",")

data=[
    dict(
    type = 'choropleth',
    locations = df['country'],
    z=df['medianRTT'],
    colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
     autocolorscale = False,
     reversescale = True,
     marker = dict(
     line = dict (
        color = 'rgb(180,180,180)',
        width = 0.5
        ) ),
    colorbar = dict(
        autotick = False,
        title = 'ms'),
      ) ]



layout = dict(
    title = 'Median RTT for DNS CHAOS Measurement',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
offline.plot( fig, validate=False, filename='rtt.html' )
