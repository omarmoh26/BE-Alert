import statistics
def att(attention):
    med=statistics.median(attention)
    mean=statistics.mean(attention)
    # if mean >= 75:
    #     print("not sleepy and focused")
    #     return "not sleepy and focused"
    # elif mean >= 50:
    #     print("not sleepy but not focused")
    #     return "not sleepy but not focused"
    # elif mean >= 25:
    #     print("sleepy")
    #     return "sleepy"
    # elif mean >= 0:
    #     print("very sleepy")
    #     return "very sleepy"
    if med >= 75:
        print("not sleepy and focused")
        return "not sleepy and focused"
    elif med >= 50:
        print("not sleepy but not focused")
        return  "not sleepy but not focused"
    elif med >= 25:
        print("sleepy")
        return "sleepy"
    elif med >= 0:
        print("very sleepy")
        return "very sleepy"
    
