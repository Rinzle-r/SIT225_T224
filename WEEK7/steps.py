import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Step 1 >>
data = pd.read_csv("sensor_data.csv", encoding='ISO-8859-9')


temp_col = 'Temperature (°C)'
humi_col = 'Humidity (%)'

# Step 2 >>
X = data[[temp_col]].values  
y = data[humi_col].values 

# Step 3 >>
model = LinearRegression()
model.fit(X, y)

# Step 4 >>
temp_min = X.min()
temp_max = X.max()
temp_ran = np.linspace(temp_min, temp_max, 100).reshape(-1, 1)
humi_predi = model.predict(temp_ran)

# Step 5 >>
def plot_regression(data, title):
    X = data[[temp_col]].values
    y = data[humi_col].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    temp_min = X.min()
    temp_max = X.max()
    temp_ran = np.linspace(temp_min, temp_max, 100).reshape(-1, 1)
    humi_predi = model.predict(temp_ran)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Original Data')
    plt.plot(temp_ran, humi_predi, color='red', linewidth=2, label='Regression Line')
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Initial plot
plot_regression(data, ' >> Temperature &  Humidity with Linear Regression <<')

# Step 6 >>
def filter_outliers(data, temp_min, temp_max):
    return data[(data[temp_col] >= temp_min) & (data[temp_col] <= temp_max)]

# Applying initial filtering 
filtered_temp_min = data[temp_col].quantile(0.05)
filtered_temp_max = data[temp_col].quantile(0.95)
filtered_data = filter_outliers(data, filtered_temp_min, filtered_temp_max)

# Plotting after initial filtering
plot_regression(filtered_data, '>> Temperature & Humidity (Filtered) << ')

# Step 7 >> 
plot_regression(filtered_data, ' >> Filtered Temperature & Humidity with Linear Regression <<')

# Step 8 >>
# Apply additional filtering 
additional_temp_min = data[temp_col].quantile(0.1)
additional_temp_max = data[temp_col].quantile(0.9)
data_additional = filter_outliers(data, additional_temp_min, additional_temp_max)

# Plot after additional filtering
plot_regression(data_additional, ' >> Temperature vs Humidity with Further Filtered Data <<')
