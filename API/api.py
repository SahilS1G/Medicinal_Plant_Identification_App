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

class_names = ['Aloevera',
 'Amla',
 'Amruthaballi',
 'Arali',
 'Astma_weed',
 'Badipala',
 'Balloon_Vine',
 'Bamboo',
 'Beans',
 'Betel',
 'Bhrami',
 'Bringaraja',
 'Caricature',
 'Castor',
 'Catharanthus',
 'Chakte',
 'Chilly',
 'Citron lime (herelikai)',
 'Coffee',
 'Common rue(naagdalli)',
 'Coriender',
 'Curry',
 'Doddpathre',
 'Drumstick',
 'Ekka',
 'Eucalyptus',
 'Ganigale',
 'Ganike',
 'Gasagase',
 'Ginger',
 'Globe Amarnath',
 'Guava',
 'Henna',
 'Hibiscus',
 'Honge',
 'Insulin',
 'Jackfruit',
 'Jasmine',
 'Kambajala',
 'Kasambruga',
 'Kohlrabi',
 'Lantana',
 'Lemon',
 'Lemongrass',
 'Malabar_Nut',
 'Malabar_Spinach',
 'Mango',
 'Marigold',
 'Mint',
 'Neem',
 'Nelavembu',
 'Nerale',
 'Nooni',
 'Onion',
 'Padri',
 'Palak(Spinach)',
 'Papaya',
 'Parijatha',
 'Pea',
 'Pepper',
 'Pomoegranate',
 'Pumpkin',
 'Raddish',
 'Rose',
 'Sampige',
 'Sapota',
 'Seethaashoka',
 'Seethapala',
 'Spinach1',
 'Tamarind',
 'Taro',
 'Tecoma',
 'Thumbe',
 'Tomato',
 'Tulsi',
 'Turmeric',
 'ashoka',
 'camphor',
 'kamakasturi',
 'kepala']

def image_ndarray(data)-> np.ndarray:
    np_img = np.array(Image.open(BytesIO(data)))
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



