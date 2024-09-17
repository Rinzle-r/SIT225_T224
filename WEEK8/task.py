import sys
import traceback
import csv
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
import os
import threading
from dash import dcc
from dash import html
import dash
from dash.dependencies import Output, Input
import plotly.graph_objs as go

DEVICE_ID = "2824075c-421d-4155-88c8-64132d5385bf"
SECRET_KEY = "DTMjGC9bjqITKfCuBJxO1Yz#r"

value_py_x = None
value_py_y = None
value_py_z = None

data_x = []
data_y = []
data_z = []
timestamps = []
N = 100  

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time Accelerometer Data"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='graph-update',
        interval=1000,  
        n_intervals=0
    )
])

def write_to_csv():
    global value_py_x, value_py_y, value_py_z

    file_exists = os.path.isfile('accelerometer_data.csv')
    if value_py_x is not None and value_py_y is not None and value_py_z is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('accelerometer_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header if the file is new
            if not file_exists:
                writer.writerow(["timestamp", "x", "y", "z"])

            # Write the actual data
            writer.writerow([timestamp, value_py_x, value_py_y, value_py_z])

        # Store values for plotting
        timestamps.append(timestamp)
        data_x.append(value_py_x)
        data_y.append(value_py_y)
        data_z.append(value_py_z)

        # Keep only the last N samples for plotting
        if len(timestamps) > N:
            timestamps.pop(0)
            data_x.pop(0)
            data_y.pop(0)
            data_z.pop(0)

# Callback function for py_x variable
def on_py_x_changed(client, value):
    global value_py_x
    value_py_x = value
    print(f"New py_x value: {value_py_x}")
    write_to_csv()

# Callback function for py_y variable
def on_py_y_changed(client, value):
    global value_py_y
    value_py_y = value
    print(f"New py_y value: {value_py_y}")
    write_to_csv()

# Callback function for py_z variable
def on_py_z_changed(client, value):
    global value_py_z
    value_py_z = value
    print(f"New py_z value: {value_py_z}")
    write_to_csv()

# Function to update the graph in Dash app
@app.callback(
    Output('live-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph_live(n):
    fig = go.Figure()

    # Add lines for x, y, and z data
    if data_x:  # Check if there's data to plot
        fig.add_trace(go.Scatter(x=list(range(len(data_x))), y=data_x, mode='lines', name='X'))
        fig.add_trace(go.Scatter(x=list(range(len(data_y))), y=data_y, mode='lines', name='Y'))
        fig.add_trace(go.Scatter(x=list(range(len(data_z))), y=data_z, mode='lines', name='Z'))

    fig.update_layout(title='Real-Time Accelerometer Data (X, Y, Z)',
                      xaxis_title='Sample Number',
                      yaxis_title='Acceleration')

    return fig

# Main function with Arduino Cloud client setup
def main():
    print("Starting main function")

    try:
        # Instantiate Arduino Cloud client
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
        )
        print("Client created successfully.")

        # Register callbacks for py_x, py_y, and py_z accelerometer variables
        client.register("py_x", value=None, on_write=on_py_x_changed)
        client.register("py_y", value=None, on_write=on_py_y_changed)
        client.register("py_z", value=None, on_write=on_py_z_changed)
        print("Variables registered successfully.")

        # Start the client
        client.start()
        print("Client started successfully.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # Start the Arduino Cloud client in a separate thread
        arduino_thread = threading.Thread(target=main)
        arduino_thread.start()

        # Start the Dash app
        app.run_server(debug=True, use_reloader=False)  # use_reloader=False to avoid restarting Dash app when Arduino client starts

    except Exception as e:
        print(f"Exception in main: {e}")
        traceback.print_exc()
