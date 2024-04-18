from fastapi import FastAPI ,File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_details(class_name,ismedicinal):
    if ismedicinal== True:
        message = 'Give me five line information, highlighting its uses and significance, about this medicinal plant: ' + str(class_name)
        details = model.generate_content(message)
        return details.candidates[0].content.parts[0].text
    else:
        return None

model_ld = tf.keras.layers.TFSMLayer('../model/mpim_final', call_endpoint='serving_default')

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

def image_ndarray(data):
    image = Image.open(BytesIO(data))
    image = image.resize((224,224))
    np_img = np.array(image)
    return np_img

@app.get("/ping")
async def ping():
    return "Hello I am Alive"

@app.post("/predict/")
async def predict(file: UploadFile):
    image = image_ndarray(await file.read())
    img_bth =  np.expand_dims(image,0)
    predictions = model_ld(img_bth)
    print(predictions["dense"])
    confidence = np.max(predictions["dense"])
    predict_class = class_names[np.argmax(predictions["dense"])]
    is_medicinal = True if confidence > 0.5 else False
    details = get_details(predict_class,is_medicinal)
    return {
            'class': predict_class,
            'confidence':float(confidence),
            'ismedicinal':is_medicinal,
            'details':details
            }
@app.post("/fx/")
async def get_features(file: UploadFile):
    img = iamge_ndarray(await file.read())
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    green_lower = (36, 0, 0)
    green_upper = (86, 255, 255)
    brown_lower = (8, 60, 20)
    brown_upper = (30, 255, 200)
    yellow_lower = (21, 39, 64)
    yellow_upper = (40, 255, 255)

    mask_green = cv.inRange(hsv, green_lower, green_upper)
    mask_brown = cv.inRange(hsv, brown_lower, brown_upper)
    mask_yellow = cv.inRange(hsv, yellow_lower, yellow_upper)
    mask_combined = cv.bitwise_or(mask_green, mask_brown)
    mask_combined = cv.bitwise_or(mask_combined, mask_yellow)

    result = cv.bitwise_and(img, img, mask=mask_combined)
    contours, _ = cv.findContours(mask_combined, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv.boundingRect(max(contours, key=cv.contourArea))

    zoomed_in_img = result[y:y+h, x:x+w]
    zoomed_in_img_blurred = cv.GaussianBlur(zoomed_in_img, (5, 5), 0)
    zoomed_in_img_rgb = cv.cvtColor(zoomed_in_img_blurred, cv.COLOR_BGR2RGB)
    zoomed_in_img_gray = cv.cvtColor(zoomed_in_img_rgb, cv.COLOR_BGR2GRAY)

    edges_noraml = cv.Canny(zoomed_in_img_gray, 100, 200)
    zoomed_in_img_gray = cv.cvtColor(zoomed_in_img_blurred, cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(zoomed_in_img_gray)
    edges = cv.Canny(enhanced_img, 100, 200)

    _, img_bytes = cv.imencode('.png', zoomed_in_img_rgb)
    _, enhanced_bytes = cv.imencode('.png', enhanced_img)
    _, edges_bytes = cv.imencode('.png', edges)
    _, edges_normal_bytes = cv.imencode('.png', edges_normal)

    return Response(content=img_bytes.tobytes(), media_type="image/png"), \
           Response(content=enhanced_bytes.tobytes(), media_type="image/png"), \
           Response(content=edges_bytes.tobytes(), media_type="image/png"), \
           Response(content=edges_normal_bytes.tobytes(), media_type="image/png")




if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8000)



