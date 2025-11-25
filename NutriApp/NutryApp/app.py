# ...existing code...
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'cambia_esto_en_produccion'

api_key="tN2XZsdySpg5RvS75AJNOLrDHjPbny4W64vfXF3N"
API_URL="https://api.nal.usda.gov/fdc/v1/foods/search"

def _get_first(form, *keys, default=''):
    """Retorna el primer valor no vacío del formulario."""
    for k in keys:
        v = form.get(k)
        if v is not None and v != '':
            return v
    return default

RECIPES = [
    {
        'id': 1,
        'title': 'Bowl de avena con frutas y frutos secos',
        'description': 'Desayuno energético con avena, leche, plátano, frutos secos y miel.',
        'ingredients': [
            '60 g avena',
            '250 ml leche o bebida vegetal',
            '1 plátano',
            '1 cucharada de miel',
            '30 g frutos secos (almendras, nueces)'
        ],
        'steps': [
            'Cocina la avena con la leche a fuego medio por 5-7 minutos.',
            'Sirve en un bowl, añade rodajas de plátano, frutos secos y miel al gusto.'
        ]
    },
    {
        'id': 2,
        'title': 'Ensalada de quinoa y pollo',
        'description': 'Almuerzo balanceado con proteína magra y carbohidratos complejos.',
        'ingredients': [
            '100 g quinoa cocida',
            '120 g pechuga de pollo a la plancha',
            'Tomate cherry',
            'Pepino',
            'Aderezo (aceite oliva, limón, sal)'
        ],
        'steps': [
            'Cocina la quinoa según paquete y deja enfriar.',
            'Corta el pollo en tiras y mezcla con la quinoa y verduras.',
            'Aliña al gusto y sirve.'
        ]
    },
    {
        'id': 3,
        'title': 'Salmón al horno con vegetales',
        'description': 'Cena rica en proteínas y grasas saludables.',
        'ingredients': [
            '150 g filete de salmón',
            'Brócoli, zanahoria y espárragos',
            'Limón, sal y pimienta'
        ],
        'steps': [
            'Coloca el salmón y vegetales en bandeja, rocía con aceite y limón.',
            'Hornea a 180°C por 15-20 minutos hasta que el salmón esté cocido.'
        ]
    }
]
# ...existing code...

@app.route('/')
def inicio():
    """Página de inicio con información."""
    return render_template('info.html')

@app.route('/api')
def apis():
    

@app.route('/formulario')
def formulario():
    """Página del formulario de registro."""
    user = session.get('user', {})
    error = session.pop('error', None)
    return render_template('formulario.html', error=error, **user)

@app.route('/resultado', methods=['POST'])
def resultado():
    """Procesa formulario y calcula IMC y calorías."""
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    correo_electronico = request.form.get('correo_electronico', '').strip()
    contraseña = request.form.get('contraseña', '')
    genero = request.form.get('genero', 'masculino').lower()
    
    try:
        edad = int(request.form.get('edad', 0))
        peso = float(request.form.get('peso', 0))
        altura = float(request.form.get('altura', 0))
    except (ValueError, TypeError):
        session['error'] = 'Error: Verifica que edad, peso y altura sean números válidos.'
        return redirect(url_for('formulario'))
    
    if edad <= 0 or peso <= 0 or altura <= 0:
        session['error'] = 'Error: Los valores deben ser mayores a 0.'
        return redirect(url_for('formulario'))
    
    imc = round(peso / (altura ** 2), 2)
    
    if imc < 18.5:
        clasificacion = 'Bajo peso'
        recomendacion = 'Aumenta tu ingesta calórica de forma saludable.'
    elif imc < 25:
        clasificacion = 'Peso normal'
        recomendacion = 'Mantén tu peso actual con hábitos saludables.'
    elif imc < 30:
        clasificacion = 'Sobrepeso'
        recomendacion = 'Considera aumentar actividad física y revisar tu dieta.'
    else:
        clasificacion = 'Obesidad'
        recomendacion = 'Consulta a un profesional de salud.'
    
    if genero == 'masculino':
        tmb = 88.362 + (13.397 * peso) + (4.799 * (altura * 100)) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * (altura * 100)) - (4.330 * edad)
    
    tmb = round(tmb, 2)
    calorias = round(tmb * 1.55, 2)
    
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
        'calorias': calorias
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
        calorias=calorias
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login con correo y contraseña."""
    if request.method == 'GET':
        return render_template('login.html')
    
    correo = request.form.get('correo', '').strip()
    contraseña = request.form.get('contraseña', '')
    user = session.get('user')
    
    if not user:
        flash('Primero debes completar el formulario.')
        return redirect(url_for('formulario'))
    
    if correo == user.get('correo_electronico') and contraseña == user.get('contraseña'):
        session['authenticated'] = True
        return redirect(url_for('rutina'))
    
    flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/rutina')
def rutina():
    """Muestra rutina personalizada con detalle, dieta y enlaces a recetas."""
    user = session.get('user')
    if not user:
        flash('Debes completar el formulario primero.')
        return redirect(url_for('formulario'))

    clas = user.get('clasificacion', '').lower()
    if 'bajo' in clas:
        rutina_detalle = {
            'descripcion': 'Enfocado en ganancia muscular y aumento calórico',
            'plan_semanal': [
                {'dia': 'Lunes', 'actividad': 'Fuerza — Tren superior (4 ejercicios, 3x8-12)'},
                {'dia': 'Martes', 'actividad': 'Cardio ligero 20-30 min'},
                {'dia': 'Miércoles', 'actividad': 'Fuerza — Tren inferior (4 ejercicios, 3x8-12)'},
                {'dia': 'Jueves', 'actividad': 'Descanso activo: caminata 30 min'},
                {'dia': 'Viernes', 'actividad': 'Fuerza — Full body (3 series por ejercicio)'},
                {'dia': 'Sábado', 'actividad': 'Cardio ligero o actividad recreativa'},
                {'dia': 'Domingo', 'actividad': 'Descanso completo'}
            ],
            'dieta': {
                'objetivo': 'Superávit calórico moderado (+300-500 kcal)',
                'ejemplo': {
                    'desayuno': 'Avena con leche, plátano y frutos secos (ver receta 1)',
                    'media_mañana': 'Yogur griego con miel',
                    'almuerzo': 'Quinoa con pollo y verduras (ver receta 2)',
                    'merienda': 'Batido proteico con fruta',
                    'cena': 'Pescado o pollo con verduras y patata'
                }
            }
        }
    elif 'normal' in clas:
        rutina_detalle = {
            'descripcion': 'Mantener condición y composición corporal',
            'plan_semanal': [
                {'dia': 'Lunes', 'actividad': 'Fuerza — Full body (3x8-12)'},
                {'dia': 'Martes', 'actividad': 'Cardio moderado 30-40 min'},
                {'dia': 'Miércoles', 'activity': 'Movilidad y core'},
                {'dia': 'Jueves', 'actividad': 'Fuerza — Enfoque en técnica'},
                {'dia': 'Viernes', 'actividad': 'Cardio intervalado 20-30 min'},
                {'dia': 'Sábado', 'actividad': 'Actividad recreativa'},
                {'dia': 'Domingo', 'actividad': 'Descanso activo'}
            ],
            'dieta': {
                'objetivo': 'Mantener calorías de mantenimiento',
                'ejemplo': {
                    'desayuno': 'Tostadas integrales con aguacate y huevo',
                    'almuerzo': 'Quinoa con pollo (ver receta 2)',
                    'cena': 'Salmón al horno con vegetales (ver receta 3)'
                }
            }
        }
    else:
        rutina_detalle = {
            'descripcion': 'Reducir grasa corporal con déficit moderado y actividad cardiovascular',
            'plan_semanal': [
                {'dia': 'Lunes', 'actividad': 'Cardio 30-40 min + core'},
                {'dia': 'Martes', 'actividad': 'Fuerza — Enfoque en grandes grupos musculares (3x8-12)'},
                {'dia': 'Miércoles', 'actividad': 'HIIT 20-25 min'},
                {'dia': 'Jueves', 'actividad': 'Fuerza — Técnica y movilidad'},
                {'dia': 'Viernes', 'actividad': 'Cardio moderado 40 min'},
                {'dia': 'Sábado', 'actividad': 'Actividad recreativa ligera'},
                {'dia': 'Domingo', 'actividad': 'Descanso'}
            ],
            'dieta': {
                'objetivo': 'Déficit calórico moderado (-300-600 kcal), alta proteína',
                'ejemplo': {
'desayuno': 'Omelette con verduras',
                    'almuerzo': 'Ensalada grande con proteína magra (pollo o pescado)',
                    'cena': 'Verduras asadas con porción de quinoa'
                }
            }
        }

    return render_template('rutina.html', user=user, rutina=rutina_detalle)

@app.route('/perfil')
def perfil():
    """Muestra perfil del usuario."""
    user = session.get('user')
    if not user:
        flash('Debes completar el formulario primero.')
        return redirect(url_for('formulario'))
    
    return render_template('perfil.html', user=user)

@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    """Calculadora de TMB."""
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0))
            edad = int(request.form.get('edad', 0))
            genero = request.form.get('genero', 'masculino').lower()
            
            if genero == 'masculino':
                tmb_calc = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
            else:
                tmb_calc = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
            
            tmb_calc = round(tmb_calc, 2)
            return render_template('tmb.html', tmb=tmb_calc, peso=peso, altura=altura, edad=edad, genero=genero)
        except (ValueError, TypeError):
            return render_template('tmb.html', error='Valores inválidos.')
    
    return render_template('tmb.html')

@app.route('/gct', methods=['GET', 'POST'])
def gct():
    """Calculadora de Gasto Calórico Total."""
    if request.method == 'POST':
        try:
            tmb_val = float(request.form.get('tmb', 0))
            actividad = float(request.form.get('actividad', 1.55))
            gct_calc = round(tmb_val * actividad, 2)
            return render_template('gct.html', gct=gct_calc, tmb=tmb_val, actividad=actividad)
        except (ValueError, TypeError):
            return render_template('gct.html', error='Valores inválidos.')
    
    return render_template('gct.html')

@app.route('/peso_ideal', methods=['GET', 'POST'])
def peso_ideal():
    """Calculadora de peso ideal (fórmula de Devine)."""
    if request.method == 'POST':
        try:
            altura_cm = float(request.form.get('altura', 0))
            genero = request.form.get('genero', 'masculino').lower()
            
            altura_m = altura_cm / 100
            if genero == 'masculino':
                ideal = 50 + (2.3 * (altura_cm - 152.4))
            else:
                ideal = 45.5 + (2.3 * (altura_cm - 152.4))
            
            ideal = round(ideal, 2)
            return render_template('peso_ideal.html', ideal=ideal, altura=altura_cm, genero=genero)
        except (ValueError, TypeError):
            return render_template('peso_ideal.html', error='Altura inválida.')
    
    return render_template('peso_ideal.html')

@app.route('/macros', methods=['GET', 'POST'])
def macros():
    """Calculadora de macronutrientes."""
    if request.method == 'POST':
        try:
            calorias = float(request.form.get('calorias', 0))
            p_pct = float(request.form.get('p', 30))
            c_pct = float(request.form.get('c', 40))
            g_pct = float(request.form.get('g', 30))
            
            prot = round((calorias * p_pct / 100) / 4, 2)
            carb = round((calorias * c_pct / 100) / 4, 2)
            fat = round((calorias * g_pct / 100) / 9, 2)
            
            macros_result = {'prot': prot, 'carb': carb, 'fat': fat}
            return render_template('macros.html', macros=macros_result, calorias=calorias, p=p_pct, c=c_pct, g=g_pct)
        except (ValueError, TypeError):
            return render_template('macros.html', error='Valores inválidos.')
    
    return render_template('macros.html')

@app.route('/clear')
def clear():
    """Borrar datos del usuario."""
    session.pop('user', None)
    session.pop('authenticated', None)
    flash('Datos borrados.')
    return redirect(url_for('formulario'))

@app.route('/logout')
def logout():
    """Cerrar sesión."""
    session.pop('authenticated', None)
    session.pop('user', None)
    flash('Sesión cerrada.')
    return redirect(url_for('inicio'))

@app.route('/recetas')
def recetas():
    """Lista de recetas disponibles."""
    return render_template('recetas.html', recetas=RECIPES)

@app.route('/recetas/<int:receta_id>')
def receta_detalle(receta_id):
    """Detalle de una receta."""
    receta = next((r for r in RECIPES if r['id'] == receta_id), None)
    if not receta:
        flash('Receta no encontrada.')
        return redirect(url_for('recetas'))
    return render_template('receta_detalle.html', receta=receta)
# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)