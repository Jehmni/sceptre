from flask import Flask, send_from_directory
from routes.transcribe import transcribe_bp
import os

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.register_blueprint(transcribe_bp, url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/scripts/<path:path>')
def send_script(path):
    return send_from_directory(os.path.join(app.static_folder, 'scripts'), path)

@app.route('/styles/<path:path>')
def send_style(path):
    return send_from_directory(os.path.join(app.static_folder, 'styles'), path)

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(os.path.join(app.static_folder, 'images'), path)

if __name__ == "__main__":
    app.run(debug=True)