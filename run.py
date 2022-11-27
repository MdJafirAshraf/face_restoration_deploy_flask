import os, cv2
import inference_gfpgan
from flask import Flask, request, render_template
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['RESULT_FOLDER'] = 'static/result/restored_imgs'
run_with_ngrok(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/upload', methods = ['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        img = cv2.imread(file_path)
        height, width, channels = img.shape
        print(height, width)

        inference_gfpgan.start()
        out_path = os.path.join(app.config['RESULT_FOLDER'], file.filename)
        
        img_1 = cv2.imread(out_path)
        out_img = cv2.resize(img_1, (width, height))
        cv2.imwrite(out_path, out_img)

        return render_template("index.html", image_path = file_path, output_path = out_path)



if __name__ == '__main__':
    app.run()