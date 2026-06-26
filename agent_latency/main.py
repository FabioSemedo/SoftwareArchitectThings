import json
import matplotlib.pyplot as plt
import numpy as np

from time import time
from typing import Dict, List, Tuple

from ewma import estimate_agent_latency
from ewma import _calculate_ewma

def printH(header):
    print("___________________________________________________________")
    print(header)
    print("___________________________________________________________")

def test_estimate_agent_latency():
    printH("Testing estimate_agent_latency:")
    data = [50,80,80,60]
    print("avg: ", sum(data)/len(data))
    result_125 = estimate_agent_latency(data, newest_first=False, alpha=0.125)
    result_150 = estimate_agent_latency(data, newest_first=False, alpha=0.15)
    result_200 = estimate_agent_latency(data, newest_first=False, alpha=0.2)
    result_500 = estimate_agent_latency(data, newest_first=False, alpha=0.5)
    result_900 = estimate_agent_latency(data, newest_first=False, alpha=0.9)

    print("alpha = 0.125", data, result_125)
    print("alpha = 0.150", data, result_150)
    print("alpha = 0.200", data, result_200)
    print("alpha = 0.500", data, result_500)
    print("alpha = 0.900", data, result_900)

    data.reverse()
    result_125 = estimate_agent_latency(data, newest_first=True, alpha=0.125)
    print("alpha = 0.125", data, result_125)

# Compute EWMA_i where i = step = size of sample given to EWMA
def calculate_ewma_i(buf: list, data: list, step: int):
        j = 0
        buf.append(estimate_agent_latency(data[:step], newest_first=False, max_sample_size=step + 1))
        for i in range(step*2, len(data), step):
            j += step
            buf.append(estimate_agent_latency(data[j:i], newest_first=False, max_sample_size=step +1))

            
def read_dataset(data_file: str, newest_is_frist: bool) -> Tuple[List[float], List[float]]:
    printH(f"Testing estimate_agent_latency with real data: {data_file}")


    with open(f"data/{data_file}", "r") as file:
        data: Dict[str, List[Tuple[float, float]]] = json.loads(file.read())

    print(data)
    if newest_is_frist:
        data["data"].reverse()

    timestamp = [x[0] for x in data["data"]]
    latency = [x[1]*1000 for x in data["data"]] # convert to ms

    return (latency, timestamp)

def wrap_dataset(buffer:list, timestamps: list, step:int ):
    print(f"EWMA_{step}: ", buffer, "\nlength: ", len(buffer))

    arr = []
    time_idx = step-1
    ewma_idx = 0
    while(time_idx < len(timestamps)):
        arr.append((timestamps[time_idx], buffer[ewma_idx]))
        time_idx += step
        ewma_idx += 1

    return arr

data, timestamp = read_dataset("idle_1.json", newest_is_frist=True)

ewma = _calculate_ewma(data)
ewma_ds = wrap_dataset(ewma, timestamp, 1)

ewma_10: List[float] = []
step = 10

calculate_ewma_i(buf=ewma_10, data=data, step=step)


def graph():
    # Generate sample data for distinct groups
    x_data_1 = np.array(timestamp)
    y_data_1 = np.array(data)  

    x_data_2 = np.array(timestamp)
    y_data_2 = np.array(ewma)   

    buf = ewma_10
    x_data_3 = np.array([x for x in range(int(200/len(buf)),201, int(200/len(buf)))])
    y_data_3 = np.array(buf)

    plt.plot(x_data_1, y_data_1, color='blue', label='Agent heartbeep latency')
    plt.plot(x_data_2, y_data_2, color='red', label='EWMA latency estimation')

    # # Calculate the trend lines
    # # np.polyfit(x, y, 1) calculates a 1st-degree polynomial (a linear trend line)
    # fit_1 = np.polyfit(x_data_1, y_data_1, 1)
    # line_1 = np.poly1d(fit_1)

    # fit_2 = np.polyfit(x_data_2, y_data_2, 1)
    # line_2 = np.poly1d(fit_2)

    # # Plot the trend lines
    # # We pass the x-data and the calculated y-values from our poly1d functions
    # plt.plot(x_data_1, line_1(x_data_1), color='blue', linestyle='--', label='Group A Trend')
    # plt.plot(x_data_2, line_2(x_data_2), color='red', linestyle='--', label='Group B Trend')

    # Draw the scatter plots
    # plt.scatter(x_data_1, y_data_1, color='blue', label='Heartbeep delta time')
    # plt.scatter(x_data_2, y_data_2, color='red', label='EWMA')
    plt.scatter(x_data_3, y_data_3, color='green', label=f'EWMA_{step} subset')

    # Format and label the chart
    plt.title('Benchmarking EWMA_i estimation of the Robotiar agent latency')
    plt.xlabel('Time (in s)')
    plt.ylabel('Latency (in ms)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    # 6. Render the plot
    plt.savefig(fname=f"images/temp_{int(time())}.png")