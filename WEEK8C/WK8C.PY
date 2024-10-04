import sys
import traceback
import csv
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient
import os
import threading
from dash import dcc, html
from dash.dependencies import Output, Input
import dash
import plotly.graph_objs as go

# Device details
DEVICE_ID = "d8b84c4e-639a-4358-9012-edb3c95628f2"
SECRET_KEY = "ywcfQApLpyPJiiP#enclGn79f"

value_py_x = None
value_py_y = None
value_py_z = None

# Buffers to hold the data for plotting
buffer_x = []
buffer_y = []
buffer_z = []
timestamps = []

# Number of samples to show on the graph at any given time
N = 50  

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time Accelerometer Data"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=200, n_intervals=0)  # Faster update at200ms
])

def write_to_csv():
    global value_py_x, value_py_y, value_py_z

    # Ensure we have values to work with
    if value_py_x is not None and value_py_y is not None and value_py_z is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        buffer_x.append(value_py_x)
        buffer_y.append(value_py_y)
        buffer_z.append(value_py_z)
        timestamps.append(timestamp)

        # Keep buffer sizes to the last N samples
        if len(buffer_x) > N:
            buffer_x.pop(0)
            buffer_y.pop(0)
            buffer_z.pop(0)
            timestamps.pop(0)

# Callbacks for handling incoming accelerometer data
def on_py_x_changed(client, value):
    global value_py_x
    value_py_x = value
    write_to_csv()

def on_py_y_changed(client, value):
    global value_py_y
    value_py_y = value
    write_to_csv()

def on_py_z_changed(client, value):
    global value_py_z
    value_py_z = value
    write_to_csv()

# Updating the graph
@app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph_live(n):
    fig = go.Figure()

    if buffer_x:  # Ensure there is data to plot
        fig.add_trace(go.Scatter(x=list(range(len(buffer_x))), y=buffer_x, mode='lines', name='X'))
        fig.add_trace(go.Scatter(x=list(range(len(buffer_y))), y=buffer_y, mode='lines', name='Y'))
        fig.add_trace(go.Scatter(x=list(range(len(buffer_z))), y=buffer_z, mode='lines', name='Z'))

    fig.update_layout(title='Real-Time Accelerometer Data (X, Y, Z)',
                      xaxis_title='Sample Number',
                      yaxis_title='Acceleration')

    return fig

# Main function to set up Arduino Cloud client
def main():
    try:
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
        )

        # Register accelerometer callbacks
        client.register("py_x", value=None, on_write=on_py_x_changed)
        client.register("py_y", value=None, on_write=on_py_y_changed)
        client.register("py_z", value=None, on_write=on_py_z_changed)

        client.start()

    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    arduino_thread = threading.Thread(target=main)
    arduino_thread.start()

    # Run the Dash app
    app.run_server(debug=True, use_reloader=False)
