# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
from flask import Flask,request, render_template

app=Flask(__name__,template_folder="templates")
model = pickle.load(open('PRJ.pkl', 'rb'))
sc = pickle.load(open('sc.pkl', 'rb'))
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
    features_name = ['layer_height','wall_thickness','infill_density','infill_pattern','nozzle_temperature', 'bed_temperature','print_speed','fan_speed','roughness','tension_strenght','elongation']
    features_value=[input_features]
    #x_df=pd.DataFrame(features_value,columns=features_name)
    #x=lb.transform(x_df)
    #x=sc.transform(x_df)
    
    
    prediction = model.predict(features_value)
    print(prediction)
    
    output=prediction[0]  
    print(output)
    if(output==1) :
        return render_template("result.html",prediction_text = "The Suggested Material is ABS.(Acrylonitrile butadiene styrene is a common thermoplastic polymer typically used for injection molding applications)")
    elif(output==0) :
        return render_template("result.html",prediction_text = "The Suggested Material is PLA.(PLA, also known as polylactic acid or polylactide, is a thermoplastic made from renewable resources such as corn starch, tapioca roots or sugar cane, unlike other industrial materials made primarily from petroleum)")
    else :
        return render_template("result.html",prediction_text = 'The given values do not match the range of values of the model.Try giving the values in the mnetioned range')
    

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000, debug=False)