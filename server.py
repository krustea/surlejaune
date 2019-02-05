from flask import Flask
from temperature import TemperatureSensor
from flask_socketio import SocketIO, send, emit
from flask import render_template
import time
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)
degcel = TemperatureSensor()
socketio = SocketIO(app)
broche = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup des leds
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
# setup du buzzer
GPIO.setup(22, GPIO.OUT)

GPIO.setup(broche, GPIO.IN)


@app.route("/")
def index():
    return render_template('index.html')


def message_loop():
    currentstate = 0
    previousstate = 0
    while True:

        # Lecture du capteur
        currentstate = GPIO.input(broche)
        # Si le capteur est déclenché
        #        print("current state:"+ str(currentstate))
        if currentstate == 1 and previousstate == 0:
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            Celsius = degcel.degreeCelsius()
            message = ("la temperature est de : " + str(Celsius))
            socketio.emit('alert', message, Broadcast=True)
            previousstate = 1
            print("mouvement")
        # Si le capteur est s'est stabilisé
        elif currentstate == 0 and previousstate == 1:
            GPIO.output(18, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            previousstate = 0
        # On attends 10ms
        time.sleep(0.01)


# Vue que notre méthode pour lire nos message est une boucle infinie
# Elle bloquerait notre serveur. Qui ne pourrait répondre à aucune requête.
# Ici nous créons un Thread qui va permettre à notre fonction de se lancer
# en parallèle du serveur.
read_messages = threading.Thread(target=message_loop)
read_messages.start()
