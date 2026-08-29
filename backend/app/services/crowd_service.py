def calculate_crowd_status(booked_count: int, capacity: int) -> str:
    """
    Calculates crowd density status based on booked count and capacity.
    0 - 50%   = LOW
    >50 - 80% = MEDIUM
    >80%      = HIGH
    """
    if capacity <= 0:
        return "HIGH"
    
    ratio = booked_count / capacity
    if ratio <= 0.50:
        return "LOW"
    elif ratio <= 0.80:
        return "MEDIUM"
    else:
        return "HIGH"
