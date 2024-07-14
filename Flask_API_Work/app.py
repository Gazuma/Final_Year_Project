from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = load_model("./imageclassifier.keras")

def preprocess_image(image):
    # Resize the image to 256x256
    image = cv2.resize(image, (256, 256))
    # Convert the image to a float32 numpy array and normalize
    image = image.astype('float32') / 255.0
    # Expand dimensions to match model input shape (batch size, height, width, channels)
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': "No selected file"}), 400
    
    # Read the image from the file stream
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': "Invalid image"}), 400
    
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    predictions_list = predictions.tolist()

    return jsonify(predictions=predictions_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
