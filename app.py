from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configuração do MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Brinks%40123@localhost/pwa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

# Inicializa banco de dados e criptografia de senhas
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Modelo do usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'validador' ou 'acionador'

# Função para criar usuários iniciais
def criar_usuarios_iniciais():
    if Usuario.query.count() == 0:
        senha_hash = bcrypt.generate_password_hash('123').decode('utf-8')
        validador = Usuario(nome='Validador', email='validador@example.com', senha_hash=senha_hash, role='validador')
        acionador = Usuario(nome='Acionador', email='acionador@example.com', senha_hash=senha_hash, role='acionador')
        
        db.session.add(validador)
        db.session.add(acionador)
        db.session.commit()
        print('Usuários iniciais criados: Validador e Acionador')

# Rota para a página inicial
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.senha_hash, senha):
            session['user_id'] = usuario.id
            session['role'] = usuario.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Rota do painel após login
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'validador':
        return render_template('validador.html')
    else:
        return render_template('acionador.html')

# Rota para verificar novas mensagens
@app.route('/check_new_messages')
def check_new_messages():
    # Exemplo: Simulando a lógica de checagem de mensagens (para ajustar conforme necessidade)
    return jsonify({'new_message': False})

# Rota para enviar mensagem ao validador
@app.route('/send_message_to_validador', methods=['POST'])
def send_message_to_validador():
    data = request.get_json()
    mensagem = data.get('message')
    
    if mensagem:
        # Lógica de processamento ou armazenamento da mensagem
        print(f"Mensagem recebida: {mensagem}")
        return jsonify({'status': 'Mensagem enviada com sucesso'}), 200
    else:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400

# Função principal de execução
if __name__ == '__main__':
    with app.app_context():
        criar_usuarios_iniciais()  # Verifica e cria os usuários antes de iniciar o servidor
        app.run(host='62.72.7.88', port=5000, debug=True)
 #app.run(host='62.72.7.88', port=5000, debug=True)
