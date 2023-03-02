import statisticalRecords
import pandas as pd
import joblib
def classfy(alpha1,alpha2):
    try:
        Alpha1_IQR=statisticalRecords.getAlpha1_IQR(alpha1)
        print('got alpha1 iqr')
        Alpha1_median=statisticalRecords.getAlpha1_median(alpha1)
        print('got alpha1 median')
        Alpha2_mean=statisticalRecords.getAlpha2_mean(alpha2)
        print('gotalpha2 mean')
        df = pd.DataFrame({"Alpha1_IQR" : [Alpha1_IQR], "Alpha1_median" : [Alpha1_median],"Alpha2_mean" : [Alpha2_mean]})
        print('put it in dataframe')
        loaded_model = joblib.load('models/knn_model.sav')
        print('loaded model')
        predict=loaded_model.predict(df)
        print('predictied model')
        print(predict)
        if 0 in predict:
            print("not sleepy")
            return 0
        else:
            print("sleepy")
            return 1
    except Exception as e:
        print(e)
        
    
 
    
