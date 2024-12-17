from flask import Flask, render_template, url_for, request, jsonify
import os

app = Flask(__name__)

# Configuration du dossier static pour les images
IMAGE_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route("/")
def index():
    # Récupérer les images directement dans static/
    images = [url_for('static', filename=img) for img in os.listdir(IMAGE_FOLDER) if img.endswith(('jpg', 'png', 'jpeg'))]
    return render_template("index.html", images=images, title="Galerie d'images")

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    # Récupérer les données depuis le bouton d'ajout
    data = request.json
    image = data.get("image")
    quantity = data.get("quantity", 1)
    return jsonify({"status": "success", "image": image, "quantity": quantity})

if __name__ == "__main__":
    app.run(debug=True)
