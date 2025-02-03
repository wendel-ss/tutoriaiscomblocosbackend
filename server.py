from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from io import StringIO
import os

app = Flask(__name__)
# Permite todas as origens para desenvolvimento
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500", "https://tutoriaiscomblocos.netlify.app/"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Rota de healthcheck para o Render
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Python Code Execution API"
    })

@app.route('/execute', methods=['POST'])
def execute_code():
    print("Recebendo requisição para executar código")  # Debug
    code = request.json.get('code', '')
    print("Código recebido:", code)  # Debug
    
    # Captura a saída do print
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        # Executa o código
        exec(code)
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        print("Saída gerada:", output)  # Debug
        return jsonify({
            'success': True,
            'output': output
        })
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = str(e)
        print("Erro na execução:", error_msg)  # Debug
        return jsonify({
            'success': False,
            'error': error_msg
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
