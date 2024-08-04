from flask import Flask, render_template, request, redirect, url_for
import os
from io import BytesIO
from backend.imageProcessing.validation import is_tar_road
from backend.calculations.regModel.pothole_model import get_pothole_model
from backend.calculations.pothole_areas import get_pothole_area


app = Flask(__name__)


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

#inital route / login
@app.route('/')
def login():
    return render_template('client/quote.html')



#this is the route for uploading / this will take effect after the user uploads the image
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return render_template('client/quote.html', message='This formated is not supported')
    file = request.files['image']
    if file == '':
        return render_template('client/quote.html', message='Please select an image')
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file_data = file.read()
        
        file_location = f'./uploads/{filename}'
        if is_tar_road(file_location): #this is what happens if the image contains a tar road
            for area in get_pothole_area(f'./uploads/{filename}'):
                pothole_price = 0
                price = get_pothole_model(area,1,0)
                pothole_price = pothole_price + price 
            print("there is a road")
            return render_template('client/quote.html', price = f"The cost of this is R", btn = "Submit Quote")
        else: #this happens when the image does not contain a tar road
            print("There is no road")
            message = """The image does not contain a road, please enter an image with a road
                or the image is not clear, please Re-take the picture and try again"""
            return render_template('client/quote.html', message = message)
    else:
        return render_template ('client/quote.html', message="File type not allowed"), 400
    
@app.route('/upload/customization/service')
def get_services():
    return render_template('client/service.html')

@app.route('/upload/customization', methods = ['POST'])
def get_customization():
    return render_template('client/customization.html')

if __name__ == '__main__':
    app.run(debug=True)