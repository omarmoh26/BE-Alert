import pandas as pd

def savetoCSV(attention,meditation,delta,theta,lowAlpha,highAlpha,lowBeta,highBeta,lowGamma,highGamma,filename):

    try: 
        dataset = pd.read_csv(filename+'.csv')
        df = pd.DataFrame({"attention" : attention, "meditation" : meditation,"delta" : delta, "theta" : theta
                                    , "lowAlpha" : lowAlpha, "highAlpha" : highAlpha, "lowBeta" : lowBeta,
                                    "highBeta" : highBeta, "lowGamma" : lowGamma, "highGamma" : highGamma})
        dataset=pd.concat([dataset,df])
        dataset.to_csv(filename+'.csv',index=False)  
        
        # df.to_csv("meawake.csv", index=False)
    except FileNotFoundError:
        df = pd.DataFrame({"attention" : attention, "meditation" : meditation,"delta" : delta, "theta" : theta
                                    , "lowAlpha" : lowAlpha, "highAlpha" : highAlpha, "lowBeta" : lowBeta,
                                    "highBeta" : highBeta, "lowGamma" : lowGamma, "highGamma" : highGamma})
        df.to_csv(filename+'.csv', index=False)

