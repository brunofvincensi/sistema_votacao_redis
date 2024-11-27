from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
r = redis.Redis(host='localhost', port=6379, db=0)

CATEGORIAS = ['Melhor Filme', 'Melhor Série', 'Melhor Jogo']

@app.route('/')
def index():
    votos = {cat: int(r.get(f'votos:{cat}') or 0) for cat in CATEGORIAS}
    return render_template('index.html', categorias=CATEGORIAS, votos=votos)

@app.route('/votar', methods=['POST'])
def votar():
    categoria = request.form['categoria']
    r.incr(f'votos:{categoria}')
    r.rpush('log:votacoes', f'{categoria}')

    # Emitir o evento de atualização para todos os clientes conectados
    votos = {cat: int(r.get(f'votos:{cat}') or 0) for cat in CATEGORIAS}
    socketio.emit('atualizar_ranking', votos)

    return jsonify({
        'status': 'sucesso',
        'categoria': categoria
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)










