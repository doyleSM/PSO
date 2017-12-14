from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chavesecreta'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/protegido?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Esta faltando o Token!!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token invalido!'}), 403

        return f(*args, **kwargs)

    return decorated
@app.route('/')
@app.route('/desprotegido')
def unprotected():
    return jsonify({'message' : 'Todos podem ver, Pagina liberada'})

@app.route('/protegido')
@token_required
def protected():
    return jsonify({'message' : 'Parabens!! seu token eh valido e voce tem acesso a pagina.'})


def token():
    
    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
    return token.decode('UTF-8')

if __name__ == '__main__':
    app.run(debug=True)