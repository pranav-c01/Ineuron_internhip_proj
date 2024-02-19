# split the raw data 
# save it in data/processed folder
import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import mutual_info_classif,SelectPercentile
from get_data import read_params
import joblib

def preprocessing_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    preprocessed_data_store_path = config["split_data"]["preprocessed_data_path"]
    ord_enc_path = config["ord_encoder_path"]
    TARGET_COL = config["base"]["target_col"]

    df = pd.read_csv(raw_data_path, sep=",")

    ## Missing values handle
    if len(df.columns[df.isna().any()])>0:
        for i in df.columns[df.isna().any()]:
            df[i].fillna(df[i].mode().loc[0],inplace=True)



##    X,y = df_ord.drop('class',axis=1),df_ord['class']

    ## Feature Selection :- Selecting Most important features by the technique of 
##    record = pd.DataFrame({'columns':X.columns,'mutual_info_class_f_score':mutual_info_classif(X, ##y)}).sort_values('mutual_info_class_f_score',ascending=False).head(15)
##    df_ord_mutual_cls = X[record['columns']]
##    df_ord_mutual_cls['class'] = y
    
    ## Ordinal encoding for categprical vars
    enc = OrdinalEncoder()
    df_ord = pd.DataFrame(enc.fit_transform(df),columns=df.columns)
#    class_cat = {'p':0,'e':1}
#    df_ord[TARGET_COL] = df[TARGET_COL].map(class_cat)


    ## Feature Selection :- Selecting Most important features by the technique of SelectPercentile	
    print(df_ord)
    selector = SelectPercentile(mutual_info_classif, percentile=80)  # Adjust percentile as needed
    X_selected = selector.fit_transform(df_ord.drop(TARGET_COL, axis=1), df_ord[TARGET_COL])
    selected_features = df_ord.columns[1:][selector.get_support()]
    df_sel = pd.concat([df_ord[selected_features],df_ord[TARGET_COL]],axis=1)

    joblib.dump(enc,ord_enc_path)
    df_sel.to_csv(preprocessed_data_store_path, sep=",", index=False, header=df_sel.columns)

    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    preprocessing_data(config_path=parsed_args.config)

