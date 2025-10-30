# 🔔 Notification Service - Ejercicio 1

Servicio de notificaciones independiente para el sistema de gestión de usuarios.

## 🚀 Funcionalidades
- Recibe notificaciones via HTTP POST
- Procesa creación de nuevos usuarios
- Genera notificaciones (consola en desarrollo)

## 📋 Endpoints
- `POST /notify` - Recibe notificación de usuario creado
- `GET /health` - Health check del servicio

## 🛠️ Ejecución
```bash
pip install -r requirements.txt
python app.py