from typing import Annotated
from fastapi import FastAPI ,File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
from tensorflow.keras.models import load_model
import tensorflow_hub as hub

def load_custom_model(model_path):
    return load_model(
        model_path,
        custom_objects={'KerasLayer': hub.KerasLayer}
    )

model_ld = load_custom_model('./model/mpia_fmod.h5')

app = FastAPI()

def image_ndarray(data)-> np.ndarray:
    np_img = np.arrray(Image.open(BytesIO(data)))
    return np_img

@app.get("/ping")
async def ping():
    return "Hello I am Alive"

@app.post("/predict/")
async def predict(file: UploadFile):
    image = image_ndarray(await file.read())
    img_bth =  np.expand_dims(np_img,0)
    predictions = model_ld.predict(img_bth)
    predict_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    is_medicinal = True if confidence > 0.5 else False
    return {
            'class': predict_class,
            'confidence':float(confidence),
            'ismedicinal':is_medicinal
            }

if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8000)



