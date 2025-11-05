Nombre de la escuela  
Materia: Emplea Framwork para el desarrollo de software.
Actividad: Investigación de APIs Nutricionales.
Alumno: Jared Olmeda y Angel Frías.
Docente: Juan Rubén Treviño Tapia.
Fecha: 25/sep/2025

1. Tabla comparativa de APIs nutricionales
| API               | Tipo de datos                                               | Costo / Plan gratuito          | Límites de uso                     | Facilidad de implementación | Calidad de documentación          |
|-------------------|-------------------------------------------------------------|--------------------------------|------------------------------------|-----------------------------|----------------------------------|  
| Nutritionix       | Alimentos de marca, restaurantes, datos nutricionales, entrada en lenguaje natural | Plan gratuito limitado         | Restricción en número de peticiones y usuarios activos | Fácil, REST estándar        | Buena, con ejemplos claros       |
| Edamam           | Análisis nutricional de recetas/ingredientes, búsqueda de alimentos, etiquetas dietas/alergias | Desde $29/mes (sin plan gratis) | Límite de peticiones según plan    | Fácil de usar con SDKs y ejemplos | Muy completa, con guías y ejemplos |
| USDA FoodData Central | Base de datos pública con composición nutricional de alimentos genéricos y de marca | Gratis (pública)               | 1,000 requests/hora/IP            | Muy sencilla (REST, JSON)   | Excelente, con OpenAPI y ejemplos |
| Spoonacular      | Datos de recetas, cálculo nutricional, búsqueda de menús y productos | Plan gratuito (~3,000 requests/mes) | Límite en plan gratuito           | Buena, endpoints variados      | Clara, con SDKs y Postman       |
2. API seleccionada y justificación
He elegido USDA FoodData Central API porque:
• Es gratuita y no tiene costos ocultos.
• Ofrece datos confiables, actualizados y públicos.
• Tiene documentación muy clara y fácil de seguir.
• Permite probar rápidamente con herramientas como Postman o curl.
• Es ideal para fines académicos y proyectos de aprendizaje.
3. Registro y obtención de API Key
1. Ingresé a la página oficial de la API: https://fdc.nal.usda.gov/api-guide
2. Solicité una clave API gratuita proporcionando mi correo electrónico.
3. Recibí la API key en mi correo (se usa en cada solicitud con el parámetro api_key).
Ejemplo de uso en consulta:
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=TU_API_KEY"
```
4. Ejemplos de solicitudes y respuestas
🔎 Búsqueda de alimentos
Solicitud (curl):
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=banana&api_key=TU_API_KEY"
```
Respuesta JSON simplificada:
```json
{
  "foods": [
    {
      "fdcId": 110265,
      "description": "Banana, raw",
      "foodNutrients": [
        { "nutrientName": "Protein", "value": 1.09, "unitName": "G" },
        { "nutrientName": "Fat", "value": 0.33, "unitName": "G" },
        { "nutrientName": "Carbohydrate", "value": 22.84, "unitName": "G" },
        { "nutrientName": "Energy", "value": 89, "unitName": "KCAL" }
      ]
    }
  ]
}
```
📊 Detalle de alimento por ID
Solicitud:
```bash
curl "https://api.nal.usda.gov/fdc/v1/food/110265?api_key=TU_API_KEY"
```
Respuesta JSON simplificada:
```json
{
  "fdcId": 110265,
  "description": "Banana, raw",
  "foodNutrients": [
    { "nutrientName": "Protein", "value": 1.09, "unitName": "G" },
    { "nutrientName": "Fat", "value": 0.33, "unitName": "G" },
    { "nutrientName": "Carbohydrate", "value": 22.84, "unitName": "G" },
    { "nutrientName": "Energy", "value": 89, "unitName": "KCAL" }
  ]
}
```
5. Dificultades encontradas y soluciones
| Dificultad               | Causa                          | Solución                                 |
|--------------------------|--------------------------------|------------------------------------------|
| Clave API no funcionaba  | Error al copiar/pegar          | Revisar espacios y parámetro api_key      |
| Exceso de peticiones     | Superar límite 1000/hora       | Esperar 1h o cachear resultados            |
| Alimentos no encontrados | Nombre distinto en DB          | Probar términos genéricos/sinónimos         |
| Demasiados resultados    | Muchos alimentos coinciden     | Usar paginación pageNumber/pageSize            |