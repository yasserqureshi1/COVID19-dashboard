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
dfcountry = pd.read_csv('countryMap.txt', sep='\t')
dff = a.merge(dfcountry, how='inner', left_on=['country_code'], right_on=['2let'])

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

app.layout = html.Div(
    [

        html.Div([
            html.H1(children='COVID19 Dashboard', style={'textAlign': 'center', 'font-family': 'Helvetica'}),
            html.H6(children='By Yasser Qureshi', style={'textAlign': 'center', 'font-family': 'Helvetica'})
        ], className="row", ),

    html.H4(children='Worldmap of Cases', style={'textAlign': 'center', 'font-family': 'Helvetica'}),

        html.Div([
            dcc.Graph(id='map-display',
                      figure={
                          'data': [go.Choropleth(
                              locations=dff['3let'],
                              z=dff['latest'],
                              text=dff['country'],
                              colorscale='sunset',
                              autocolorscale=False,
                              reversescale=True,
                              marker_line_color='darkgray',
                              marker_line_width=0.5,
                              colorbar_title='Cases',
                          )
                          ],
                          'layout': dict(
                              title_text='World Map of Cases',
                              geo=dict(
                                  showframe=False,
                                  showcoastlines=False,
                                  projection_type='equirectangular'))
                      }
                      ),

        ]),

        html.Div([

            html.H4(children='Worldwide Cases', style={'textAlign': 'center', 'font-family': 'Helvetica'}),

            html.Div(
                dcc.Graph(
                    id='Worldwide Cases',
                    figure={
                        'data': [
                            {'x': ['Confirmed', 'Deaths', 'Recovered'],
                             'y': [df1.latest[1], df2.latest[1], df3.latest[1]],
                             'type': 'bar'},
                        ],
                    },
                    style={'height': 400, 'width': 400}
                ),
                style={'display': 'inline-block', 'height': '200px'}
            ),

            html.Div([
                html.P(children=['Number of confirmed cases: ', df1.latest[1]], style={'font-family': 'Helvetica'}),
                html.P(children=['Number of deaths cases: ', df2.latest[1]], style={'font-family': 'Helvetica'}),
                html.P(children=['Number of recovered cases: ', df3.latest[1]], style={'font-family': 'Helvetica'}),
            ], style={'display': 'inline-block', 'height': '200px'}),

        ], className='row'),

        html.Div(
            html.H4(children='Plot of Cases in Country', style={'textAlign': 'center', 'font-family': 'Helvetica'}),
            className='row'),

        html.Div(
            dcc.Input(
                id='confirmed',
                type='text',
                placeholder='Country',
            ), className='row', style={'textAlign': 'center'}
        ),

        html.Div([
            html.Div(id='output1', style={'width': 600, 'height': 400}, className='six columns'),
            html.Div(id='output2', style={'width': 600, 'height': 400}, className='six columns')],
            className='row'),

    ]
)


@app.callback(
    Output("output1", "children"),
    [Input("confirmed", "value")]
)
def update_output(country):
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
                             'title': 'Plot of Cases'
                         }
                     },
                     )


@app.callback(
    Output("output2", 'children'),
    [Input('confirmed', 'value')]
)
def table2(country):
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
    return dcc.Graph(id=f"{country} Rate",
                     figure={
                         'data': [
                             {'x': xrate, 'y': rate, 'type': 'line', 'name': 'Rate'}
                         ],
                         'layout': {
                             'title': 'Rate of Cases'
                         }
                     },
                     )


if __name__ == "__main__":
    app.run_server(debug=True)
