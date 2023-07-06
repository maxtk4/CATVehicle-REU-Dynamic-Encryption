
def validate(codea: str, codeb: str):
    """
    Calculates the hamming distance between codea and codeb
    Returns the percentage of disagreements between the codes
        (length - hamming distance) / length of code
    """
    return (len(codea) - sum([1 if codea[index] != codeb[index] else 0 for index in range(len(codea))])) / len(codea)