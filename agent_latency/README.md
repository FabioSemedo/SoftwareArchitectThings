This section aims to study how adequately the exponentialy weighted moving average (EWMA) estimates the latency of an agent's connection as well as in sample volumne impact the estimations.

---

- [ ] Gather data from an idle agent
- [ ] Gather data from a busy agent (pubsub)

Draw a gragh:
  - [ ] Latency vs Time
  - [ ] EWMA vs Time
  - [ ] EWMA vs Time with a Sample size 5 $EWMA_{5}$
  - [ ] EWMA vs Time with a Sample size 10 $EWMA_{10}$
  - [ ] EWMA vs Time with a Sample size 20 $EWMA_{20}$
  - [ ] EWMA vs Time with a Sample size 10 $EWMA_{25}$
>Note: since the server is already gathering the last 20 agent system metric datapoints, using a sample of size $\leq$ 20 would be ideal

Evaluate accuracy:
  - [ ] Compared to EWMA that uses the entire dataset, we will measure the margin of error of EWMA$_i$ that uses a subset of the dataset:
  > margin = 1.00 -  abs($EWMA_i - EWMA$)

Segment the dataset to study how the subsets handle:
    - [ ] 1 trend in the latency (1 segment)
    - [ ] A change in the trend  (between segments)
  