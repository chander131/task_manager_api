# 🛡️ task_manager_api

Una API desarrollada en Django REST Framework, responsable de gestionar la **autenticación basada en cookies** para una aplicación cliente tipo manejador de tareas.

Este backend maneja login, logout y validación de sesión mediante cookies `HttpOnly` seguras. Se integra con MongoDB a través de `mongoengine`.

---

## 🚀 Características

- Autenticación con cookies `HttpOnly`
- Sesiones protegidas y verificables desde frontend
- Conexión con MongoDB usando `mongoengine`
- Documentación automática vía `drf-spectacular`
- CORS habilitado para integración con frontend

---

## 🧰 Tecnologías

- Python 3.11+
- Django 4.2
- Django REST Framework
- MongoDB (via `mongoengine`)
- CORS headers + JWT
- `python-dotenv` para configuración flexible

---

## ⚙️ Instalación y ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/chander131/task_manager_api.git
cd task_manager_api
```

### 2. Crea y activa un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt

```

4. Crea el archivo `.env`

```env
DATABASE_HOST=localhost
DATABASE_PORT=27017
MONGO_DB_NAME=my_db
MONGO_DB_USERNAME=user
MONGO_DB_PASSWORD=password
SECRET_KEY=
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
ENV=PROD
JWT_SECRET_KEY=my_super_secret_key

```

> Asegúrate de configurar correctamente `MONGODB_URI` con tu conexión a Atlas o Mongo local.

5. Ejecuta el servidor de desarrollo

```bash
python manage.py runserver

```

---

### 🔐 Endpoints clave

- `POST /auth/login/` – Inicia sesión y configura cookie

- `POST /auth/logout/` – Cierra sesión limpiando la cookie

- `GET /auth/me/` – Verifica usuario autenticado vía cookie

- `GET /schema/` – Documentación OpenAPI vía drf-spectacular

- `GET /docs/` – Interfaz Swagger UI (si configuraste la vista)

### 🛠️ Formateo y estilo

```bash
black .
isort .
flake8 .

```

### 📦 Despliegue con Gunicorn

```bash
gunicorn task_manager_api.wsgi:application

```

> Asegúrate de usar `.env` apropiado y tener configurado `django-cors-headers` para producción segura.

### 🧑‍💻 Contribuciones

Pull requests y sugerencias son bienvenidas.
Crea un issue para iniciar una discusión sobre mejoras o nuevas funcionalidades.

### 📄 Licencia

Este proyecto está licenciado bajo MIT. Consulta el archivo LICENSE para más detalles.
