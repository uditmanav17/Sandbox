def slices(series, length):
    if not series or length <= 0 or len(series) < length:
        raise ValueError("Check your inputs")
    
    return [series[i:i+length] for i in range(len(series)-length+1)]
    