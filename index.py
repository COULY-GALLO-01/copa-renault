from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import mysql.connector

app=Flask(__name__)
app.secret_key = 'patri'

#tendriamos k usar la base aca pero pongo esto como para ver que funque
users = {
    'pajan': 'god',
    'pocho': 'pochin'
}

# Configuración de la base de datos
db_config = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'tu_host',
    'database': 'tu_base_de_datos'
}

# Función para obtener una conexión a la base de datos
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def home():
    if 'username' in session:
        return render_template("home.html")
    return "You are not logged in <br><a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT dni_participante, email, password_hash FROM participantes WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
            session['email'] = user['email']
            flash('Login successful!')
            cursor.close()
            conn.close()
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.')
        
        cursor.close()
        conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.')
    return render_template('logout.html')


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

if __name__ == "__main__":
    app.run(debug=True, port=3500)

