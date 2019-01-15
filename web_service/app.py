import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import flask
import os
import pandas as pd
from collections import Counter


app = dash.Dash(
    __name__,
    assets_external_scripts='https://cdn.plot.ly/plotly-finance-1.28.0.min.js'
)
server = app.server
app.title = 'So Sánh Việc'
df = pd.read_csv(os.path.join(os.getcwd(), "job_new.csv"))
skills = df.SKILL.unique()

app.layout = html.Div([
    html.Div([
        html.H2(u'SO SÁNH VIỆC',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Img(
            src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
            style={
                'height': '100px',
                'float': 'right'
            },
        ),
    ]),

    dcc.Dropdown(
        id='skill-input',
        options=[{'label': i, 'value': i} for i in skills],
    ),
    dcc.Graph(id='local-graph',
              style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='type-company-graph',
              style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='count-exp-graph',
              style={'width': '100%', 'display': 'inline-block'})
], className="container")


@app.callback(
    dash.dependencies.Output('local-graph', 'figure'),
    [dash.dependencies.Input('skill-input', 'value')]
)
def update_graph_local(skill_value):
    table_skill = df[df.SKILL == skill_value]

    # local
    count_local = Counter(table_skill['ADDRESS'])
    list_local = list(count_local)

    counts_local = []
    for k in list_local:
        count_l = count_local[k]
        counts_local.append(count_l)

    zip_local = list(zip(list_local, counts_local))
    new_type, new_count = zip(*zip_local)

    local_company = list(new_type)
    count_local = list(new_count)

    table_local = pd.DataFrame(
        {'local_company': local_company, 'count_local': count_local})
    table_local_small = table_local[table_local['count_local'] <= 160]

    return {
        'data': [
            go.Bar(
                x=table_local_small.local_company,
                y=table_local_small.count_local,
                marker={
                    'color': 'rgb(0,204,204)',
                },
                text=table_local_small.count_local,
                textposition='auto',
            )
        ],
        'layout': {
            'title': u'Khu vực tuyển dụng cho kỹ năng {}'.format(skill_value),
            'font': {'color': '#000000'}
        }
    }


@app.callback(
    dash.dependencies.Output('type-company-graph', 'figure'),
    [dash.dependencies.Input('skill-input', 'value')]
)
def update_graph_type_company(skill_value):
    table_skill = df[df.SKILL == skill_value]

    # type company
    count_type_company = Counter(table_skill['TYPE'])
    list_type_company = list(count_type_company)

    counts_type_company = []
    for q in list_type_company:
        count_t = count_type_company[q]
        counts_type_company.append(count_t)

    zip_type_company = list(zip(list_type_company, counts_type_company))
    new_type, new_count = zip(*zip_type_company)

    type_company = list(new_type)
    count_company = list(new_count)

    return {
        'data': [
            go.Pie(
                values=count_company,
                labels=type_company,
                hoverinfo='label+percent',
                textinfo='value',
                marker={
                    'colors':
                    ['rgb(210,105,30)',
                     'rgb((0,128,0)',
                     ]
                }
            )
        ],
        'layout': {
            'title': u'Công ty tuyển dụng cho kỹ năng {}'.format(skill_value),
            'font': {'color': '#000000'}
        }
    }


@app.callback(
    dash.dependencies.Output('count-exp-graph', 'figure'),
    [dash.dependencies.Input('skill-input', 'value')]
)
def update_graph_count_exp(skill_value):
    table_skill = df[df.SKILL == skill_value]

    # count_exp
    count_exp = Counter(table_skill['EXP'])
    list_exp = list(count_exp)

    counts_exp = []
    for e in list_exp:
        count_e = count_exp[e]
        counts_exp.append(count_e)

    zip_exp = list(zip(list_exp, counts_exp))
    new_type, new_count = zip(*zip_exp)

    exp_company = list(new_type)
    count_exp = list(new_count)

    table_exp = pd.DataFrame(
        {'exp_company': exp_company, 'count_exp': count_exp})
    table_exp_small = table_exp[table_exp['count_exp'] <= 10]

    return {
        'data': [
            go.Bar(
                x=table_exp_small.exp_company,
                y=table_exp_small.count_exp,
                text=table_exp_small.count_exp,
                textposition='auto',
                marker={
                    'color': 'rgb(138,43,226)',
                },
            )
        ],
        'layout': {
            'title': u'Năm kinh nghiệm cho kỹ năng {}'.format(skill_value),
            'font': {'color': '#000000'}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
