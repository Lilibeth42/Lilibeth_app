from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        api_key = "4cd9ee62b93443a4a9d008cae4058eab"  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            # Procesamos los datos para ajustarlos
            latitud = datos['coord']['lat']
            longitud = datos['coord']['lon']
            weather_data = {
                'ciudad': datos['name'],
                'temperatura': round(datos['main']['temp'], 1),  # Redondeamos la temperatura
                'descripcion': datos['weather'][0]['description'].capitalize(),  # En español
                'latitud': f"{abs(latitud)}° {'Norte' if latitud >= 0 else 'Sur'}",
                'longitud': f"{abs(longitud)}° {'Este' if longitud >= 0 else 'Oeste'}",
                'icono': datos['weather'][0]['icon']
            }
        else:
            weather_data = {'error': 'No se encontró información para la ciudad ingresada.'}
    return render_template('index.html', weather_data=weather_data)

@app.route('/cv.html')
def cv():
    return render_template('cv.html')

if __name__ == '__main__':
    app.run(debug=True)
