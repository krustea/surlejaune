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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup des leds
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
# setup du buzzer
GPIO.setup(22, GPIO.OUT)


@app.route("/")
def index():
    return render_template('index.html')


def message_loop():
    while True:
        Celsius = degcel.degreeCelsius()
        if Celsius < 15:
            GPIO.output(24, GPIO.HIGH)
            message = ("la temperature est de : " + str(Celsius) + ", declenchement des radiateurs")
            socketio.emit('alert', message, Broadcast=True)
        elif Celsius > 30:
            GPIO.output(18, GPIO.HIGH)
            message2 = ("la temperature est de : " + str(Celsius) + ", declenchement de la climatisation")
            socketio.emit('alert', message2, Broadcast=True)

        elif Celsius > 40:
            GPIO.output(22, GPIO.HIGH)
            message4 = ("la temperature est de : " +str(Celsius) + ", Alerte, il fait beaucoup trop chaud")
            socketio.emit('alert', message4, Broadcast=True)

        else:
            GPIO.output(18, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            message3 = ("la temperature est de : " + str(Celsius) + ". Il fait bon")
            socketio.emit('alert', message3, Broadcast=True)

        # On attends 10ms
        time.sleep(30)



# Vue que notre méthode pour lire nos message est une boucle infinie
# Elle bloquerait notre serveur. Qui ne pourrait répondre à aucune requête.
# Ici nous créons un Thread qui va permettre à notre fonction de se lancer
# en parallèle du serveur.
read_messages = threading.Thread(target=message_loop)
read_messages.start()
