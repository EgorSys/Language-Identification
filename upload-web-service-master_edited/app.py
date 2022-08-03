import os
import uuid
from flask import Flask, render_template, request
import json


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
    timestamps = {"timestamps": [
        {"start": 0.05, "end": 0.5, "id": 0}, {"start": 1.2, "end": 2.5, "id": 1}
    ]}

    return render_template('index.html', timestamps=timestamps)
