from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import mysql.connector

app = Flask(__name__)
app.secret_key = 'patri'

# Configuración de la base de datos
db_config = {
    'host': "localbmf4xvockkzpjbcbrlhh-mysql.services.clever-cloud.com",
    'user': "uvygxbx3ujut3sab",
    'password': "gDrHqdsepK62CtCk16ei",
    'database': "bmf4xvockkzpjbcbrlhh"
}

# Función para obtener una conexión a la base de datos
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def home():
    if 'email' in session:
        return render_template("home.html")
    return "You are not logged in <br><a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required!')
            return redirect(url_for('login'))
        
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
    return redirect(url_for('home'))

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

if __name__ == "__main__":
    app.run(debug=True, port=3500)
