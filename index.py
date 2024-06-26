from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'patri'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uvygxbx3ujut3sab:gDrHqdsepK62CtCk16ei@bmf4xvockkzpjbcbrlhh-mysql.services.clever-cloud.com:3306/bmf4xvockkzpjbcbrlhh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# tabla usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

#tabla equipo
class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Equipo {self.nombre}>'

#tabla resultados
class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deporte = db.Column(db.String(50), nullable=False)
    equipo1_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    equipo2_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    puntuacion1 = db.Column(db.Integer, nullable=False)
    puntuacion2 = db.Column(db.Integer, nullable=False)
    ganador = db.Column(db.String(80), nullable=False)

    equipo1 = db.relationship('Equipo', foreign_keys=[equipo1_id])
    equipo2 = db.relationship('Equipo', foreign_keys=[equipo2_id])

    def __repr__(self):
        return f'<Resultado {self.deporte}: {self.equipo1.nombre} vs {self.equipo2.nombre}>'


# Crea todas las tablas
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'nombres' not in session:
        flash('Inicie sesión primero.')
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        nombre = request.form.get('nombre_sign')
        contraseña = request.form.get('password_sign')

        if not nombre or not contraseña:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('sign_in'))

        # Verifica si existe en la base de datos
        if User.query.filter_by(username=nombre).first():
            flash('El usuario ya existe. Por favor, elija otro nombre de usuario.')
            return redirect(url_for('sign_in'))

        # Crea un nuevo usuario y lo agrega a la base 
        new_user = User(username=nombre, password=contraseña)
        db.session.add(new_user)
        db.session.commit()

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

        user = User.query.filter_by(username=nombres).first()
        if user and user.password == password:
            session['nombres'] = nombres
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('nombres', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

@app.route("/resultados")
def resultados():
    resultados = Resultado.query.all() 
    return render_template("resultados.html", resultados=resultados)


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    nombre = request.form['nombre']
    return f'Formulario enviado por {nombre}'

@app.route('/perfil')
def perfil():
    if 'nombres' in session:
       nombre_ususario = session['nombres']
       return render_template('perfil.html', nombre_perfil=nombre_ususario)
    else:
        flash('Inicie sesión primero.')
        return redirect(url_for('login'))

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        deporte = request.form['deporte']
        equipo1_nombre = request.form['equipo1']
        puntuacion1 = int(request.form['puntuacion1'])
        equipo2_nombre = request.form['equipo2']
        puntuacion2 = int(request.form['puntuacion2'])

        # Verifica si los equipos existen en la base y los crea si no hay
        equipo1 = Equipo.query.filter_by(nombre=equipo1_nombre).first()
        if not equipo1:
            equipo1 = Equipo(nombre=equipo1_nombre)
            db.session.add(equipo1)

        equipo2 = Equipo.query.filter_by(nombre=equipo2_nombre).first()
        if not equipo2:
            equipo2 = Equipo(nombre=equipo2_nombre)
            db.session.add(equipo2)

        db.session.commit()

        
        if puntuacion1 > puntuacion2:
            ganador = equipo1.nombre
        elif puntuacion2 > puntuacion1:
            ganador = equipo2.nombre
        else:
            ganador = 'Empate'

        # Crea un nuevo resultado
        resultado = Resultado(deporte=deporte, equipo1_id=equipo1.id, equipo2_id=equipo2.id, puntuacion1=puntuacion1, puntuacion2=puntuacion2, ganador=ganador)
        db.session.add(resultado)
        db.session.commit()

        flash('Resultado agregado correctamente.')
        return redirect(url_for('resultados'))

    return render_template('agregar.html')

if __name__ == '__main__':
    app.run(debug=True, port=3500)
