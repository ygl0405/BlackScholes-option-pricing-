import dash
from dash import dcc, html, Input, Output, State
import numpy as np
from scipy.stats import norm
import plotly.express as px
import pandas as pd
from numpy import exp, sqrt, log

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def run(
        self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike) +
            (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
            ) / (
                volatility * sqrt(time_to_maturity)
            )
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
        ) - current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

if __name__ == "__main__":
    time_to_maturity = 2
    strike = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05

    # Black Scholes
    BS = BlackScholes(
        time_to_maturity=time_to_maturity,
        strike=strike,
        current_price=current_price,
        volatility=volatility,
        interest_rate=interest_rate)
    BS.run()

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                background-color: #0d1b2a; /* Dark blue */
                color: #ffffff;
                font-family: Arial, sans-serif;
                height: 100%;
                overflow-x: hidden; /* Prevent horizontal scrollbars */
            }
            #root {
                height: 100%;
                display: flex;
                flex-direction: column;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'backgroundColor': '#000000',
        'color': '#ffffff',
        'fontFamily': 'Arial, sans-serif',
        'height': '100vh',
        'margin': '0',
        'padding': '0',
    },
    children=[
        # Left-side input panel
        html.Div(
            style={
                'width': '30%',
                'backgroundColor': '#1b263b',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '5px 5px 15px rgba(0, 0, 0, 0.5)',
                'overflowY': 'auto',
            },
            children=[
                html.H2(
                    "Model Parameters",
                    style={'textAlign': 'center', 'marginBottom': '20px'}
                ),
                html.Label("Underlying Price (S):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='underlying-price',
                    type='number',
                    value=100,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Strike Price (K):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='strike-price',
                    type='number',
                    value=100,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Implied Volatility (σ):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='volatility',
                    type='number',
                    value=0.2,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Time to Maturity (T in years):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='maturity',
                    type='number',
                    value=1,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Risk-Free Rate (r):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='risk-free-rate',
                    type='number',
                    value=0.05,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Call Option Bid Price:", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='call-bid-price',
                    type='number',
                    value=10,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Put Option Bid Price:", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='put-bid-price',
                    type='number',
                    value=10,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.H3(
                    "Heatmap Parameters",
                    style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom': '20px', 'color': '#ffffff'}
                ),
                html.Label("Min Implied Volatility (σ min):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='min-volatility',
                    type='number',
                    value=0.1,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Label("Max Implied Volatility (σ max):", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='max-volatility',
                    type='number',
                    value=0.5,
                    style={'width': '100%', 'marginBottom': '20px'}
                ),
                html.Button('Calculate', id='calculate-button', n_clicks=0, style={'marginTop': '10px'}), 
            ]
        ),
        # Right-side output panel
        html.Div(
            style={
                'width': '70%',
                'padding': '20px',
                'backgroundColor': '#102027',
                'borderRadius': '10px',
                'marginLeft': '10px',
                'boxShadow': '5px 5px 15px rgba(0, 0, 0, 0.5)',
                'overflowY': 'auto',
            },
            children=[
                html.H1(
                    "Black-Scholes Option Pricing",
                    style={
                        'textAlign':'center',
                        'fontWeight':'bold',
                        'marginBottom':'20px',
                    }
                ),
                html.H2("Current Input Parameters"),
                html.Div(id='parameter-table',style={'marginBottom': '20px'}),

                html.H2("Option Values"),
                html.Div(id='option-values', style={'marginBottom': '20px'}),  # Displays calculated values

                html.H2("Potential P&L- Interactive Heatmap "),
                html.P(
                    "The heatmap visualizes the profit or loss for the option price relative to bid price"
                    "across a range of implied volatility and an underlying prices.",
                    style={
                        'fontSize':'16px',
                        'fontStyle':'italic',
                        'marginBottom':'20px',
                    }
                ),
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'row'},
                    children=[
                        dcc.Graph(id='call-heatmap', style={'flex': 1, 'marginRight': '10px'}),
                        dcc.Graph(id='put-heatmap', style={'flex': 1})
                    ]
                ),
                html.Div(
                    style={
                        'textAlign':'center',
                        'padding': '10px',
                        'backgroundColor': '#1b263b',
                        'borderTop': '1px solid #333',
                    },
                    children=[
                        #LinkedIn Profile
                        html.A(
                            href="https://www.linkedin.com/in/yungyulee",
                            target="_blank",
                            style={'textDecoration': 'none', 'color': '#ffffff'},
                            children=[
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/174/174857.png",
                                    style={'width': '20px', 'verticalAlign': 'middle', 'marginRight': '8px'}
                                ),
                                "LinkedIn"
                            ]
                        ),
                        html.A(
                            href="https://github.com/ygl0405",
                            target="_blank",
                            style={'textDecoration':'none','color':'#ffffff', 'display':'flex','alignItems':'center'},
                            children=[
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/733/733553.png",
                                    style={'width': '20px', 'verticalAlign': 'middle', 'marginRight': '8px'}
                                ),
                                "GitHub"
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)

# Callback to update input parameters, option values, and heatmaps
@app.callback(
    [Output('parameter-table', 'children'),
     Output('option-values', 'children'),
     Output('call-heatmap', 'figure'),
     Output('put-heatmap', 'figure')],
    [Input('calculate-button', 'n_clicks')],
    [State('underlying-price', 'value'),
     State('strike-price', 'value'),
     State('volatility', 'value'),
     State('maturity', 'value'),
     State('risk-free-rate', 'value'),
     State('call-bid-price', 'value'),
     State('put-bid-price', 'value'),
     State('min-volatility', 'value'),
     State('max-volatility', 'value')]
)
def update_output(n_clicks, S, K, sigma, T, r, call_bid, put_bid, min_vol, max_vol):
    # Create a data dictionary for the parameters table
    parameters_data = [
        {"Parameter": "Underlying Price (S)", "Value": S},
        {"Parameter": "Strike Price (K)", "Value": K},
        {"Parameter": "Implied Volatility (σ)", "Value": sigma},
        {"Parameter": "Time to Maturity (T)", "Value": T},
        {"Parameter": "Risk-Free Rate (r)", "Value": r},
        {"Parameter": "Call Option Bid Price", "Value": call_bid},
        {"Parameter": "Put Option Bid Price", "Value": put_bid},
        {"Parameter": "Min Implied Volatility (σ min)", "Value": min_vol},
        {"Parameter": "Max Implied Volatility (σ max)", "Value": max_vol}
    ]
    parameter_table = html.Table(
        style={'width': '100%', 'color': '#ffffff', 'borderCollapse': 'collapse'},
        children=[
            html.Tr([
                html.Th(param["Parameter"], style={'padding': '10px', 'border': '1px solid #D3D3D3'}) for param in parameters_data
            ]),
            html.Tr([
                html.Td(param["Value"], style={'padding': '10px', 'border': '1px solid #D3D3D3', 'textAlign': 'center'}) for param in parameters_data
            ])
        ]
    )

    
    # Calculate option values
    bs= BlackScholes(T,K,S, sigma,r)
    bs.run()
    call_value= bs.call_price
    put_value= bs.put_price

    option_values = html.Div([
        html.P(f"European Call Option Value: {call_value:.2f}", style={'color': '#00FF00'}),
        html.P(f"European Put Option Value: {put_value:.2f}", style={'color': '#FF4500'})
    ])
    
    # Generate a range of stock prices
    stock_prices = np.linspace(S - 10, S + 10, 10)

    # Generate a range of volatility values
    volatilities = np.linspace(min_vol, max_vol, 10)

    call_pnl = np.zeros((len(stock_prices), len(volatilities)))
    put_pnl = np.zeros((len(stock_prices), len(volatilities)))

# Calculate P&L values efficiently
    for i, sp in enumerate(stock_prices):
        for j, vol in enumerate(volatilities):
            bs = BlackScholes(T, K, sp, vol, r)
            bs.run()
            call_pnl[i, j] = round(bs.call_price- call_bid, 2)
            put_pnl[i, j] = round(bs.put_price- put_bid, 2)

# Use numpy meshgrid to efficiently create DataFrame for P&L
    sp_grid, vol_grid = np.meshgrid(stock_prices, volatilities, indexing="ij")

    call_heatmap_data = pd.DataFrame({
        "Stock Price": sp_grid.flatten(),
        "Volatility": vol_grid.flatten(),
        "Call P&L": call_pnl.flatten()
    })

    put_heatmap_data = pd.DataFrame({
        "Stock Price": sp_grid.flatten(),
        "Volatility": vol_grid.flatten(),
       "Put P&L": put_pnl.flatten()
    })

    # Create heatmaps
    call_heatmap = px.density_heatmap(
        call_heatmap_data,
        x="Stock Price",
        y="Volatility",
        z="Call P&L",
        color_continuous_scale="RdYlGn",
        labels={"x": "Stock Price", "y": "Implied Volatility", "color": "Call P&L"},
        title="Call Option P&L Heatmap",
        text_auto=True
        )
    

    put_heatmap = px.density_heatmap(
       put_heatmap_data,
        x="Stock Price",
        y="Volatility",
        z="Put P&L",
        color_continuous_scale="RdYlGn",
        labels={"x": "Stock Price", "y": "Implied Volatility", "color": "Put P&L"},
        title="Put Option P&L Heatmap",
        text_auto=True
       )   # Initialize P&L matrice
    
    return parameter_table, option_values, call_heatmap, put_heatmap


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

