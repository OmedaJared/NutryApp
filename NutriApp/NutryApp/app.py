from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'cambia_esto_en_produccion'

def _get_first(form, *keys, default=''):
    """Returns the first non-empty value from the form for the given keys."""
    for k in keys:
        v = form.get(k)
        if v is not None:
            return v
    return default

@app.route('/clear')
def clear():
    """Borrar datos del usuario guardados en sesión y volver al formulario."""
    session.pop('user', None)
    session.pop('authenticated', None)
    flash('Datos borrados.')
    return redirect(url_for('formulario'))

@app.route('/')
def inicio():
    """Home page with information about the application."""
    return render_template('info.html')

@app.route('/formulario')
def formulario():
    """Page that contains the form for user input."""
    # Prefill with session data if available
    user = session.get('user', {})
    return render_template('formulario.html', **user)

@app.route('/resultado', methods=['POST'])
def resultado():
    """Processes the form data and calculates BMI and caloric needs."""
    nombre = _get_first(request.form, 'nombre', 'Nombre', '').strip()
    apellido = _get_first(request.form, 'apellido', 'Apellido', '').strip()
    edad_raw = _get_first(request.form, 'edad', 'Edad', '')
    peso_raw = _get_first(request.form, 'peso', 'Peso', '')
    altura_raw = _get_first(request.form, 'altura', 'Altura', '')
    contraseña = _get_first(request.form, 'contraseña', 'contrasena', '')
    correo_electronico = _get_first(request.form, 'correo_electronico', 'correo', '')
    genero = _get_first(request.form, 'genero', 'Genero', 'masculino')

    try:
        edad = int(edad_raw)
        peso = float(peso_raw)
        altura = float(altura_raw)
    except (ValueError, TypeError):
        error_msg = "Por favor completa todos los campos correctamente."
        return render_template(
            'formulario.html',
            nombre=nombre,
            apellido=apellido,
            edad=edad_raw,
            peso=peso_raw,
            altura=altura_raw,
            genero=genero,
            correo_electronico=correo_electronico,
            contraseña=contraseña,
            error=error_msg
        )

    imc = round(peso / (altura ** 2), 2)

    if imc < 18.5:
        clasificacion = "Bajo peso"
        recomendacion = "Aumenta tu ingesta calórica con alimentos saludables y realiza ejercicios de fuerza."
    elif imc < 25:
        clasificacion = "Peso normal"
        recomendacion = "Mantén una dieta equilibrada y continúa con actividad física regular."
    elif imc < 30:
        clasificacion = "Sobrepeso"
        recomendacion = "Reduce azúcares y grasas, e incrementa tu consumo de frutas y verduras."
    else:
        clasificacion = "Obesidad"
        recomendacion = "Consulta a un especialista y adopta un plan de alimentación controlado."

    if genero.lower() == "masculino":
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad - 161

    calorias_mantenimiento = round(tmb * 1.55, 2)

    # Guardar datos relevantes en sesión para login y uso posterior
    session['user'] = {
        'nombre': nombre,
        'apellido': apellido,
        'edad': edad,
        'peso': peso,
        'altura': altura,
        'correo_electronico': correo_electronico,
        'contraseña': contraseña,
        'genero': genero,
        'imc': imc,
        'clasificacion': clasificacion,
        'recomendacion': recomendacion,
        'calorias': calorias_mantenimiento
    }

    return render_template(
        'formulario.html',
        nombre=nombre,
        apellido=apellido,
        edad=edad,
        peso=peso,
        altura=altura,
        correo_electronico=correo_electronico,
        contraseña=contraseña,
        genero=genero,
        imc=imc,
        clasificacion=clasificacion,
        recomendacion=recomendacion,
        calorias=calorias_mantenimiento
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login with correo and contraseña stored from formulario."""
    if request.method == 'GET':
        return render_template('login.html')
    correo = request.form.get('correo', '').strip()
    contraseña = request.form.get('contraseña', '')
    user = session.get('user')
    if not user:
        flash('No hay datos registrados. Completa primero el formulario.')
        return redirect(url_for('formulario'))
    if correo == user.get('correo_electronico') and contraseña == user.get('contraseña'):
        session['authenticated'] = True
        return redirect(url_for('rutina'))
    flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

# ...existing code...
@app.route('/rutina')
def rutina():
    """Muestra rutina y plan basado en los datos guardados.

    Permite acceso si existe 'user' en sesión incluso cuando no hay flag
    'authenticated' (para que el botón 'Ir a rutina' funcione sin pedir login).
    """
    user = session.get('user')
    if not user:
        flash('Completa el formulario o inicia sesión para ver tu rutina.')
        return redirect(url_for('formulario'))
    # Auto-autenticar si hay datos en sesión para permitir acceso directo
    if not session.get('authenticated'):
        session['authenticated'] = True
    return render_template('rutina.html', user=user)
# ...existing code...

@app.route('/perfil')
def perfil():
    """Muestra toda la información del usuario y botón para cerrar sesión."""
    if not session.get('authenticated'):
        flash('Inicia sesión para ver tu perfil.')
        return redirect(url_for('login'))
    user = session.get('user', {})
    return render_template('perfil.html', user=user)

@app.route('/logout')
def logout():
    """Cerrar sesión y regresar al inicio."""
    session.pop('authenticated', None)
    # conservar user? limpiar todo por seguridad
    session.pop('user', None)
    flash('Sesión cerrada.')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)