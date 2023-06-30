
def validate(codea: str, codeb: str):
    """
    Calculates the hamming distance between codea and codeb
    Returns the percentage of disagreements between the codes
        hamming distance / length of code
    """
    differences = 0

    for index in range(len(codea)):
        #ternary operators are incredible
        #this comment is longer than the code would have been to write this normally
        #but I don't care
        differences += 1 if codea[index] != codeb[index] else 0

    return (len(codea) - differences) / len(codea)