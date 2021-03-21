from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from flask_mqtt import Mqtt
import json

user1 = 'LM1993'
user2 = 'LM1'

#ip ='192.168.15.4' 
ip = '0.0.0.0'
code = 'CODE12345'

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'domotic.cloud.shiftr.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'domotic'
app.config['MQTT_PASSWORD'] = 'KgW9mvfZH89jjr70'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['SECRET_KEY'] = 'JKLMAL930201'
mqtt = Mqtt(app)
socketio = SocketIO(app)



######## MQTT FUNCTIONS #########
mqtt.subscribe('temperature')
mqtt.subscribe('relay1_server')
mqtt.subscribe('relay2_server')
mqtt.subscribe('relay3_server')
mqtt.subscribe('relay4_server')


  

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):    
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    socketio.emit('mqtt_message', data=data)


@socketio.on('verify')
def handle_verify(data):
    d = str(data)
    print('received message: ' + str(data))
    if(d == code):
        emit('disable', False)
    else:
        emit('disable', True)
        
@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('message_arduino', data)


@socketio.on('publish')
def handle_publish(json_str):
    topic = '/led'    
    payload = json_str
    #data = json.loads(json_str)
    print('DATA topic ' + str(json_str['topic']))
    #mqtt.publish(topic, payload)
    mqtt.publish(json_str['topic'], json_str['payload'])

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/')
def home():
    return "Hello World"

@app.route('/post-data', methods=['GET', 'POST'])
def post_data():
    if request.method == 'POST':
        apiKey = request.form.get('api_key')
        temp = request.form.get('temp')
        print('Api Key ' + apiKey)
        print('Temperature '+ temp)
        return apiKey


        
if __name__ == '__main__':
    #app.run(host=ip, port=5000, debug=False)
    #app.run(debug=True)
    socketio.run(app, cors_allowed_origins="*")

