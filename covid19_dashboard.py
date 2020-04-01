import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash()
df1 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/confirmed')
df2 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/deaths')
df3 = pd.read_json('https://coronavirus-tracker-api.herokuapp.com/recovered')

no_confirmed_ww = df1.latest[1]
no_deaths_ww = df2.latest[1]
no_recovered_ww = df3.latest[1]

app.layout = html.Div(
    [
        html.H1(children='COVID19 Dashboard'),
        html.H4(children='Worldwide Cases'),
        html.P(children=['Number of confirmed cases: ', no_confirmed_ww]),
        html.P(children=['Number of deaths cases: ', no_deaths_ww]),
        html.P(children=['Number of recovered cases: ', no_recovered_ww]),
        dcc.Graph(
            id='Worldwide Cases',
            figure={
                'data': [
                    {'x': ['Confirmed', 'Deaths', 'Recovered'], 'y': [no_confirmed_ww, no_deaths_ww, no_recovered_ww], 'type': 'bar'},
                ]
            }
        ),
        html.H4(children='Plot of Cases in Country'),
        dcc.Input(
            id='confirmed',
            type='text',
            placeholder='Country',
        ),
        html.Div(id='output1')
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
                         ]
                     }
                     )


if __name__ == "__main__":
    app.run_server(debug=True)
