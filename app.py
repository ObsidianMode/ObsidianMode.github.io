from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'annemgirdimi'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'name' not in session:
        return redirect(url_for('index'))
    return render_template('index.html', name=session['name'])

@socketio.on('message')
def handle_message(data):
    print('Message received:', data)  # Debugging line
    emit('message', {'username': data['username'], 'message': data['message']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
