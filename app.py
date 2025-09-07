from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="adan123",
    database="product_db"
)
cursor = db.cursor(dictionary=True)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        oldprice = request.form["oldprice"]
        discount = int(request.form["discount"])
        image = request.form["image_url"]
        rating = request.form["rating"]

        cursor.execute("INSERT INTO products (name, price, discount, img_url, oldprice, rating) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, discount, image, oldprice, rating))
        db.commit()
        return redirect("/upload")
    
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("upload.html", products=products)
    
@app.route("/")
def gallery():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("gallery.html", products=products)


@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    db.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        oldprice = float(request.form["oldprice"])
        discount = int(request.form["discount"])
        image = request.form["image_url"]
        rating = float(request.form["rating"])

        cursor.execute("""
            UPDATE products 
            SET name=%s, price=%s, oldprice=%s, discount=%s, img_url=%s, rating=%s
            WHERE id=%s
        """, (name, price, oldprice, discount, image, rating, id))
        db.commit()
        return redirect("/")

    # Fetch existing product for form
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    return render_template("edit.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)
