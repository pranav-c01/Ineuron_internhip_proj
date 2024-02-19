import yaml
import os
import json
import joblib
import numpy as np


params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")

class NotInRange(Exception):
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)

#class NotInCols(Exception):
#    def __init__(self, message="Not in cols"):
#        self.message = message
#        super().__init__(self.message)



def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    ord_encoder_path = config["ord_encoder_path"]
    model = joblib.load(model_dir_path)
    ord_encoder = joblib.load(ord_encoder_path)

    selected_cols = ['cap-shape','cap-color','bruises','odor','gill-spacing','gill-size','gill-color','stalk-root','stalk-surface-above-ring','stalk-surface-below-ring','stalk-color-above-ring','stalk-color-below-ring','ring-number','ring-type','spore-print-color','population','habitat']
    
    try:
        # print("\n\n\n\n\nDATA",data,"\n\n\n")
        trans_data = list("p") + list(data.values())
        encoded_data = ord_encoder.transform([trans_data])[0]
        encoded_dict = {}
        for i, col in enumerate(data.keys()):
            encoded_dict[col] = encoded_data[i+1]
        encoded_dict = {col: encoded_dict[col] for col in selected_cols}

        #print(f"\n\nBefore prediction\nData={[list(encoded_dict.values())]}\n")
        prediction = model.predict([list(encoded_dict.values())])[0]
        #prediction = model.predict([[7.7,0.56,0.08,2.5,0.114,14.0,46.0,0.9971,3.24,0.66,9.6]])
        if  prediction in [0.0,1.0]:
            return ["p" if prediction==1.0 else "e"]
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"


def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
#    def _validate_cols(col):
#        schema = get_schema()
#        actual_cols = schema.keys()
#        if col not in actual_cols:
#            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        if not (dict_request[col][0] in schema[col]) :
            raise NotInRange

    for col, val in dict_request.items():
#        _validate_cols(col)
        _validate_values(col, val)
    
    return True


def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request
#        print("data before list comp")
#        data = [list(map(float, i)) for i in list(data)]
#        print("data after list comp\n\n",data,"\n\n",type(data),np.array(data).reshape(1,-1))       
#        response = predict(np.array(data).reshape(1,-1))
        #print(f"\n\n\nDATA :- \n\n{data}")
        response = predict(dict_request)
        return response
    else:
        print("validation failed")

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = dict_request
#            data = np.array([list(map(float, i)) for i in list(data)]).reshape(1,-1)
#            print(data)
            response = predict(data)
            response = {"response": response}
            return response
            
    except NotInRange as e:
        response = {"the_expected_range": get_schema(), "response": str(e) }
        return response

#    except NotInCols as e:
#        response = {"the_exected_cols": get_schema().keys(), "response": str(e) }
#        return response


    except Exception as e:
        response = {"response": str(e) }
        return response

