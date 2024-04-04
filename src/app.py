# app.py
from flask import Flask, render_template, jsonify, request
from tinydb import TinyDB, Query
from pydobot import Dobot
from serial.tools import list_ports
import time
import pydobot
import inquirer

# port="COM4"
app = Flask(__name__)
db = TinyDB('database.json')
# robo = pydobot.Dobot(port=port, verbose=False)
robo = None
def conectar():
    available_ports = list_ports.comports()

    porta_escolhida = inquirer.prompt([inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])])["porta"]

    print('Porta escolhida:', porta_escolhida)

    global robo 
    robo = pydobot.Dobot(port=porta_escolhida, verbose=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move_robot', methods=['POST'])
def move_robot():
    # if request.method == 'POST':
        if not robo:
            conectar()
        command = request.form['command']
        movimento(command)
        # Simulando movimento do robô
        time.sleep(2)
        db.insert({'command': command, 'timestamp': time.time()})
        time.sleep(2)
    # else:
    #  return (get_commands())
        
@app.route('/get_commands', methods=['GET'])
def get_commands():
    commands = db.all()
    return jsonify(commands)


def movimento(command):
    if command == "+10 em x":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= 10
        robo.move_to(x + deslocamento, y, z, r, wait=True) 
        robo.close()
    elif command == "-10 em x":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= -10
        robo.move_to(x + deslocamento, y, z, r, wait=True) 
        robo.close()
    elif command == "+10 em y":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= 10
        robo.move_to(x, y + deslocamento, z, r, wait=True) 
        robo.close()
    elif command == "-10 em y":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= -10
        robo.move_to(x, y + deslocamento, z, r, wait=True) 
        robo.close()
    elif command == "+10 em z":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= 10
        robo.move_to(x, y, z + deslocamento, r, wait=True) 
        robo.close()
    elif command == "-10 em z":
        (x, y, z, r, j1, j2, j3, j4) = robo.pose()
        deslocamento= -10
        robo.move_to(x, y, z + deslocamento, r, wait=True) 
        robo.close()
    elif command == "ligar atuador":
        robo.suck(True)
        robo.close()
    elif command == "desligar atuador":
        robo.suck(False)
        robo.close()
    
if __name__ == '__main__':
    app.run(debug=True)
