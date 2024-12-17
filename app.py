from flask import Flask, render_template, url_for, request, jsonify, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clé secrète pour stocker les sessions

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

    # Ajouter au panier ou mettre à jour la quantité si déjà existant
    for item in session["cart"]:
        if item["image"] == image:
            item["quantity"] += quantity
            break
    else:
        session["cart"].append({"image": image, "quantity": quantity})

    session.modified = True
    return jsonify({"status": "success", "image": image, "quantity": quantity})

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart_items=cart_items, title="Récapitulatif de commande")

@app.route("/update_cart", methods=["POST"])
def update_cart():
    data = request.json
    action = data.get("action")
    image = data.get("image")

    if "cart" in session:
        session["cart"] = [
            {"image": item["image"], "quantity": item["quantity"] - 1} if action == "decrease" and item["image"] == image and item["quantity"] > 1 else
            item for item in session["cart"] if not (action == "delete" and item["image"] == image)
        ]
    session.modified = True
    return jsonify({"status": "success", "cart": session["cart"]})

if __name__ == "__main__":
    app.run(debug=True)
