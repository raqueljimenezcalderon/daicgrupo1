from flask import Flask, render_template_string, request , render_template
import RPi.GPIO as GPIO    
from time import sleep
import datetime
import sys
# Configuracion de la app
app = Flask(__name__)
app.config['DEBUG'] = True

# Inicializacion de la app
'''if __name__ == "__main__":
    app.run()'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

video_muestra = "./static/Hola.mp4"
respuesta = "No hay mensajes"

#Configuracion de GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Pin del buzzer
buzz = 24

# Pines de los servos
servo_pin_0 = 16          
servo_pin_1 = 12

# leds (los digitos son los numeros donde estan conectados los pines)
led_0 = 5
led_1 = 18

# Inicializar pines botones
boton_0 = 26
boton_1 = 22

# Configurar pin buzzer
GPIO.setup(buzz, GPIO.OUT)

# Configurar pines Servos
GPIO.setup(servo_pin_0, GPIO.OUT)     
GPIO.setup(servo_pin_1, GPIO.OUT)

# Creacion de canales PWM en la frecuencia de 50Hz (En un principio no es necesario cambiar)
p_0 = GPIO.PWM(servo_pin_0, 50)
p_1 = GPIO.PWM(servo_pin_1, 50)

# Inicializar los servos en la posicion 0 -
p_0.start(0)
p_1.start(0)

# Configurar los pines de las Leds
GPIO.setup(led_0, GPIO.OUT)
GPIO.output(led_0, GPIO.LOW)
GPIO.setup(led_1, GPIO.OUT)
GPIO.output(led_1, GPIO.LOW)

# Configurar los pines de los botones
GPIO.setup(boton_0, GPIO.IN)
GPIO.setup(boton_1, GPIO.IN)


# Pagina inicial del buzz
@app.route('/buzz')
def home1():
    templateData = {
        'buzz' : buzz,
    }
    return render_template('buzzer.html', **templateData)


# Reaccion del buzz con los botones
@app.route('/<buzzer>/<action>')
def buzzer(buzzer, action):
    GPIO.output(int(buzzer), int(action))
    templateData = {
        'buzz' : GPIO.input(buzz), 
    }
    return render_template('buzzer.html', **templateData)


# Pagina inicial de los leds
@app.route('/leds')
def home3():
    templateData = {
        'led_0' : led_0,
        'led_1' : led_1,
    }
    return render_template('led.html', **templateData)


# Reaccion de los leds con los botones
@app.route('/<led>/<action>')
def led(led, action):
    GPIO.output(int(led), int(action))
    templateData = {
        'led_0' : GPIO.input(led_0),
        'led_1' : GPIO.input(led_1),
    }
    return render_template('led.html', **templateData)


# Url que redirige a los servos
@app.route("/motores")
def home2():
    return render_template('servo.html')


# Funcionamiento de los servos
@app.route("/test", methods=["POST"])
def test():
    # Recoge los valore de los sliders
    slider_0 = request.form["slider_0"]
    slider_1 = request.form["slider_1"]
    # Cambia el ciclo para que el motor se mueva
    p_0.ChangeDutyCycle(float(slider_0))
    p_1.ChangeDutyCycle(float(slider_1))
    # Espera a que se mueva
    print(slider_0)
    print(slider_1)
    sleep(1)
    # Para el servo
    p_0.ChangeDutyCycle(0)
    p_1.ChangeDutyCycle(0)
    return render_template('servo.html')


# Inicializa la ventana de los botones
@app.route("/botones")
def hello():
    respuestas()
    if GPIO.input(boton_0):
        doorStatus = "open"
    else:
        doorStatus = "closed"
    templateData = {
        'doorStatus': doorStatus,
    }
    print(doorStatus)
    return render_template('boton.html', **templateData)


# Funcionamiento de los leds
@app.route('/ledLevel/<level>')
def pin_state(level):
    # PWM.set_duty_cycle("P8_11", float(level))
    return "LED level set to " + "."


@app.route("/")
def home():
    respuestas()
    return render_template('inicio.html')


@app.route("/saludo")
def saludo():
    respuestas()
    # Cambio web
    respuesta = "Saludando"
    # Movimientos en bot
    p_0.ChangeDutyCycle(5)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    sleep(1)
    GPIO.output(led_1, 0)
    p_0.ChangeDutyCycle(7.5)
    sleep(1)
    GPIO.output(led_0, 0)
    p_0.ChangeDutyCycle(0)
    p_1.ChangeDutyCycle(0)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.3)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.3)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    # Cambiar cara
    global video_muestra
    video_muestra = "./static/Hola.mp4"
    # Actualizar web
    return render_template('inicio.html', respuesta=respuesta, title="inicio")


@app.route("/triste")
def triste():
    respuestas()
    # Cambio web
    respuesta = "Triste"
    # Movimientos en bot
    p_0.ChangeDutyCycle(10)
    p_1.ChangeDutyCycle(10)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    sleep(1)
    GPIO.output(led_1, 0)
    p_0.ChangeDutyCycle(7.5)
    p_1.ChangeDutyCycle(7.5)
    sleep(1)
    GPIO.output(led_0, 0)
    p_0.ChangeDutyCycle(0)
    p_1.ChangeDutyCycle(0)
    GPIO.output(buzz, 1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.4)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.4)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.4)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    # Cambiar cara
    global video_muestra
    video_muestra = "./static/Triste.mp4"
    # Actualizar web
    return render_template('inicio.html', respuesta=respuesta, title="inicio")


@app.route("/agitarBrazos")
def agitarBrazos():
    respuestas()
    # Cambio web
    respuesta = "Agitando Brazos"
    # Movimientos en bot
    p_0.ChangeDutyCycle(10)
    p_1.ChangeDutyCycle(10)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    sleep(1)
    p_0.ChangeDutyCycle(5)
    p_1.ChangeDutyCycle(5)
    sleep(1)
    p_0.ChangeDutyCycle(10)
    p_1.ChangeDutyCycle(10)
    sleep(1)
    p_0.ChangeDutyCycle(5)
    p_1.ChangeDutyCycle(5)
    sleep(1)
    p_0.ChangeDutyCycle(7.5)
    p_1.ChangeDutyCycle(7.5)
    sleep(1)
    GPIO.output(led_0, 0)
    p_0.ChangeDutyCycle(0)
    p_1.ChangeDutyCycle(0)
    GPIO.output(buzz, 1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    sleep(0.4)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.2)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.4)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 1)
    GPIO.output(buzz, 0)
    sleep(0.1)
    GPIO.output(led_0, 1)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 1)
    sleep(0.1)
    GPIO.output(led_0, 0)
    GPIO.output(led_1, 0)
    GPIO.output(buzz, 0)
    # Cambiar cara
    global video_muestra
    video_muestra = "./static/Saludo.mp4"
    # Actualizar web
    return render_template('inicio.html', respuesta=respuesta, title="inicio")

@app.route("/pickles")
def pickles():
    respuestas()
    video = video_muestra
    return render_template("pickles.html", title="pickles", video=video)


def respuestas():
    global respuesta
    if GPIO.input(boton_0):
        respuesta = "Hola"
    elif GPIO.input(boton_1):
        respuesta = "Estoy bien"
    elif GPIO.input(boton_1) and GPIO.input(boton_0):
        respuesta = "Que tal?"
    print(respuesta)

@app.route("/reacciones")
def reacciones():
    respuestas()
    global respuesta
    templateData = {
        'respuesta': respuesta,
    }
    return render_template("reacciones.html", title="reacciones", **templateData)