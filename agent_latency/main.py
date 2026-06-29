import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
from pprint import pprint
from typing import Dict, List, Tuple

from ewma import estimate_agent_latency
from ewma import _calculate_ewma

ALPHA = 0.3

IDLE_FILE = "idle_agent_1.json"
BUSY_FILE = "busy_agent_1.json"

def printH(header):
    print("________________________________________________________")
    print(header)
    print("________________________________________________________")

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

# -----------------------------------------------------------------------------------------
# Prepare data
# -----------------------------------------------------------------------------------------

# Compute EWMA_i where i = step = size of sample given to EWMA
def calculate_ewma_i(buf: list, data: list, step: int):
    j = 0
    buf.append(estimate_agent_latency(data[:step], newest_first=False, max_sample_size=step + 1, alpha=ALPHA))
    for i in range(step*2, len(data)+1, step):
        j += step
        buf.append(estimate_agent_latency(data[j:i], newest_first=False, max_sample_size=step +1, alpha=ALPHA))

            
def read_dataset(data_file: str, newest_is_frist: bool) -> Tuple[List[float], List[float]]:
    """
    Example
    -------
    >>> {"data":[["2026-06-26 13:38:45.743316+00","0.05012702941894531"],["2026-06-26 13:38:35.908915+00","0.22125792503356934"]]}
    [1782481125.743316, 1782481115.908915], [50.12702941894531, 221.25792503356934]
    """
    printH(f"Testing estimate_agent_latency with real data: {data_file}")


    with open("./data/"+data_file, "r") as file:
        data: Dict[str, List[Tuple[str, float]]] = json.loads(file.read())

    if newest_is_frist:
        data["data"].reverse()

    timestamp = [datetime.datetime.fromisoformat(x[0]).timestamp() for x in data["data"]]        
    latency = [float(x[1])*1000 for x in data["data"]] # convert to ms

    return (latency, timestamp)

def zip_timestamp_with_ewma(buffer:List[float], timestamps: List[float], step:int) -> List[Tuple[float, float]]:
    print(f"EWMA_{step}: length=", len(buffer))

    arr = []
    time_idx = step-1
    ewma_idx = 0
    while(time_idx < len(timestamps)):
        arr.append((timestamps[time_idx], buffer[ewma_idx]))
        time_idx += step
        ewma_idx += 1

    return arr

# -----------------------------------------------------------------------------------------
# Visuals
# -----------------------------------------------------------------------------------------

def add_to_graph(data:List[Tuple[float, float]], scatter: bool,  color:str, label:str):
        x_data = np.array([x[0] for x in data])
        y_data = np.array([x[1] for x in data])

        if scatter:
            plt.scatter(x_data, y_data, color=color, label=label)
        else:
            plt.plot(x_data, y_data, color=color, label=label)

def save_graph():
    # Format and label the chart
    plt.title(f'Benchmarking EWMA_i estimation of the Robotiar agent latency with Alpha = {ALPHA}')
    plt.xlabel('Time (in ms)')
    plt.ylabel('Latency (in ms)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    fname = f"images/temp_{int(datetime.datetime.now().timestamp())}.png"
    # fname = f"images/temp.png"
    plt.savefig(fname=fname, dpi=300, bbox_inches='tight')

if __name__=="__main__":
    plt.figure(figsize=(12, 6))

    data, timestamp = read_dataset(IDLE_FILE, newest_is_frist=True)
    start = timestamp[0]
    timestamp = [round(timestamp[i] - start, 4) for i in range(len(timestamp))]
    add_to_graph(list(zip(timestamp, data)), scatter=False, color= "#1A1A1A", label="Latency")
    
    ewma = _calculate_ewma(data, alpha=ALPHA)
    ewma_ds = zip_timestamp_with_ewma(ewma, timestamp, 1)
    add_to_graph(ewma_ds, scatter=False, color="blue", label="EWMA")

    def ewma_i(step: int, color:str):
        ewma_i: List[float] = []
        step = step
        calculate_ewma_i(buf=ewma_i, data=data, step=step)
        ewma_i_ds = zip_timestamp_with_ewma(ewma_i, timestamp, step)
        add_to_graph(ewma_i_ds, scatter=True, color=color, label=f"EWMA_{step}")

    ewma_i(5 , "#a60000")
    ewma_i(10, "#E00000")
    # ewma_i(15, "#459000")
    ewma_i(20, "#02e132")
    # ewma_i(25, "#6704a5")
    save_graph()