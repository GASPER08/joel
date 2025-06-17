from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["EquipoMamba"]
jugadores = db["Jugadores"]

@app.route('/')
def index():
    datos = jugadores.find()
    return render_template('index.html', jugadores=datos)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        sexo = request.form['sexo']
        if nombre and numero and sexo:
            jugadores.insert_one({"Nombre": nombre, "Numero": numero, "Sexo": sexo})
        return redirect(url_for('index'))
    return render_template('form.html', accion="Crear")

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    jugador = jugadores.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = request.form['numero']
        sexo = request.form['sexo']
        jugadores.update_one({"_id": ObjectId(id)}, {"$set": {"Nombre": nombre, "Numero": numero, "Sexo": sexo}})
        return redirect(url_for('index'))
    return render_template('form.html', jugador=jugador, accion="Editar")

@app.route('/eliminar/<id>')
def eliminar(id):
    jugadores.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
