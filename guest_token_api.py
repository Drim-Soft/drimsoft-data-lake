"""
API para generar Guest Tokens de Superset
Uso: python guest_token_api.py
"""
from flask import Flask, jsonify
from flask_cors import CORS
import jwt
import time
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ============================================
# CONFIGURACIÓN - DEBE COINCIDIR CON superset_config.py
# ============================================
GUEST_TOKEN_JWT_SECRET = 'DRIMSOFT_GUEST_TOKEN_SECRET_2025_PRODUCTION'
GUEST_TOKEN_JWT_AUDIENCE = 'superset'
GUEST_TOKEN_JWT_ALGO = 'HS256'
GUEST_TOKEN_JWT_EXP_SECONDS = 86400  # 24 horas

# UUID del dashboard (obtenerlo de Superset → Dashboard → ... → Embed)
DASHBOARD_ID = '7a1067c2-43db-4874-b94a-6e97889fb622'

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'guest_token_api',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/guest-token', methods=['POST', 'GET'])
def generate_guest_token():
    """
    Genera un token JWT válido para acceso embebido de Superset
    NO requiere body en la request
    """
    try:
        # Timestamp actual
        current_time = int(time.time())
        
        # Payload del JWT según documentación de Superset
        payload = {
            'user': {
                'username': 'guest_user',
                'first_name': 'Guest',
                'last_name': 'User'
            },
            'resources': [{
                'type': 'dashboard',
                'id': DASHBOARD_ID
            }],
            'rls': [],  # Row Level Security (vacío = sin restricciones)
            'iat': current_time,
            'exp': current_time + GUEST_TOKEN_JWT_EXP_SECONDS,
            'aud': GUEST_TOKEN_JWT_AUDIENCE,
            'type': 'guest'
        }
        
        # Generar token JWT
        token = jwt.encode(
            payload,
            GUEST_TOKEN_JWT_SECRET,
            algorithm=GUEST_TOKEN_JWT_ALGO
        )
        
        # PyJWT en versiones nuevas retorna string directamente
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        exp_datetime = datetime.fromtimestamp(payload['exp'])
        
        print(f"✅ Token generado: {token[:50]}...")
        print(f"📅 Expira: {exp_datetime.isoformat()}")
        
        return jsonify({
            'token': token,
            'expires_at': exp_datetime.isoformat(),
            'expires_in_seconds': GUEST_TOKEN_JWT_EXP_SECONDS,
            'dashboard_id': DASHBOARD_ID
        }), 200
        
    except Exception as e:
        print(f"❌ Error generando token: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'message': 'Error al generar guest token'
        }), 500

@app.route('/api/dashboard-config', methods=['GET'])
def get_dashboard_config():
    """Retorna la configuración del dashboard"""
    return jsonify({
        'dashboard_id': DASHBOARD_ID,
        'superset_domain': 'http://localhost:8088'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🔓 DRIMSOFT GUEST TOKEN API")
    print("=" * 70)
    print(f"🚀 Servidor: http://localhost:5001")
    print(f"📊 Dashboard: {DASHBOARD_ID}")
    print(f"⏰ Tokens válidos: {GUEST_TOKEN_JWT_EXP_SECONDS}s ({GUEST_TOKEN_JWT_EXP_SECONDS/3600:.1f}h)")
    print(f"🔐 Algoritmo: {GUEST_TOKEN_JWT_ALGO}")
    print("\n📡 Endpoints:")
    print("   POST/GET /api/guest-token      - Generar token")
    print("   GET      /api/dashboard-config - Configuración")
    print("   GET      /api/health           - Health check")
    print("\n⚠️  IMPORTANTE: SECRET debe coincidir con superset_config.py")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)