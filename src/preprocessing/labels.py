def label_sleep_quality(score):
    if score >= 8:
        return "Good"
    elif score >= 6:
        return "Average"
    else:
        return "Poor"
