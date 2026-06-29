This section aims to study the adequacy of the Exponentially Weighted Moving Average ([EWMA](https://en.wikipedia.org/wiki/EWMA_chart)) in estimating the latency of an agent's connection and the impact of sample size on the accuracy of these estimations.
   
---

Methodology, Data Collection and Visualisation

- [x] Gather data from an idle agent
- [x] Gather data from a busy agent (pubsub)Visualizations Developed
- [x] Latency vs. Time
- [x] EWMA vs. Time
- [x] EWMA vs. Time with a Sample size 5 ($\text{EWMA}_{5}$)
- [x] EWMA vs. Time with a Sample size 10 ($\text{EWMA}_{10}$)
- [x] EWMA vs. Time with a Sample size 20 ($\text{EWMA}_{20}$)
- [x] EWMA vs. Time with a Sample size 25 ($\text{EWMA}_{25}$)

>Note: Because the server currently gathers the last 20 agent system metric datapoints, utilizing a sample size of $\leq$ 20 is optimal for this implementation.

---

Conclusions

An analysis of the [graphs](./images/) reveals that the standard EWMA, with $\alpha = 0.125$ tends to underestimate agent latency by a considerable margin:
- ~15% underestimation for a sample with a fixed trend.
- ~30% underestimation for a sample with fluctuating trends.

To mitigate this discrepancy and decrease the margin we have a few options, 
1. Increase $\alpha$
 
The default $\alpha$ is 0.125. Testing shows $\alpha$ = 0.3 decreases the margin between true latency and the EWMA estimation to bellow 5%. As well as causing sample sizes to have less influce in the yield.  
I.e. $\text{EWMA}_5 \approx \text{EWMA}_{20} \approx \text{EWMA}$

2. Decrease the sample size, $i$, (with $\alpha$ = 0.125) provided to the EWMA calculation. 

The resulting delta between the true latency and the $\text{EWMA}_i \land \alpha = 0.125$ estimation will decrease as $i$ decreases:

Sample size 5: Delta is < 5%                                    [View ewma_5](./images/temp_ewma_05.png)  
Sample size 10: Delta is closely aligned with the standard EWMA [View ewma_10](./images/temp_ewma_10.png)  
Sample size 20: Delta is approximately equal to the standard EWMA             [View ewma_20](./images/temp_ewma_20.png)  

---

Limitations & Future Considerations

**Clock Offset Bias**: The current data contains a bias due to clock offsets. When the system clock corrects itself the measured latency drops dramatically. This causes the measured latency to range from roughly 0.1s to 1.0s every ~2s. These clock corrections artificially impact the benchmark because the server currently resides on the same machine as the agent.

**Production Environment**: Once the Robotair infrastructure is deployed to a production environment, the agents will typically run on machines separate from the server. While this physical separation will inherently increase the baseline agent latency, it will also significantly decrease the influence of the clock fluctuations observed in our current measurements.  
  This means that estimations like $\text{EWMA}_5$ and $\text{EWMA}_{10}$ would server as better indicators of the agent's connection's health.

Data and Graphs can be found here:  
[Data](./data/)  
[Graphs](./images/)