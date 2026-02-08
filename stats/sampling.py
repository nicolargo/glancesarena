from datetime import datetime, timedelta
from typing import List, Optional, Tuple


def sample_history(
    history: List[Tuple[datetime, float]],
    period_seconds: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    aggregation: str = 'mean'
) -> List[Tuple[datetime, float]]:
    """
    Generate a sampling of the history with a configurable period.

    Args:
        history: List of tuples (datetime, value)
        period_seconds: Sampling period in seconds (None = period is entire history)
        start_date: Start date (None = first date in history)
        end_date: End date (None = last date in history)
        aggregation: Aggregation method ('mean', 'min', 'max', 'first', 'last')

    Returns:
        List of sampled tuples (datetime, value)
    """
    if not history:
        return []

    # Sort history by date
    sorted_history = sorted(history, key=lambda x: x[0])

    # Define boundaries
    if start_date is None:
        start_date = sorted_history[0][0]
    if end_date is None:
        end_date = sorted_history[-1][0]

    # Filter history by dates
    filtered_history = [
        (dt, val) for dt, val in sorted_history
        if start_date <= dt <= end_date
    ]

    if not filtered_history:
        return []

    # Generate time buckets
    sampled_data = []
    current_bucket_start = start_date
    period_delta = timedelta(seconds=period_seconds if period_seconds is not None else (end_date - start_date).total_seconds())

    while current_bucket_start <= end_date:
        bucket_end = current_bucket_start + period_delta

        # Find all values in this bucket
        bucket_values = [
            val for dt, val in filtered_history
            if current_bucket_start <= dt < bucket_end
        ]

        if bucket_values:
            # Apply aggregation
            if aggregation == 'mean':
                aggregated_value = sum(bucket_values) / len(bucket_values)
            elif aggregation == 'min':
                aggregated_value = min(bucket_values)
            elif aggregation == 'max':
                aggregated_value = max(bucket_values)
            elif aggregation == 'first':
                aggregated_value = bucket_values[0]
            elif aggregation == 'last':
                aggregated_value = bucket_values[-1]
            else:
                raise ValueError(f"Aggregation '{aggregation}' not supported")

            # Use bucket midpoint as timestamp
            bucket_timestamp = current_bucket_start + period_delta / 2
            sampled_data.append((bucket_timestamp, aggregated_value))

        current_bucket_start = bucket_end

    return sampled_data
