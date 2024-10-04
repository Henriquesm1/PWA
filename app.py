from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

# Configuração do Flask e do banco de dados
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Brinks@123@localhost/pwa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Rota de painel
@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'validador':
        return render_template('validador.html')
    elif role == 'acionador':
        return render_template('acionador.html')
    return redirect(url_for('login'))

# Evento de acionamento
@socketio.on('acionamento')
def handle_acionamento(data):
    # Notifica o validador que o acionador iniciou o chat
    emit('acionamento', data, broadcast=True)

# Evento de mensagem
@socketio.on('message')
def handle_message(data):
    # Envia mensagem para todos os usuários conectados
    send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='62.72.7.88', port=5000, debug=True)
