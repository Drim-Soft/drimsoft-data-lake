from flask import Flask, render_template, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import plotly.express as px
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuración desde variables de entorno (Docker)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'warehouse'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'warehouse'),
    'user': os.getenv('DB_USER', 'warehouse'),
    'password': os.getenv('DB_PASSWORD', 'warehouse123')
}

logger.info(f"📊 Conectando a: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

def execute_query(query):
    conn = None
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logger.error(f"❌ Query error: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def execute_query_dict(query):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy'}), 200
    except:
        return jsonify({'status': 'unhealthy'}), 500

@app.route('/api/stats')
def get_stats():
    stats = {}
    try:
        r = execute_query_dict("SELECT COUNT(*) as total FROM planifika_user")
        stats['total_users_planifika'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COUNT(*) as total FROM drimsoft_user")
        stats['total_users_drimsoft'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COUNT(*) as total FROM proyectos_project")
        stats['total_projects'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COUNT(*) as total FROM proyectos_task")
        stats['total_tasks'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COUNT(*) as total FROM drimsoft_ticket")
        stats['total_tickets'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COUNT(*) as total FROM suscripciones_subscription")
        stats['total_subscriptions'] = r[0]['total'] if r else 0
        
        r = execute_query_dict("SELECT COALESCE(SUM(total), 0) as revenue FROM suscripciones_invoice")
        stats['total_revenue'] = float(r[0]['revenue']) if r else 0
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/projects-status')
def projects_status():
    query = """
    SELECT ps.name as status, COUNT(*) as count
    FROM proyectos_project p
    JOIN proyectos_projectstatus ps ON p.idprojectstatus = ps.idprojectstatus
    GROUP BY ps.name
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.pie(df, values='count', names='status', title='Proyectos por Estado',
                 color_discrete_sequence=px.colors.qualitative.Set3, hole=0.3)
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/charts/tasks-status')
def tasks_status():
    query = """
    SELECT ts.name as status, COUNT(*) as count
    FROM proyectos_task t
    JOIN proyectos_taskstatus ts ON t.idtaskstatus = ts.idtaskstatus
    GROUP BY ts.name
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.bar(df, x='status', y='count', title='Tareas por Estado',
                 color='status', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False)
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/charts/tickets-status')
def tickets_status():
    query = """
    SELECT ts.name as status, COUNT(*) as count
    FROM drimsoft_ticket t
    JOIN drimsoft_ticketstatus ts ON t.idticketstatus = ts.idticketstatus
    GROUP BY ts.name
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.bar(df, x='status', y='count', title='Tickets por Estado',
                 color='status', color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(showlegend=False)
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/charts/methodology-distribution')
def methodology():
    query = """
    SELECT m.name as methodology, COUNT(*) as count
    FROM proyectos_project p
    JOIN proyectos_methodology m ON p.idmethodology = m.idmethodology
    GROUP BY m.name
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.pie(df, values='count', names='methodology', title='Metodologías',
                 color_discrete_sequence=px.colors.qualitative.Bold, hole=0.4)
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/charts/revenue-timeline')
def revenue():
    query = """
    SELECT startdate, SUM(total) as revenue
    FROM suscripciones_invoice
    WHERE startdate IS NOT NULL
    GROUP BY startdate
    ORDER BY startdate
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.line(df, x='startdate', y='revenue', title='Ingresos', markers=True)
    fig.update_traces(line_color='#10b981')
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/charts/subscriptions-status')
def subscriptions():
    query = """
    SELECT ss.name as status, COUNT(*) as count
    FROM suscripciones_invoice i
    JOIN suscripciones_subscriptionstatus ss ON i.idsubscriptionstatus = ss.idsubscriptionstatus
    GROUP BY ss.name
    """
    df = execute_query(query)
    if df.empty:
        return jsonify({'data': [], 'layout': {}})
    
    fig = px.bar(df, x='status', y='count', title='Suscripciones',
                 color='status', color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(showlegend=False)
    return jsonify(json.loads(fig.to_json()))

if __name__ == '__main__':
    logger.info("🚀 Dashboard iniciado")
    app.run(host='0.0.0.0', port=5000, debug=True)