# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
from flask import Flask,request, render_template



import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "tyPK4UQwuZTabQw_m-yne58L1VdeViVVcmonkTLSk3Oo"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app=Flask(__name__,template_folder="templates")
model = pickle.load(open('PRJ.pkl', 'rb'))
#sc = pickle.load(open('sc.pkl', 'rb'))
lb = pickle.load(open('lb.pkl', 'rb'))

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('result.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    #features_value = [np.array(input_features)]
    #print(features_value)
    total=[input_features]
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields":['layer_height','wall_thickness','infill_density','infill_pattern','nozzle_temperature', 'bed_temperature','print_speed','fan_speed','roughness','tension_strenght','elongation'] ,"values":total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/124c3f5c-b772-4c95-af1f-fb36a7d0f024/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    print(predictions)
    pred = response_scoring.json()

    output = pred['predictions'][0]['values'][0][0]
  
    print(output)
    
    if(output==1) :
        return render_template("result.html",prediction_text = "The Suggested Material is ABS.(Acrylonitrile butadiene styrene is a common thermoplastic polymer typically used for injection molding applications)")
    elif(output==0) :
        return render_template("result.html",prediction_text = "The Suggested Material is PLA.(PLA, also known as polylactic acid or polylactide, is a thermoplastic made from renewable resources such as corn starch, tapioca roots or sugar cane, unlike other industrial materials made primarily from petroleum)")
    else :
        return render_template("result.html",prediction_text = 'The given values do not match the range of values of the model.Try giving the values in the mnetioned range')
    

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000, debug=False)