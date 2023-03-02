import pandas as pd
import numpy as np

def savetoCSV(attention,meditation,delta,theta,lowAlpha,highAlpha,lowBeta,highBeta,lowGamma,highGamma,classification,filename):

    try: 
        if classification==0:
            classification=np.zeros(len(attention), dtype=int)
        else:
            classification=np.ones(len(attention), dtype=int)
        dataset = pd.read_csv(filename+'.csv')
        df = pd.DataFrame({"attention" : attention, "meditation" : meditation,"delta" : delta, "theta" : theta
                                    , "lowAlpha" : lowAlpha, "highAlpha" : highAlpha, "lowBeta" : lowBeta,
                                    "highBeta" : highBeta, "lowGamma" : lowGamma, "highGamma" : highGamma,"classification" : classification})
        dataset=pd.concat([dataset,df])
        dataset.to_csv(filename+'.csv',index=False)  
        
        # df.to_csv("meawake.csv", index=False)
    except FileNotFoundError:
        df = pd.DataFrame({"attention" : attention, "meditation" : meditation,"delta" : delta, "theta" : theta
                                    , "lowAlpha" : lowAlpha, "highAlpha" : highAlpha, "lowBeta" : lowBeta,
                                    "highBeta" : highBeta, "lowGamma" : lowGamma, "highGamma" : highGamma, "classification" : classification})
        df.to_csv(filename+'.csv', index=False)

