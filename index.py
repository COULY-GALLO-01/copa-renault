from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import hashlib
import mysql.connector
import json

app = Flask(__name__)
app.secret_key = 'patri'

db_config = {
    'host': "localbmf4xvockkzpjbcbrlhh-mysql.services.clever-cloud.com",
    'user': "uvygxbx3ujut3sab",
    'password': "gDrHqdsepK62CtCk16ei",
    'database': "bmf4xvockkzpjbcbrlhh"
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def home():
    if 'nombres' not in session:
        flash('inicie sesion primero.')
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

def guardar_usuarios(users):
    with open('usuarios.json', 'w') as archivo:
        json.dump(users, archivo)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        nombre = request.form.get('nombre_sign') 
        contraseña = request.form.get('password_sign')
        
        if not nombre or not contraseña:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('sign_in'))
        
        if nombre in users:
            flash('El usuario ya existe.')
            return redirect(url_for('sign_in'))
        
        users[nombre] = {'nombres': nombre, 'password': contraseña }
        guardar_usuarios(users)
        
        flash('¡Ya has ingresado!')
        return redirect(url_for('login'))
    
    return render_template('sign_in.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombres = request.form.get('nombres')  
        password = request.form.get('password')
        
        if not nombres or not password:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('login'))
        
        if nombres in users:
            user = users[nombres]
            if user['password'] == password:
                session['nombres'] = user['nombres']
                flash('¡Inicio de sesión exitoso!')
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta.')
        else:
            flash('El usuario no existe.')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('nombres', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route("/resultados")
def resultados():
    return render_template("resultados.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    nombre = request.form['nombre']
    return f'Formulario enviado por {nombre}'

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

if __name__ == '__main__':
    app.run(debug=True, port=3500)
