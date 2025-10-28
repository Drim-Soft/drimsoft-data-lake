"""
API simple para ejecutar el ETL desde el dashboard
Uso: python api_etl.py
"""
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir CORS desde cualquier origen

# Estado del ETL
etl_state = {
    'running': False,
    'progress': 0,
    'last_run': None,
    'last_success': None,
    'last_error': None,
    'current_step': None
}

def run_etl():
    """Ejecuta el script ETL en background"""
    global etl_state
    
    try:
        etl_state['running'] = True
        etl_state['progress'] = 0
        etl_state['last_run'] = datetime.now().isoformat()
        etl_state['last_error'] = None
        
        print("🚀 Ejecutando ETL Pipeline...")
        
        # Ejecutar el script ETL
        process = subprocess.Popen(
            ['python', 'ETL/etl4.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Simular progreso (puedes mejorar esto parseando el output real)
        for i in range(0, 101, 10):
            etl_state['progress'] = i
            time.sleep(1)
        
        # Esperar a que termine
        stdout, stderr = process.communicate(timeout=300)
        
        if process.returncode == 0:
            etl_state['last_success'] = datetime.now().isoformat()
            etl_state['progress'] = 100
            print("✅ ETL completado exitosamente")
            print(stdout)
        else:
            raise Exception(stderr or "Error desconocido en ETL")
            
    except Exception as e:
        etl_state['last_error'] = str(e)
        print(f"❌ Error en ETL: {e}")
    
    finally:
        etl_state['running'] = False

@app.route('/api/etl/trigger', methods=['POST'])
def trigger_etl():
    """Endpoint para iniciar el ETL"""
    if etl_state['running']:
        return jsonify({
            'status': 'running',
            'message': 'ETL ya está en ejecución',
            'progress': etl_state['progress']
        }), 409
    
    # Ejecutar en background
    thread = threading.Thread(target=run_etl)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'started',
        'message': 'ETL iniciado correctamente',
        'started_at': etl_state['last_run']
    }), 202

@app.route('/api/etl/status', methods=['GET'])
def get_status():
    """Obtener estado actual del ETL"""
    return jsonify(etl_state), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("🚀 Iniciando API ETL en http://localhost:5000")
    print("📡 Endpoints disponibles:")
    print("   POST /api/etl/trigger  - Ejecutar ETL")
    print("   GET  /api/etl/status   - Estado del ETL")
    print("   GET  /api/health       - Health check")
    app.run(host='0.0.0.0', port=5000, debug=True)