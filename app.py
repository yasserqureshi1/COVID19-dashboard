import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df1 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/confirmed')
df2 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/deaths')
df3 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/recovered')

df = pd.json_normalize(df1['locations'])

a = df.groupby(by='country').agg({'latest': 'sum', 'country_code': 'min'}).reset_index()
# dfcountry = pd.read_csv('countryMap.txt', sep='\t')
dfcountry = pd.read_csv(
    'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv')
dff = a.merge(dfcountry, how='inner', left_on=['country_code'], right_on=['alpha-2'])
# dff = a.merge(dfcountry, how='inner', left_on=['country_code'], right_on=['2let'])

sortedtable = a.sort_values(by='latest', ascending=False, ignore_index=True)

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

continent = dict(Asia=0, Americas=0, Europe=0, Africa=0, Oceania=0)
for i in continent:
    for j in range(len(dff)):
        if i == dff.region[j]:
            continent[i] = continent[i] + dff.latest[j]

app.layout = html.Div([
    html.Div(id='top', children=[
        html.Div(id='topleft', className='four columns', children=[
            html.Div(id='title', children=[html.H1(
                children='COVID19 Dashboard', style={'font-family': 'Helvetica'}
            )]),
            html.Div(id='description', children=[html.P(
                children=['Data is analysed from the following sources:', html.Br(),
                          ' - John Hopkins University', html.Br(),
                          ' - Conference of State Bank Supervisors', html.Br(),
                          ' - New York Times'],
                style={'font-family': 'Helvetica'}
            )]),
            html.Div(id='worldstats', children=[
                html.Div(id='piechart', className='five columns', children=[
                    # dcc.Graph(
                    #     figure=go.Figure(
                    #         data=go.Pie(
                    #             labels=['Confirmed', 'Deaths', 'Recovered'],
                    #             values=[df1.latest[1], df2.latest[1], df3.latest[1]],
                    #             textinfo='label+value',
                    #             showlegend=False,
                    #
                    #         ),
                    #         layout=go.Layout(
                    #             margin=go.layout.Margin(
                    #                 l=10,
                    #                 r=10,
                    #                 b=40,
                    #                 t=40,
                    #                 pad=0
                    #             ),
                    #             title_text='Worldwide Cases'
                    #         ),
                    #     ),
                    #     config={"displayModeBar": False}
                    # )
                    html.H6([' ', html.Br()], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H6(['CONFIRMED:'], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H4([df1.latest[1]], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H6(['DEATHS:'], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H4([df2.latest[1]], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H6(['RECOVERED:'], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                    html.H4([df3.latest[1]], style={'textAlign': 'center', 'font-family': 'Helvetica'}),
                ]),
                html.Div(id='continents', className='seven columns', children=[
                    dcc.Graph(id="Continents Data",
                              figure={
                                  'data': [
                                      {'x': ['Africa', 'Asia', 'Europe', 'Americas', 'Oceania'],
                                       'y': [continent['Africa'], continent['Asia'], continent['Europe'],
                                             continent['Americas'], continent['Oceania']],
                                       'type': 'bar'}
                                  ],
                                  'layout': {
                                      'title': 'Continents:',
                                      'margin': dict(
                                          l=40,
                                          r=30,
                                          b=60,
                                          t=60,
                                          pad=4)
                                  }

                              },
                              config={"displayModeBar": False}
                              )
                ])
            ])]),

        html.Div(id='topright', className='eight columns', children=[
            html.Div([
                html.Div(id='titlebar', className='six columns',
                         children=[html.H6(children=['Search by Country:'], style={'font-family': 'Helvetica'})]),
                html.Div(id='creds', className='six columns',
                         children=[html.H6(['Created by Yasser Qureshi'])])
            ]),
            html.Div(id='countryinput', children=[
                dcc.Input(
                    id='confirmed',
                    type='text',
                    placeholder='Country',
                )
            ]),
            html.Div(id='plots', children=[
                html.Div(id='plotofcases', className='six columns'),
                html.Div(id='plotofrate', className='six columns')
            ]),
            html.Div(id='stats')
        ]),
    ]),

    html.Div(id='empty', className='row', children=''),

    html.Div(id='bottom', children=[
        html.Div(id='map', className='six columns', children=[
            html.H6(children=['World Map:'], style={'font-family': 'Helvetica', 'textAlign': 'center'}),
            dcc.Graph(id='map-display',
                      figure={
                          'data': [go.Choropleth(
                              locations=dff['alpha-3'],
                              z=dff['latest'],
                              text=dff['country'],
                              colorscale='sunset',
                              autocolorscale=False,
                              reversescale=True,
                              marker_line_color='darkgray',
                              marker_line_width=0.5,
                              colorbar_title='Cases',
                          )],
                          'layout': dict(
                              title_text='World Map of Cases',
                              geo=dict(
                                  showframe=False,
                                  showcoastlines=True,
                                  projection_type='equirectangular'),
                              margin=dict(
                                  l=5,
                                  r=5,
                                  b=0,
                                  t=0,
                                  pad=2
                              ),
                              autosize=False
                          )
                      },
                      config={"displayModeBar": False}
                      )]
                 ),

        html.Div(id='table', className='four columns', children=[
            html.H6(['Ranked Table:'], style={'font-family': 'Helvetica', 'textAlign': 'center'}),
            html.Table(
                [html.Tr([html.Th(col) for col in sortedtable.columns])] +
                # Body
                [html.Tr([
                    html.Td(sortedtable.iloc[i][col]) for col in sortedtable.columns
                ]) for i in range(min(len(sortedtable), 10))],
                style={
                    'margin-left': 100,
                    'margin-right': 'auto'}

            )
        ])
    ])
])


@app.callback(
    Output("plotofcases", "children"),
    [Input("confirmed", "value")]
)
def plotofcases(country):
    for i in range(len(df1)):
        if country == '':
            x1 = 1
            y1 = 1
            break
        if df1.loc[i, 'locations']['province'] == country:
            a = df1.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x1: object
            x1, y1 = zip(*a)
            break
        elif df1.loc[i, 'locations']['country'] == country:
            if df1.loc[i, 'locations']['province'] == '':
                a = df1.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x1: object
                x1, y1 = zip(*a)
                break
        else:
            x1 = 1
            y1 = 1

    for i in range(len(df2)):
        if country == '':
            x2 = 1
            y2 = 1
            break
        if df2.loc[i, 'locations']['province'] == country:
            a = df2.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x2: object
            x2, y2 = zip(*a)
            break
        elif df2.loc[i, 'locations']['country'] == country:
            if df2.loc[i, 'locations']['province'] == '':
                a = df2.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x2: object
                x2, y2 = zip(*a)
                break
        else:
            x2 = 1
            y2 = 1

    for i in range(len(df3)):
        if country == '':
            x3 = 1
            y3 = 1
            break
        if df3.loc[i, 'locations']['province'] == country:
            a = df3.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x3: object
            x3, y3 = zip(*a)
            break
        elif df3.loc[i, 'locations']['country'] == country:
            if df3.loc[i, 'locations']['province'] == '':
                a = df3.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x3: object
                x3, y3 = zip(*a)
                break
        else:
            x3 = 1
            y3 = 1

    return dcc.Graph(id=f"{country} Data",
                     figure={
                         'data': [
                             {'x': x1, 'y': y1, 'type': 'line', 'name': 'Confirmed'},
                             {'x': x2, 'y': y2, 'type': 'line', 'name': 'Deaths'},
                             {'x': x3, 'y': y3, 'type': 'line', 'name': 'Recovered'}
                         ],
                         'layout': {
                             'title': 'Plot of Cases:',
                             'margin': dict(
                                 l=40,
                                 r=40,
                                 b=70,
                                 t=50,
                                 pad=3
                             ),
                             'autosize': 'False'
                         }
                     },
                     config={"displayModeBar": False}
                     )


@app.callback(
    Output("plotofrate", 'children'),
    [Input('confirmed', 'value')]
)
def plotofrate(country):
    for i in range(len(df1)):
        if country == '':
            xrate = [1, 1]
            rate = 1
            break
        if df1.loc[i, 'locations']['province'] == country:
            a = df1.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x1: object
            x1, y1 = zip(*a)
            rate = []
            for j in range(len(y1) - 1):
                rate.append(int(y1[j + 1]) - int(y1[j]))
            xrate = x1[1:]
            break
        elif df1.loc[i, 'locations']['country'] == country:
            if df1.loc[i, 'locations']['province'] == '':
                a = df1.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x1: object
                x1, y1 = zip(*a)
                rate = []
                for j in range(len(y1) - 1):
                    rate.append(int(y1[j + 1]) - int(y1[j]))
                xrate = x1[1:]
                break
        else:
            rate = 1
            xrate = [1, 1]

    for i in range(len(df2)):
        if country == '':
            x1rate = [1, 1]
            rate1 = 1
            break
        if df1.loc[i, 'locations']['province'] == country:
            a = df2.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x1: object
            x1, y1 = zip(*a)
            rate1 = []
            for j in range(len(y1) - 1):
                rate1.append(int(y1[j + 1]) - int(y1[j]))
            x1rate = x1[1:]
            break
        elif df2.loc[i, 'locations']['country'] == country:
            if df2.loc[i, 'locations']['province'] == '':
                a = df2.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x1: object
                x1, y1 = zip(*a)
                rate1 = []
                for j in range(len(y1) - 1):
                    rate1.append(int(y1[j + 1]) - int(y1[j]))
                x1rate = x1[1:]
                break
        else:
            rate1 = 1
            x1rate = [1, 1]

    return dcc.Graph(id=f"{country} Rate",
                     figure={
                         'data': [
                             {'x': xrate, 'y': rate, 'type': 'line', 'name': 'Confirmed'},
                             {'x': x1rate, 'y': rate1, 'type': 'line', 'name': 'Deaths'}
                         ],
                         'layout': {
                             'title': 'Cases by Day:',
                             'margin': dict(
                                 l=40,
                                 r=40,
                                 b=70,
                                 t=50,
                                 pad=3
                             ),
                             'autosize': 'False'
                         }
                     },
                     config={"displayModeBar": False}
                     )


@app.callback(
    Output("stats", "children"),
    [Input("confirmed", "value")]
)
def stats(country):
    for i in range(len(df1)):
        if country == '':
            y1 = [0]
            break
        if df1.loc[i, 'locations']['province'] == country:
            a = df1.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x1: object
            x1, y1 = zip(*a)
            break
        elif df1.loc[i, 'locations']['country'] == country:
            if df1.loc[i, 'locations']['province'] == '':
                a = df1.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x1: object
                x1, y1 = zip(*a)
                break
            else:
                y1 = [0]
        else:
            y1 = [0]

    for i in range(len(df2)):
        if country == '':
            y2 = [0]
            break
        if df2.loc[i, 'locations']['province'] == country:
            a = df2.loc[i, 'locations']['history']
            a = sorted(a.items(), key=lambda p: p[1], reverse=False)
            x2: object
            x2, y2 = zip(*a)
            break
        elif df2.loc[i, 'locations']['country'] == country:
            if df2.loc[i, 'locations']['province'] == '':
                a = df2.loc[i, 'locations']['history']
                a = sorted(a.items(), key=lambda p: p[1], reverse=False)
                x2: object
                x2, y2 = zip(*a)
                break
            else:
                y2 = [0]
        else:
            y2 = [0]

    if len(y1) > 1:
        x1 = ((y1[-1] - y1[-2]) / y1[-1]) * 100
        x1 = format(x1, '7.2f')
    else:
        x1 = 0

    if len(y2) > 1:
        x2 = ((y2[-1] - y2[-2]) / y2[-1]) * 100
        x2 = format(x2, '7.2f')
    else:
        x2 = 0

    for i in range(len(sortedtable)):
        if sortedtable.loc[i, 'country'] == country:
            rank = i + 1
            break
        else:
            rank = 0

    return html.Div([
        html.Div([
            html.Div(style={'textAlign': 'center', 'font-family': 'Helvetica'}, children=[
                html.H6(['cases', html.Br(), y1[-1], html.Br()]),
                html.P([x1, '%'])],
                     )], className='four columns'),

        html.Div(style={'textAlign': 'center', 'font-family': 'Helvetica'}, children=[
            html.H6(['deaths', html.Br(), y2[-1], html.Br()]),
            html.P([x2, '%'])], className='four columns'),

        html.Div(style={'textAlign': 'center', 'font-family': 'Helvetica'}, children=[
            html.H6(['rank', html.Br(), rank, html.Br()])])
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
