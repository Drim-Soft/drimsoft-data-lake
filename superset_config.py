# superset_config.py
# Configuración de producción con Guest Token habilitado

import os

# ============================================
# SECRET KEYS - CRÍTICO: Deben coincidir
# ============================================
# Este es el SECRET_KEY principal de Superset
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY', 'supersecretkey123456789abcdefgh')

# Este es el secreto ESPECÍFICO para Guest Tokens (puede ser diferente)
GUEST_TOKEN_JWT_SECRET = 'DRIMSOFT_GUEST_TOKEN_SECRET_2025_PRODUCTION'
GUEST_TOKEN_JWT_AUDIENCE = 'superset'
GUEST_TOKEN_JWT_ALGO = 'HS256'
GUEST_TOKEN_JWT_EXP_SECONDS = 86400  # 24 horas

# ============================================
# SEGURIDAD - Deshabilitar para desarrollo
# ============================================
TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False
WTF_CSRF_EXEMPT_LIST = ['*']

# ============================================
# CORS - Permitir TODOS los orígenes
# ============================================
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': '*',
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
}

# ============================================
# COOKIES - Configuración para iframes
# ============================================
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

# ============================================
# HEADERS - Permitir embedding en iframes
# ============================================
HTTP_HEADERS = {}
OVERRIDE_HTTP_HEADERS = {}

# ============================================
# FEATURE FLAGS - Habilitar Guest Token
# ============================================
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_RBAC": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
}

# ============================================
# EMBEDDING - Configuración Guest Token
# ============================================
GUEST_ROLE_NAME = "Public"
EMBEDDED_SUPERSET = True

# ============================================
# CACHE - Redis
# ============================================
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 0,
}

DATA_CACHE_CONFIG = CACHE_CONFIG

# ============================================
# REFRESH - Auto-refresh dashboards
# ============================================
SUPERSET_DASHBOARD_PERIODICAL_REFRESH_LIMIT = 0
SUPERSET_DASHBOARD_PERIODICAL_REFRESH_WARNING_MESSAGE = None

# ============================================
# PUBLIC ROLE
# ============================================
PUBLIC_ROLE_LIKE = "Gamma"

# ============================================
# ROW LEVEL SECURITY
# ============================================
ROW_LEVEL_SECURITY_ENABLED = True