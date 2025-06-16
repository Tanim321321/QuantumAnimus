from flask import Flask, send_from_directory

app = Flask(name, static_folder='web', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('web', 'index.html')

if name == 'main':
    app.run(port=5000)