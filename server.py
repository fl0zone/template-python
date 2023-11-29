import os
from flask import Flask, send_from_directory, render_template, redirect, jsonify
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

def verificar_expiracion(fecha):
    fecha_expiracion = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    fecha_actual = datetime.now()
    return fecha_actual > fecha_expiracion

def obtener_fecha_expiracion_por_nombre(name):
    conn = psycopg2.connect(
        dbname=os.getenv('dbname'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host')
    )
    cursor = conn.cursor()
    cursor.execute("SELECT exp_date FROM licencias_cda WHERE name = %s", (name,))
    fecha = cursor.fetchone()
    conn.close()
    if fecha:
        return fecha[0]
    else:
        return None

@app.route('/verificar-expiracion', methods=['POST'])
def verificar_fecha_expiracion():
    data = request.get_json()
    if 'name' in data:
        nombre = data['name']
        fecha_exp = obtener_fecha_expiracion_por_nombre(nombre)
        if fecha_exp:
            expirado = verificar_expiracion(str(fecha_exp))
            return jsonify({'expirado': expirado})
        else:
            return jsonify({'error': 'Nombre no encontrado en la base de datos'}), 404
    else:
        return jsonify({'error': 'Se necesita proporcionar el nombre'}), 400


if __name__ == "__main__":
    app.run(port=port)