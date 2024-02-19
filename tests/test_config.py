import json
import logging
import os
import joblib
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service
import sys

sys.path.append("..")

input_data = {
    "incorrect_range":
    {"cap-shape": "q",
    "cap-surface": "q",
    "cap-color": "q",
    "bruises": "q",
    "odor": "q",
    "gill-attachment": "q",
    "gill-spacing": "q",
    "gill-size": "q",
    "gill-color": "q",
    "stalk-shape": "q",
    "stalk-root": "q",
    "stalk-surface-above-ring": "q",
    "stalk-surface-below-ring": "q",
    "stalk-color-above-ring": "q",
    "stalk-color-below-ring": "q",
    "veil-type": "q",
    "veil-color": "q",
    "ring-number": "q",
    "ring-type": "q",
    "spore-print-color": "q",
    "population": "q",
    "habitat": "q"
    },

    "correct_range":
    {"cap-shape": "x",
     "cap-surface": "s",
     "cap-color": "n",
     "bruises": "t",
     "odor": "p",
     "gill-attachment": "f",
     "gill-spacing": "c",
     "gill-size": "n",
     "gill-color": "k",
     "stalk-shape": "e",
     "stalk-root": "e",
     "stalk-surface-above-ring": "s",
     "stalk-surface-below-ring": "s",
     "stalk-color-above-ring": "w",
     "stalk-color-below-ring": "w",
     "veil-type": "p",
     "veil-color": "w",
     "ring-number": "o",
     "ring-type": "p",
     "spore-print-color": "k",
     "population": "s",
     "habitat": "u"}

}

TARGET_range = ["e","p"]

def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    #print(res,"\n\n\n\n\n\n\n\n\n\n",res[0],type(res),type(res[0]))
    assert (res[0] in TARGET_range)
    #assert  res[0] == "p" or res[0] == "e"
    #print("End of test_form_response")

def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
   # print(res,type(res))
    assert  res['response'][0] in  TARGET_range
  #  print("End of test_api_response")

#def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
#    with pytest.raises(prediction_service.prediction.NotInRange):
#        res = form_response(data)

#def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
#    res = api_response(data)
#    assert res["response"] == prediction_service.prediction.NotInRange().message

#def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
#    res = api_response(data)
#    assert res["response"] == prediction_service.prediction.NotInCols().message

#test_form_response_correct_range()
#test_api_response_correct_range()