from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "notification-service",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/notify', methods=['POST'])
def notify_user_created():
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validar campos requeridos
        required_fields = ['nombre', 'email', 'telefono']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Mostrar notificación en consola (formato mejorado)
        print("\n" + "═" * 60)
        print("📧 NOTIFICACIÓN DE USUARIO CREADO - SERVICIO INDEPENDIENTE")
        print("═" * 60)
        print(f"👤 Nombre: {data['nombre']}")
        print(f"📧 Email: {data['email']}")
        print(f"📞 Teléfono: {data['telefono']}")
        if 'creado' in data:
            print(f"🕐 Creado: {data['creado']}")
        print(f"⏰ Notificado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═" * 60)
        print("💡 Este es un servicio INDEPENDIENTE de notificaciones")
        print("═" * 60 + "\n")
        
        # Simular lógica de email (sin imports problemáticos)
        simulate_email_send(data)
        
        return jsonify({
            "message": "Notificación procesada exitosamente",
            "user": data['nombre'],
            "service": "notification-service", 
            "timestamp": datetime.now().isoformat(),
            "status": "delivered_to_console"
        }), 200
        
    except Exception as e:
        print(f"❌ Error en notificación: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def simulate_email_send(user_data):
    """Simula el envío de email (para desarrollo)"""
    print(f"✉️  [SIMULACIÓN] Email enviado a administrador")
    print(f"   Asunto: Nuevo usuario - {user_data['nombre']}")
    print(f"   Contenido: Usuario {user_data['nombre']} creado exitosamente")
    print(f"   Destinatario: admin@utec.edu.uy\n")

if __name__ == '__main__':
    print("🚀 Notification Service starting...")
    print("📍 Endpoint: http://localhost:5000/notify")
    print("🔍 Health check: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=True)