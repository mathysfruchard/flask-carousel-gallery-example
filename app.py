from flask import Flask, render_template, url_for, request, jsonify, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clé secrète pour stocker des sessions

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
    # Stocker la commande dans la session
    data = request.json
    image = data.get("image")
    quantity = int(data.get("quantity", 1))

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({"image": image, "quantity": quantity})
    session.modified = True  # Pour sauvegarder les modifications

    return jsonify({"status": "success", "image": image, "quantity": quantity})

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart_items=cart_items, title="Récapitulatif de commande")

if __name__ == "__main__":
    app.run(debug=True)
