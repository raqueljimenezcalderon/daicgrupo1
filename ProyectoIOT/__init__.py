from flask import Flask, render_template_string, request , render_template
import RPi.GPIO as GPIO    
from time import sleep
import datetime

app = Flask(__name__)

# Enable debug mode
app.config['DEBUG'] = True
if __name__ == "__main__":
    app.run()
'''if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=True) '''

#Configuracion de GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# leds (los digitos son los numeros donde estan conectados los pines)
led_0 = 5
led_1 = 18
GPIO.setup(led_0, GPIO.OUT)
GPIO.output(led_0, GPIO.LOW)
GPIO.setup(led_1, GPIO.OUT)
GPIO.output(led_1, GPIO.LOW)

#Pagina inicial de los leds
@app.route('/leds')
def home():
   templateData = {
      'led_0' : 5,
      'led_1' : 0,
   }
   return render_template('led.html', **templateData)

#Reaccion de los leds con los botones
@app.route('/<led>/<action>')
def led(led, action):
   GPIO.output(int(led), int(action))
   templateData = {
      'led_0' : GPIO.input(led_0),
      'led_1' : GPIO.input(led_1),
   }
   return render_template('led.html', **templateData)


   
   
# Pines de los servos
servo_pin = 16          
servo_pin1 = 19
 
GPIO.setmode(GPIO.BCM)
# We are using the BCM pin numbering
# Declaring Servo Pins as output pins
GPIO.setup(servo_pin, GPIO.OUT)     
GPIO.setup(servo_pin1, GPIO.OUT)
 
# Created PWM channels at 50Hz frequency
p = GPIO.PWM(servo_pin, 50)
p1 = GPIO.PWM(servo_pin1, 50)
 
# Initial duty cycle
p.start(0)
p1.start(0) 
# Store HTML code

# which URL should call the associated function.
@app.route("/pr")
def home2():
    return render_template('servo.html')
 
@app.route("/test", methods=["POST"])
def test():
    # Get slider Values
    slider1 = request.form["slider1"]
    slider2 = request.form["slider2"]
    # Change duty cycle
    p.ChangeDutyCycle(float(slider1))
    p1.ChangeDutyCycle(float(slider2))
    # Give servo some time to move
    sleep(1)
    # Pause the servo
    p.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(0)
    return render_template('servo.html')

GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.IN)
# PWM.start("P8_11", 0.0)

@app.route("/")
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

@app.route('/ledLevel/<level>')
def pin_state(level):
    # PWM.set_duty_cycle("P8_11", float(level))
    return "LED level set to " + "."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 
