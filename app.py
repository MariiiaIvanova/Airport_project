from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Получаем данные из формы
    s_use = float(request.form.get('s_use'))
    min_flights_pass = int(request.form.get('min_flights_pass'))
    price_kvatt_per_hour = float(request.form.get('price_kvatt_per_hour'))
    
    # Выполняем расчеты
    result_value = perform_calculation(s_use, min_flights_pass, price_kvatt_per_hour)
    
    # Определяем, какое сообщение нужно вывести
    if result_value > 0:
        message = "На объект целесообразно установить пьезоплитку. Выгода составит: "
    else:
        message = "Плата за электроэнергию с установлением пьезоплитки увеличится на: "
    
    return render_template('result.html', message=message, result=round(abs(result_value), 2))

def perform_calculation(s_use, min_flights_pass, price_kvatt_per_hour):

    s_pulkovo = 13.5

    k = s_use/s_pulkovo

    max_value = 614.748*k
    mean_value = 407.965*k

    number_of_tiles = 100;
    percent = 0.1;
    air_vatt_per_day = (5*min_flights_pass*number_of_tiles*30*percent)/1000000

    found_number_of_tiles = 100
    for number_of_tiles in range(1, 101):
        air_vatt_per_day = (5 * min_flights_pass * number_of_tiles*percent * 30) / 1000000
        if (air_vatt_per_day >= (110 / 100) * max_value):
            found_number_of_tiles = number_of_tiles
            break

    air_vatt_per_day_best = (5*min_flights_pass*found_number_of_tiles*percent*30)/1000000

    max_value_guarantee = 20000000
    price_per_one = 7000
    frequency_reset = (max_value_guarantee/(min_flights_pass*percent))

    prise_with_tiles = price_per_one*found_number_of_tiles*360/frequency_reset

    price_kvatt_per_hour = price_kvatt_per_hour*0.001

    price_without_tiles = price_kvatt_per_hour*24*365*mean_value*12*k

    delta = price_without_tiles-prise_with_tiles
    
    return delta


if __name__ == '__main__':
    app.run(debug=True)
