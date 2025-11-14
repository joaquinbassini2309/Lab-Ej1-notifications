from flask import Flask, request, jsonify
from datetime import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

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
        
        # Mostrar notificación en consola
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
        
        # Enviar email real AL USUARIO
        email_sent = send_real_email(data)
        
        if email_sent:
            print(f"✅ Email de bienvenida enviado a: {data['email']}")
            email_status = "delivered"
        else:
            print(f"❌ Error enviando email a: {data['email']}")
            email_status = "failed"
            
        print("═" * 60 + "\n")
        
        return jsonify({
            "message": "Notificación procesada exitosamente",
            "user": data['nombre'],
            "service": "notification-service", 
            "timestamp": datetime.now().isoformat(),
            "email_status": email_status
        }), 200
        
    except Exception as e:
        print(f"❌ Error en notificación: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def send_real_email(user_data):
    """Envía un email real de bienvenida al usuario registrado"""
    try:
        # El email se envía AL USUARIO, no al administrador
        user_email = user_data['email']
        user_name = user_data['nombre']
        
        # Crear mensaje
        message = MIMEMultipart()
        message['From'] = EMAIL_SENDER
        message['To'] = user_email  # ← AL USUARIO QUE SE REGISTRÓ
        message['Subject'] = f"🎉 ¡Bienvenido {user_name} - Registro Exitoso!"
        
        # Cuerpo del email de bienvenida
        body = f"""
        <h2>¡Bienvenido a Nuestra Plataforma, {user_name}! 🚀</h2>
        
        <p>Tu registro se ha completado exitosamente. Aquí están los detalles de tu cuenta:</p>
        
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr>
                <td style="padding: 8px; background-color: #f2f2f2;"><strong>👤 Nombre:</strong></td>
                <td style="padding: 8px;">{user_name}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background-color: #f2f2f2;"><strong>📧 Email:</strong></td>
                <td style="padding: 8px;">{user_email}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background-color: #f2f2f2;"><strong>📞 Teléfono:</strong></td>
                <td style="padding: 8px;">{user_data['telefono']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background-color: #f2f2f2;"><strong>🕐 Fecha Registro:</strong></td>
                <td style="padding: 8px;">{user_data.get('creado', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</td>
            </tr>
        </table>
        
        <br>
        <p>📋 <strong>Próximos pasos:</strong></p>
        <ul>
            <li>Accede a tu cuenta en nuestra plataforma</li>
            <li>Explora todas las funcionalidades disponibles</li>
            <li>Actualiza tu perfil si lo deseas</li>
        </ul>
        
        <p>¿Tienes alguna pregunta? No dudes en contactarnos.</p>
        
        <br>
        <p><em>Este es un mensaje automático - Por favor no responder</em></p>
        <p><strong>Sistema:</strong> Lab-Ej2-microservices - UTEC</p>
        <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        message.attach(MIMEText(body, 'html'))
        
        # Conectar y enviar
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
            
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email a {user_data['email']}: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Notification Service starting...")
    print("📍 Endpoint: http://localhost:5000/notify")
    print("🔍 Health check: http://localhost:5000/health")
    print("📧 Email configurado desde: joaquin.bassini@estudiantes.utec.edu.uy")
    app.run(host='0.0.0.0', port=5000, debug=False)