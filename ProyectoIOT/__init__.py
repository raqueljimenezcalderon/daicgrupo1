from flask import Flask, render_template_string, request , render_template
import RPi.GPIO as GPIO    
from time import sleep
import datetime


app = Flask(__name__)


# Enable debug mode
app.config['DEBUG'] = True
'''if __name__ == "__main__":
    app.run()'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

#Configuracion de GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pines de los servos
servo_pin = 16          
servo_pin1 = 19

# Configurar pines Servos
GPIO.setup(servo_pin, GPIO.OUT)     
GPIO.setup(servo_pin1, GPIO.OUT)

# Creacion de canales PWM en la frecuencia de 50Hz (En un principio no es necesario cambiar)
p = GPIO.PWM(servo_pin, 50)
p1 = GPIO.PWM(servo_pin1, 50)

# Inicializar los servos en la posicion 0 -
p.start(0)
p1.start(0) 

# leds (los digitos son los numeros donde estan conectados los pines)
led_0 = 5
led_1 = 18

# Configurar los pines de las Leds
GPIO.setup(led_0, GPIO.OUT)
GPIO.output(led_0, GPIO.LOW)
GPIO.setup(led_1, GPIO.OUT)
GPIO.output(led_1, GPIO.LOW)

# Inicializar pines botones
boton_0 = 18
boton_1 = 22

# Configurar los pines de los botones
GPIO.setup(boton_0, GPIO.IN)
GPIO.setup(boton_1, GPIO.IN)


#Pagina inicial de los leds
@app.route('/leds')
def home():
    templateData = {
        'led_0' : 5,
        'led_1' : 18,
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
    slider1 = request.form["slider1"]
    slider2 = request.form["slider2"]
    # Cambia el ciclo para que el motor se mueva
    p.ChangeDutyCycle(float(slider1))
    p1.ChangeDutyCycle(float(slider2))
    # Espera a que se mueva
    sleep(1)
    # Para el servo
    p.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(0)
    return render_template('servo.html')


# Inicializa la ventana de los botones
@app.route("/botones")
def hello():
    if GPIO.input(22):
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

