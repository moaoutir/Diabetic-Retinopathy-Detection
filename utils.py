from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import os
import numpy as np
from tensorflow.keras.models import load_model
import json
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

img_height = 224
img_width = 224
model_persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "./model/eff_B0.keras"))

model_classes = ['Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe']

def image_prediction(image_bytes):
    result = []
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((img_width, img_height))

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)
    predictions = __model.predict(img_array)
    print(predictions,"---")
    predicted_class_index = np.argmax(predictions, axis=1)
    predicted_class_index = predicted_class_index[0]
    print("Predicted class index:", predicted_class_index)
    result.append({
            'class': class_number_to_name(predicted_class_index),
            'class_probability': np.around(predictions,2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })
    print(result)
    return result

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name
    global __model

    with open('./artifacts/class_dictionary.json', 'r') as f:
            __class_name_to_number = json.load(f)
            __class_number_to_name = {n:p for p,n in __class_name_to_number.items()}

    __model = load_model(model_persist_directory)
    print("loading saved artifacts...done")

def class_number_to_name(number_class):
     return __class_number_to_name[number_class]    