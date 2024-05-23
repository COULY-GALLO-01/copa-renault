from flask import Flask, render_template, request, redirect, url_for, flash, session

app=Flask(__name__)
app.secret_key = 'patri'

users = {
    'pajan': 'god',
    'pocho': 'pochin'
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template("home.html")
    return "You are not logged in <br><a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
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

