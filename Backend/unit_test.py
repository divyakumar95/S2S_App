import unittest
import os
import pandas as pd
from model import modelClass
#from tensorflow import keras
import keras
import json

Base_dir = os.getcwd()

SAMPLE_PATH = 'uploads/Ger-01.wav'
json_path = Base_dir+'/models/model_1.json'
model_path = Base_dir+'/models/model_1.h5'
input_path = Base_dir+'/uploads'
output_path = Base_dir+'/tempOut'
WavShape = 40,151

print(input_path)
def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

class Test(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_1_load_module(self):
        load = modelClass(model_json=json_path, model_path=model_path, input_path=input_path, output_path=output_path, wav_shape=WavShape)
        temp = load.load_model(model_json=json_path, model_path= model_path)
        self.assertIsInstance(temp, keras.engine.sequential.Sequential)

    def test_2_load_audio(self):
        load = modelClass(model_json=json_path, model_path=model_path, input_path=input_path, output_path=output_path, wav_shape=WavShape)
        temp = load.load_audio(input_path=input_path)
        self.assertIsInstance(temp, pd.DataFrame)

    def test_3_predict(self):
        load = modelClass(model_json=json_path, model_path=model_path, input_path=input_path, output_path=output_path, wav_shape=WavShape)
        temp = load.predict(model_json=json_path, model_path=model_path, wav_shape=WavShape, output_path=output_path)
        self.assertIsInstance(temp, str)

if __name__ == '__main__':
    unittest.main()