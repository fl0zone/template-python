import os
from flask import Flask, send_from_directory, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Asegúrate de reemplazar los valores de host, dbname, user, password y port
# con los datos de tu base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fl0user:gtpiu7CRvXj3@ep-billowing-salad-34963344.eu-central-1.aws.neon.tech:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silencia la advertencia de SQLAlchemy

db = SQLAlchemy(app)

port = int(os.environ.get("PORT", 5000))


# Define el modelo de la tabla
class Saludo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def home():
   return render_template('index.html')


@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


@app.route('/saludo/<int:id>')
def saludo(id):
    # Busca el registro en la base de datos
    registro = Saludo.query.get(id)
    if registro:
        return f"Hola {registro.id}:{registro.nombre}"
    else:
        return f"No se encontró un saludo con el ID {id}"


if __name__ == "__main__":
    db.create_all()  # Crea las tablas en la base de datos
    app.run(port=port)
