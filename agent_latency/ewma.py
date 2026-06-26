from typing import List

# -----------------------------------------------------------------------------
# Helper functions - latency estimation
# -----------------------------------------------------------------------------

def estimate_agent_latency(
    data_points: List[float],
    newest_first: bool,
    max_sample_size: int = 20,
    alpha: float = 0.125
    ) -> float:
    """
    Calculates an estimated agent latency using an Exponentially Weighted Moving Average (EWMA).

    The final calculated value prioritizes recent data based on the chosen alpha.

    Parameters
    ----------
    data_points : List[float]
        A sequence of raw latency metrics to evaluate.
    newest_first : bool
        Indicator of how the data sample was ordered:
        - If True, selects the first `max_sample_size` elements and reverses them
          so the newest metric sits last.
        - If False, selects the trailing elements up to `max_sample_size`.
    max_sample_size : int, default 20
        The maximum number of data points to include in the calculation.
    alpha : float, default 0.125
        The smoothing factor between 0 and 1. A higher alpha gives greater weight to recent data points.

    Returns
    -------
    float
        The final estimated latency of the agent. Returns 0 if the data sample is empty.

    See Also
    --------
        _calculate_ewma

    Examples
    --------
    >>> data = [50.0, 80.0, 80.0, 60.0]
    >>> estimate_agent_latency(data, newest_first=False, alpha=0.2)
    60.64
    """
    if not (0 <= alpha <= 1):
        raise ValueError("Alpha must be between 0 and 1")
    if not data_points:
        return 0
    if not (max_sample_size > 0):
        return 0
    
    valid_metrics: List[float] = []

    # start calculating ewma from the oldest data point
    if newest_first:
        for point in reversed(data_points):
            if len(valid_metrics) >= max_sample_size:
                break
            elif point > 0:
                valid_metrics.append(point)
    else:
        for point in data_points:
            if len(valid_metrics) >= max_sample_size:
                break
            elif point > 0:
                valid_metrics.append(point)

    if not valid_metrics:
        return 0
    
    return  _calculate_ewma(valid_metrics, alpha)[-1]


def _calculate_ewma(data: List[float], alpha: float = 0.125) -> List[float]:
    """
    Compute the Exponentially Weighted Moving Average (EWMA) for a sequence of values.

    The moving average is calculated recursively where each subsequent value is 
    weighted against the previous running average. Points appearing later in the 
    `data` list carry exponentially higher weight in the final result.
    
    EWMA_t = (1-alpha)*EWMA_t-1 + alpha*Sample_t

    Parameters
    ----------
    data : List[float]
        The **chronological** sequence of numeric data points to smooth.
    alpha : float, default 0.125
        The smoothing factor between 0 and 1. The default value of 0.125 
        is a standard constant used in TCP network round trip time estimations (RFC 6298).

    Examples
    --------
    >>> data = [50,80,80,60]
    >>> _calculate_ewma(data=data, alpha=0.2)
    60.64

    See Also
    --------
        Summary: https://en.wikipedia.org/wiki/EWMA_chart
    """
    if not (0 <= alpha <= 1):
        raise ValueError("Alpha must be between 0 and 1")

    ewma = [data[0]]
    
    for current_value in data[1:]:
        next_ewma = (alpha * current_value) + ((1 - alpha) * ewma[-1])
        ewma.append(next_ewma)
    
    return ewma

# -----------------------------------------------------------------------------
# ...
# -----------------------------------------------------------------------------