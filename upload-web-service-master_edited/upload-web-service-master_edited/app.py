import os
import uuid
from flask import Flask, render_template, request
import json

import torchaudio
from speechbrain.pretrained import EncoderClassifier


language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
def classify(path, language_id):
    signal, sr = torchaudio.load(path, channels_first=False)
    signal = language_id.audio_normalizer(signal, sr)
    prediction =  language_id.classify_batch(signal)
    pred_lang_name = prediction[3][0][4:]
    return pred_lang_name
    

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_files():
    if not os.path.exists(app.config['UPLOAD_PATH']):
        os.makedirs(app.config['UPLOAD_PATH'])

    uploaded_files = request.files.getlist('file')
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.filename.lower())[-1]
        filename = str(uuid.uuid4()) + file_extension
        document_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(document_path)
    
    pred_langs = []   
    for uploaded_file in os.listdir(app.config['UPLOAD_PATH']):
        file_extension = os.path.splitext(uploaded_file.lower())[-1]
        print('File extention:', file_extension)
        if file_extension not in ['.mp3', '.wav', '.flac']:
            continue
        pred_lang = classify(app.config['UPLOAD_PATH']+'/'+uploaded_file, language_id)
        pred_langs.append(pred_lang)
    
    for fl in os.listdir(app.config['UPLOAD_PATH']):
        os.remove(app.config['UPLOAD_PATH']+'/'+fl)
        
    return render_template('result.html', pred_langs = pred_langs)
