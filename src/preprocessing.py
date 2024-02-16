# split the raw data 
# save it in data/processed folder
import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import mutual_info_classif
from get_data import read_params

def preprocessing_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    preprocessed_data_store_path = config["split_data"]["preprocessed_data_path"]
    df = pd.read_csv(raw_data_path, sep=",")

    ## Missing values handle
    if len(df.columns[df.isna().any()])>0:
        for i in df.columns[df.isna().any()]:
            df[i].fillna(df[i].mode().loc[0],inpllace=True)

    ## Ordinal encoding for categprical vars
    enc = OrdinalEncoder()
    df_ord = pd.DataFrame(enc.fit_transform(df.drop('class',axis=1)),columns=df.columns[1:])
    class_cat = {'p':0,'e':1}
    df_ord['class'] = df['class'].map(class_cat)

    X,y = df_ord.drop('class',axis=1),df_ord['class']

    ## Feature Selection :- Selecting Most important features by the technique of 
    record = pd.DataFrame({'columns':X.columns,'mutual_info_class_f_score':mutual_info_classif(X, y)}).sort_values('mutual_info_class_f_score',ascending=False).head(15)
    df_ord_mutual_cls = X[record['columns']]
    df_ord_mutual_cls['class'] = y

    new_cols = df_ord_mutual_cls.columns

    df_ord_mutual_cls.to_csv(preprocessed_data_store_path, sep=",", index=False, header=new_cols)

    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    preprocessing_data(config_path=parsed_args.config)

