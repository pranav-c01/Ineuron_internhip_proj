# load the train and test
# train algo
# save the metrices, params
import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from get_data import read_params
from urllib.parse import urlparse
import argparse
import joblib
import json
import mlflow

def eval_metrics(actual, pred):
    actual,pred = np.array(actual).flatten(), np.array(pred).flatten()
    f1_score_ = f1_score(actual,pred, average='macro')
    accuracy_score_ = accuracy_score(actual,pred)
    return accuracy_score_,f1_score_

def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    # model hyper parameters
    n_estimators = config["estimators"]["Adaboost"]["params"]["n_estimators"]
    learning_rate = config["estimators"]["Adaboost"]["params"]["learning_rate"]
    algorithm = config["estimators"]["Adaboost"]["params"]["algorithm"]

    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

################### MLFLOW ###############################
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)

    mlflow.set_experiment(mlflow_config["experiment_name"])

    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:
        lr = AdaBoostClassifier(
            n_estimators=n_estimators, 
            learning_rate=learning_rate,
            algorithm=algorithm, 
            random_state=random_state)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)
        
        (accuracy_score_,f1_score_) = eval_metrics(test_y, predicted_qualities)

# Log params into mlflow platform
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("algorithm", algorithm)

# log metrics value as per experiment for comparison  for mlflow
        mlflow.log_metric("accuracy_score_", accuracy_score_)
        mlflow.log_metric("f1_score_", f1_score_)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                lr, 
                "model", 
                registered_model_name=mlflow_config["registered_model_name"])
        else:
            mlflow.sklearn.load_model(lr, "model")
 


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
