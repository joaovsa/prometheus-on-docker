from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './files/'

@app.route('/', methods=['GET'])
def get():
  try:
    return send_file('files/tiny-puppy.jpg', attachment_filename='cute-dog.jpg')
  except Exception as e:
    return str(e)

@app.route('/', methods=['POST'])
def post():
  try:
    f = request.files['files']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tiny-puppy.jpg'))
    return str('Yay! You just posted a file.')
  except Exception as e:
    return str(e)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5001)
