import pickle
import numpy as np
import pandas as pd
from datetime import timedelta
from catboost import CatBoostClassifier
import math
import os

def load_traffic_forecaster(model_path, scaler_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    def apply_transform(input_data):
        return scaler.transform(input_data)

    def apply_inverse_transform(scaled_prediction):
        unscaled = scaler.inverse_transform(scaled_prediction)
        return np.where(unscaled < 0, 0, unscaled)
    
    def predict_traffic_volume(prev_endog, future_exog, horizon):
        prepared_input = apply_transform(prev_endog)
        scaled_forecast = model.forecast(
            prepared_input, 
            steps=horizon, 
            exog_future=future_exog
        )
        prediction = apply_inverse_transform(scaled_forecast)
        return prediction
    
    return predict_traffic_volume


def load_traffic_classifier(model_path, scaler_path):
    model = CatBoostClassifier()
    model.load_model(model_path)

    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    def prepare_input_features(traffic_series, external_factors):
        standardized_traffic_series = scaler.transform(traffic_series)
        input = []
        for i in range(len(traffic_series)-1):
            input.append(np.concatenate([standardized_traffic_series[i + 1], standardized_traffic_series[i], external_factors[i]]))
        
        return np.array(input)

    def predict_traffic_status(traffic_data, external_factors):
        model_input = prepare_input_features(traffic_data, external_factors)
        return np.squeeze(model.predict(model_input))
    
    return predict_traffic_status

def load_local_data(csv_path):
    cols = ['CarCount', 'BikeCount', 'BusCount', "Hour" ]
    data = pd.read_csv(csv_path, index_col=0)[cols]

    def convert_time_to_index(time):
        index = data.loc[data['Hour'] == time.hour].index[8]
        print(index + time.minute // 15)
        return index + time.minute // 15

    def get_prev_traffic(crossroad_id, time, lag):
        index = convert_time_to_index(time)
        return data[['CarCount', 'BikeCount', 'BusCount']].iloc[index - lag: index].values
    
    return get_prev_traffic

def get_future_exog(time, horizon):
    def get_exog(time):    
        hour = time.hour
        sin_hour = math.sin(2 * np.pi * hour / 24)
        cos_hour = math.cos(2 * np.pi * hour / 24)
        weekday = time.weekday()
        sin_weekday = math.sin(2 * np.pi * weekday / 7)
        cos_weekday = math.cos(2 * np.pi * weekday / 7)
        return [weekday, sin_hour, cos_hour, sin_weekday, cos_weekday]

    future_exog = []
    for i in range(0, horizon):
        delta = timedelta(minutes=15 * i)
        future_exog.append(get_exog(time + delta))
    return np.array(future_exog)

VAR_MODEL_FILENAME = 'var.pkl'
STD_SCALER_FILENAME = 'std-scaler.pkl'
CATBOOST_MODEL_FILENAME = 'catboost.cbm'

def create_predictor(get_prev_traffic, horizon, lag, base_path):
    def resolve_path(file):
        return os.path.join(base_path, file)
    
    var_model_path = resolve_path(VAR_MODEL_FILENAME)
    scaler_model_path = resolve_path(STD_SCALER_FILENAME)
    catboost_model_path = resolve_path(CATBOOST_MODEL_FILENAME)

    forecaster = load_traffic_forecaster(var_model_path, scaler_model_path)
    classifier = load_traffic_classifier(catboost_model_path, scaler_model_path)

    def create_classifier_input(prev_traffic, future_traffic):
        return np.vstack([prev_traffic[-1], future_traffic])
    
    def predict(time, crossroad_id):
        prev_traffic = get_prev_traffic(crossroad_id, time, lag)
        future_exog = get_future_exog(time, horizon)

        traffic_volumes = forecaster(prev_traffic, future_exog[:, 1:], horizon)
        traffic_series = create_classifier_input(prev_traffic, traffic_volumes)
        predictions = classifier(traffic_series, future_exog[:, :3])
        return predictions

    return predict
