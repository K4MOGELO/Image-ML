from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from backend.imageProcessing.validation import is_tar_road
from backend.calculations.regModel.pothole_model import get_pothole_model
from backend.calculations.pothole_areas import get_pothole_area


app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"message": "No file part"}), 400
    if 'image' not in request.files:
        return jsonify({"message": "This formated is not supported"})
    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file_location = f'./uploads/{filename}'
        if is_tar_road(file_location): #this is what happens if the image contains a tar road
            pothole_price = 0
            for area in get_pothole_area(f'./uploads/{filename}'):
                price = get_pothole_model(area,0,1)
                pothole_price = pothole_price + price 
            print("there is a road")
            print(f'the price is {pothole_price}')
            return jsonify({"message": f"The cost of this is R{pothole_price}"})
        else: #this happens when the image does not contain a tar road
            print("There is no road")
            message = """The image does not contain a road, please enter an image with a road
                or the image is not clear, please Re-take the picture and try again"""
            print(filename)
            return jsonify({"message": message}), 200








#this is the route for uploading / this will take effect after the user uploads the image
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'image' not in request.files:
#         return render_template('client/quote.html', message='This formated is not supported')
#     file = request.files['image']
#     if file == '':
#         return render_template('client/quote.html', message='Please select an image')
#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
#         file_data = file.read()
        
#         file_location = f'./uploads/{filename}'
#         if is_tar_road(file_location): #this is what happens if the image contains a tar road
#             for area in get_pothole_area(f'./uploads/{filename}'):
#                 pothole_price = 0
#                 price = get_pothole_model(area,1,0)
#                 pothole_price = pothole_price + price 
#             print("there is a road")
#             return render_template('client/quote.html', price = f"The cost of this is R", btn = "Submit Quote")
#         else: #this happens when the image does not contain a tar road
#             print("There is no road")
#             message = """The image does not contain a road, please enter an image with a road
#                 or the image is not clear, please Re-take the picture and try again"""
#             return render_template('client/quote.html', message = message)
#     else:
#         return render_template ('client/quote.html', message="File type not allowed"), 400
    
# @app.route('/upload/customization/service')
# def get_services():
#     return render_template('client/service.html')

# @app.route('/upload/customization', methods = ['POST'])
# def get_customization():
#     return render_template('client/customization.html')

if __name__ == '__main__':
    app.run(debug=True)