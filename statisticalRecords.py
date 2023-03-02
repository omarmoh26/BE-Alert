import statistics
from scipy import stats

def getAlpha1_IQR(data):
    print('getting alpha1 iqr')
    return stats.iqr(data, interpolation = 'midpoint')
    
def getAlpha1_median(data):
    print('getting alpha1 median')
    return statistics.median(data)

def getAlpha2_mean(data):
    print('getting alpha2 mean')
    return statistics.mean(data)
