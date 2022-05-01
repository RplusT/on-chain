# Import libraries for app building
## Main tools are dash and plotly. Subgrounds has its own wrappers for these two tools as well.

import dash
import dash_bootstrap_components as dbc
from dash import html
from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter, Bar
from millify import millify

# Import the queries from the uniswap_v2 data file
from uniswap_v2_data import sg, uni_v2_daily, uni_v2_factory, uni_v2_pairs, uni_v2_tokens, latest

# Building the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label('Uniswap V2 Overview',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '96px',
                             }, xs=12, sm=12, md=12, lg=6, xl=6)
        ])
    ], style={'padding': '2px'}),
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                html.P(
                    'Uniswap is a decentralized exchange (DEX) and automated market making (AMM) protocol that allows for the trading '
                    'of digital assets. The protocol uses a set of smart contracts to create liquidity pools and swap assets. '
                    'Reserves and prices are updated every time a trade is made by way of a constant product formula. '
                    'All of these eliminate the need for central intermediaries.',
                      style={'font-style': 'normal',
                             'font-weight': '400',
                             'font-size': '20px',
                             }),
                html.P(
                    'This dashboard will focus on an overview of Uniswap v2 on Ethereum-Mainnet, looking at things like trade volume, '
                    'total value locked, and activity levels over the last year.',
                      style={'font-style': 'normal',
                             'font-weight': '400',
                             'font-size': '20px',
                             })
                ]),
        ])
    ], style={'padding': '1px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Total Trading Volume (USD)',
                            style={'color': '#FFFFFF',
                                   'text-align': 'center'}),
                    html.H1('$' + 
                            millify(sg.query([uni_v2_factory.totalVolumeUSD]), precision=2),
                            style={'text-align': 'center',
                                   'color': '#FFFFFF'},
                            ),
                ]),
            ], color="primary"),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Total Value Locked (USD)',
                            style={'color': '#FFFFFF',
                                   'text-align': 'center'}),
                    html.H1('$' + 
                            millify(sg.query([uni_v2_factory.totalLiquidityUSD]), precision=2),
                            style={'text-align': 'center',
                                   'color': '#FFFFFF'},
                            ),
                ]),
            ], color='primary'),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Transactions',
                            style={'color': '#FFFFFF',
                                   'text-align': 'center'}),
                    html.H1(millify(sg.query([uni_v2_factory.txCount]), precision=2),
                            style={'text-align': 'center',
                                   'color': '#FFFFFF'},
                            ),
                ]),
            ], color='primary'),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Top Trading Pair',
                            style={'color': '#FFFFFF',
                                   'text-align': 'center'}),
                    html.H1(sg.query([uni_v2_pairs.pairName])[0],
                            style={'text-align': 'center',
                                   'color': '#FFFFFF'},
                            ),
                ]),
            ], color='primary'),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Daily Trading Volume'),
                        ]),
                    ]),
                ], style={'color': '#17202a',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Bar(
                                name='daily trading volume',
                                x=uni_v2_daily.dateNorm,
                                y=uni_v2_daily.dailyVolumeUSD
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Trading Volume (USD)'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Daily Liquidity'),
                        ]),
                    ]),
                ], style={'color': '#17202A',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='daily liquidity',
                                x=uni_v2_daily.dateNorm,
                                y=uni_v2_daily.totalLiquidityUSD
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Total Value Locked (USD'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Daily Trading Fees'),
                        ]),
                    ]),
                ], style={'color': '#17202A',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='daily fees',
                                x=uni_v2_daily.dateNorm,
                                y=uni_v2_daily.dailyFeesUSD
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Fees (USD)'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Cumulative Transactions (Swaps, Add and Remove Liquidity)'),
                        ]),
                    ]),
                ], style={'color': '#17202A',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Bar(
                                name='transaction count',
                                x=uni_v2_daily.dateNorm,
                                y=uni_v2_daily.txCount
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Transactions'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Top Pairs by Volume (USD)'),
                        ]),
                    ]),
                ], style={'color': '#17202A',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Bar(
                                name='top pairs',
                                x=uni_v2_pairs.pairName,
                                y=uni_v2_pairs.volumeUSD
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Trading Volume (USD)'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Top Tokens by Volume (USD)'),
                        ]),
                    ]),
                ], style={'color': '#17202A',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Bar(
                                name='top tokens',
                                x=uni_v2_tokens.symbol,
                                y=uni_v2_tokens.tradeVolumeUSD
                            )
                        ],
                        layout={
                            'showlegend': False,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#6c3483', 'color': 'black',
                                      'title': 'Trading Volume (USD)'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#e8daef',
                            'plot_bgcolor': '#e8daef',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#e8daef')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P('Made by rplust.',
                           className='card-text'),
                    dbc.CardLink('Twitter', href='https://twitter.com/robplust'),
                    dbc.CardLink('GitHub', href='https://github.com/RplusT/on-chain/tree/main/uniswap_v2')
                ]),
            ]),
        ]),
    ]),
], style={'backgroundColor': '#FFFFFF'}, fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
