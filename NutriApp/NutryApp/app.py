# ...existing code...
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'cambia_esto_en_produccion'

# ...existing code...

API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "tN2XZsdySpg5RvS75AJNOLrDHJPbny4W64vfX3N"

# ...existing code...

@app.route('/nutrientes', methods=['GET', 'POST'])
def nutrientes():
    """Busca alimentos en la base de datos USDA y muestra nutrientes.
    Soporta búsqueda en español."""
    alimento = None
    alimentos = None
    error = None

    if request.method == 'POST':
        alimento = request.form.get('alimento', '').strip()
        
        if not alimento:
            error = 'Por favor ingresa el nombre de un alimento.'
        elif len(alimento) < 2:
            error = 'El término debe tener al menos 2 caracteres.'
        else:
            try:
                params = {
                    'query': alimento,
                    'api_key': API_KEY,
                    'pageSize': 10
                }
                
                response = requests.get(API_URL, params=params, timeout=10)
                
                if response.status_code == 200:
                    datos = response.json()
                    foods = datos.get('foods', [])
                    
                    if not foods:
                        error = f'No se encontraron alimentos para "{alimento}". Intenta con otro término.'
                    else:
                        # ...existing code...
                        alimentos = []
                        for food in foods:
                            # Filtrar nutrientes principales
                            nutrients = []
                            nutrient_map = {
                                'Energy': ('Energía', 'kcal'),
                                'Protein': ('Proteína', 'g'),
                                'Total lipid (fat)': ('Grasa total', 'g'),
                                'Carbohydrate, by difference': ('Carbohidratos', 'g'),
                                'Fiber, total dietary': ('Fibra', 'g'),
                                'Sugars, total': ('Azúcares', 'g'),
                                'Calcium, Ca': ('Calcio', 'mg'),
                                'Iron, Fe': ('Hierro', 'mg'),
                                'Potassium, K': ('Potasio', 'mg'),
                                'Sodium, Na': ('Sodio', 'mg'),
                                'Vitamin A, RAE': ('Vitamina A', 'mcg'),
                                'Vitamin C, total ascorbic acid': ('Vitamina C', 'mg'),
                                'Vitamin D (D2 + D3)': ('Vitamina D', 'mcg'),
                                'Folate, total': ('Folato', 'mcg'),
                                'Zinc, Zn': ('Zinc', 'mg')
                            }
                            
                            for nut in food.get('foodNutrients', []):
                                nut_name = nut.get('nutrientName', '')
                                for eng_name, (es_name, unit) in nutrient_map.items():
                                    if eng_name.lower() in nut_name.lower():
                                        value = round(nut.get('value', 0), 2)
                                        nutrients.append({
                                            'name': es_name,
                                            'value': value,
                                            'unitName': unit
                                        })
                                        break
                            # Tomar todos los nutrientes que devuelve la API y mostrarlos tal cual
                            nutrients = []
                            for nut in food.get('foodNutrients', []):
                                name = nut.get('nutrientName') or nut.get('name') or 'Desconocido'
                                unit = nut.get('unitName') or nut.get('unit') or ''
                                raw_value = nut.get('value')
                                if raw_value is None:
                                    continue
                                try:
                                    value = round(float(raw_value), 2)
                                except (ValueError, TypeError):
                                    value = raw_value
                                nutrients.append({
                                    'name': name,
                                    'value': value,
                                    'unitName': unit
                                })
                            # Opcional: ordenar por nombre para mejor lectura
                            nutrients = sorted(nutrients, key=lambda x: x['name'])
                            
                            alimentos.append({
                                'description': food.get('description', 'Sin descripción'),
                                'foodCategory': food.get('foodCategory', 'Categoría desconocida'),
                                'nutrients': nutrients
                            })
# ...existing code...                     
                
                elif response.status_code == 401:
                    error = 'Error de autenticación con la API. Por favor intenta más tarde.'
                elif response.status_code == 429:
                    error = 'Límite de solicitudes alcanzado. Intenta de nuevo en unos minutos.'
                else:
                    error = f'Error en la solicitud (código {response.status_code}). Intenta de nuevo.'
                    
            except requests.exceptions.Timeout:
                error = 'La solicitud tardó demasiado. Intenta de nuevo.'
            except requests.exceptions.ConnectionError:
                error = 'Error de conexión. Verifica tu conexión a internet.'
            except Exception as e:
                error = f'Ocurrió un error inesperado: {str(e)}'

    return render_template('nutrientes.html', alimento=alimento, alimentos=alimentos, error=error)

# ...existing code...


def _get_first(form, *keys, default=''):
    """Retorna el primer valor no vacío del formulario."""
    for k in keys:
        v = form.get(k)
        if v is not None and v != '':
            return v
    return default

# ...existing code...
# --- NUEVO: datos de recetas simples para la sección de recetas (ampliado) ---
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
    },
    {
        'id': 4,
        'title': 'Tostadas integrales con aguacate y huevo',
        'description': 'Desayuno rico en grasas saludables y proteína.',
        'ingredients': [
            '2 rebanadas pan integral',
            '1/2 aguacate',
            '2 huevos',
            'Sal y pimienta'
        ],
        'steps': [
            'Tostar el pan, aplastar el aguacate sobre las tostadas.',
            'Hacer huevos a la plancha o escalfados y colocar encima.'
        ]
    },
    {
        'id': 5,
        'title': 'Batido proteico de frutos rojos',
        'description': 'Merienda rápida para recuperación muscular.',
        'ingredients': [
            '1 scoop proteína',
            '150 g frutos rojos congelados',
            '250 ml leche o bebida vegetal',
            '1 cucharada avena'
        ],
        'steps': [
            'Batir todos los ingredientes hasta obtener textura homogénea.',
            'Consumir después del entrenamiento.'
        ]
    },
    {
        'id': 6,
        'title': 'Salteado de garbanzos y espinacas',
        'description': 'Plato vegetariano alto en fibra y proteína vegetal.',
        'ingredients': [
            '200 g garbanzos cocidos',
            '100 g espinacas',
            'Ajo, cebolla, pimentón',
            'Aceite de oliva'
        ],
        'steps': [
            'Saltear ajo y cebolla, añadir garbanzos y especias.',
            'Agregar espinacas al final y cocinar 2 minutos.'
        ]
    }
]
# ...existing code...

@app.route('/rutina')
def rutina():
    """Muestra rutina personalizada con detalle, dieta y enlaces a recetas.
    Ahora usa género, peso, altura, edad e IMC para decidir objetivo y macros."""
    user = session.get('user')
    if not user:
        flash('Debes completar el formulario primero.')
        return redirect(url_for('formulario'))

    # Extraer datos
    peso = float(user.get('peso', 0))
    altura_m = float(user.get('altura', 0))
    altura_cm = altura_m * 100
    edad = int(user.get('edad', 0))
    genero = user.get('genero', 'masculino').lower()
    imc = float(user.get('imc', 0))
    # Recalcular TMB (Harris-Benedict) para precisión local
    if genero == 'masculino':
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)
    tmb = round(tmb, 2)

    # Decidir objetivo según IMC
    if imc < 18.5:
        objetivo = 'ganar'      # aumento de masa
        delta_cal = 400
        prot_per_kg = 1.8
    elif imc < 25:
        objetivo = 'mantener'   # mantenimiento
        delta_cal = 0
        prot_per_kg = 1.6
    else:
        objetivo = 'perder'     # pérdida de grasa
        delta_cal = -500
        prot_per_kg = 2.0

    # Estimar calorías de mantenimiento actuales (si el formulario ya calculó, úsalo)
    mantenimiento = user.get('calorias') or round(tmb * 1.55, 2)
    calorias_obj = max(1200, round(mantenimiento + delta_cal, 0))  # limitar mínimo seguro

    # Macros: proteína en g por kg, grasas 25% calorías, resto carbohidratos
    prot_g = round(prot_per_kg * peso, 1)
    prot_kcal = prot_g * 4
    fat_kcal = round(calorias_obj * 0.25, 0)
    fat_g = round(fat_kcal / 9, 1)
    carb_kcal = round(calorias_obj - (prot_kcal + fat_kcal), 0)
    carb_g = round(carb_kcal / 4, 1)

    # Rutina semanal adaptada por género y objetivo
    if genero == 'masculino':
        fuerza_focus = 'Fuerza con énfasis en hipertrofia y progresión de cargas'
        cardio_focus = 'Cardio moderado/intervalado'
        plan = [
            {'dia': 'Lunes', 'actividad': 'Fuerza — Pecho/Tríceps (4 ejercicios, 3-4x8-12)'},
            {'dia': 'Martes', 'actividad': 'Cardio: Intervalos 20-25 min'},
            {'dia': 'Miércoles', 'actividad': 'Fuerza — Espalda/Bíceps (4 ejercicios, 3-4x8-12)'},
            {'dia': 'Jueves', 'actividad': 'Piernas y core (4 ejercicios, 3x8-12)'},
            {'dia': 'Viernes', 'actividad': 'Full body ligero + movilidad'},
            {'dia': 'Sábado', 'actividad': 'Actividad recreativa o cardio suave'},
            {'dia': 'Domingo', 'actividad': 'Descanso activo'}
        ]
    else:
        fuerza_focus = 'Entrenamiento de resistencia funcional y tonificación'
        cardio_focus = 'Cardio moderado y trabajo de movilidad'
        plan = [
            {'dia': 'Lunes', 'actividad': 'Fuerza — Tren inferior + glúteos (4x8-12)'},
            {'dia': 'Martes', 'actividad': 'Cardio moderado 30 min + movilidad'},
            {'dia': 'Miércoles', 'activity': 'Fuerza — Tren superior (3-4 ejercicios)'},
            {'dia': 'Jueves', 'actividad': 'Pilates / Core y movilidad'},
            {'dia': 'Viernes', 'actividad': 'Circuito full body (condición + fuerza)'},
            {'dia': 'Sábado', 'actividad': 'Actividad recreativa ligera'},
            {'dia': 'Domingo', 'actividad': 'Descanso activo'}
        ]

    # Dieta de ejemplo con macros calculadas
    dieta = {
        'objetivo': {
            'ganar': 'Superávit calórico moderado (+300-500 kcal)',
            'mantener': 'Calorías de mantenimiento',
            'perder': 'Déficit moderado (-300-600 kcal)'
        }[objetivo],
        'calorias_objetivo': calorias_obj,
        'macros': {
            'proteina_g': prot_g,
            'carbohidratos_g': carb_g,
            'grasas_g': fat_g
        },
        'ejemplo': {
            'desayuno': 'Avena con leche, fruta y proteína (ver receta 1 o 4)',
            'almuerzo': 'Fuente de proteína + carbohidrato complejo + vegetales (receta 2 o 3)',
            'merienda': 'Batido proteico o yogur con frutos secos (receta 5)',
            'cena': 'Pescado/Pollo/Legumbres con verduras (receta 3 o 6)'
        }
    }

    rutina_detalle = {
        'descripcion': f'{fuerza_focus} — objetivo: {objetivo} — TMB estimado: {tmb} kcal/día',
        'plan_semanal': plan,
        'dieta': dieta
    }

    return render_template('rutina.html', user=user, rutina=rutina_detalle)
# ...existing code...
@app.route('/')
def inicio():
    """Página de inicio con información."""
    return render_template('info.html')

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
    
    # Calcular IMC
    imc = round(peso / (altura ** 2), 2)
    
    # Clasificar IMC
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
    
    # Calcular TMB (Harris-Benedict)
    if genero == 'masculino':
        tmb = 88.362 + (13.397 * peso) + (4.799 * (altura * 100)) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * (altura * 100)) - (4.330 * edad)
    
    tmb = round(tmb, 2)
    calorias = round(tmb * 1.55, 2)
    
    # Guardar en sesión
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