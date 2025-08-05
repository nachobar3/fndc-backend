# FNDC Tournament API - Endpoints Documentation

## 🔓 Endpoints Públicos (Sin autenticación)

### Autenticación
- `POST /auth/login` - Login con email/password
- `POST /auth/register` - Registro de nuevo usuario
- `POST /auth/google` - Login con Google
- `POST /auth/verify-email` - Verificar email
- `POST /auth/forgot-password` - Solicitar reset de contraseña
- `POST /auth/reset-password` - Resetear contraseña

### Información General
- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc

### Torneos (Públicos)
- `GET /tournaments/` - Listar todos los torneos
- `GET /tournaments/{id}` - Ver torneo específico

### Cubos (Públicos)
- `GET /cubes/tournament/{tournament_id}/enabled` - Ver cubos habilitados para un torneo

---

## 🔐 Endpoints Protegidos (Requieren autenticación)

### Perfil de Usuario
- `GET /auth/me` - Información del usuario actual
- `GET /users/profile` - Perfil del usuario actual
- `PUT /users/profile` - Actualizar perfil

### Torneos (Acciones de usuario)
- `POST /tournaments/{id}/register` - Registrarse a un torneo
- `GET /tournaments/{id}/registrations` - Ver registros de un torneo
- `GET /tournaments/{id}/my-registration` - Verificar mi registro

### Cubos (Acciones de usuario)
- `POST /cubes/propose` - Proponer un cubo

---

## 👑 Endpoints de Administrador (Requieren rol ADMIN)

### Gestión de Usuarios
- `GET /users/` - Listar todos los usuarios
- `PUT /users/{user_id}/role` - Cambiar rol de usuario

### Gestión de Torneos
- `POST /tournaments/` - Crear nuevo torneo

### Gestión de Cubos
- `GET /cubes/tournament/{tournament_id}/all` - Ver todas las propuestas de cubos
- `PUT /cubes/{proposal_id}/status` - Cambiar estado de propuesta de cubo

---

## 📝 Ejemplos de Uso

### Endpoints Públicos (Sin token)
```bash
# Ver todos los torneos
curl https://tu-api.onrender.com/tournaments/

# Ver torneo específico
curl https://tu-api.onrender.com/tournaments/123

# Ver cubos habilitados
curl https://tu-api.onrender.com/cubes/tournament/123/enabled
```

### Endpoints Protegidos (Con token)
```bash
# Login para obtener token
curl -X POST https://tu-api.onrender.com/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@email.com&password=password"

# Usar token para endpoints protegidos
curl https://tu-api.onrender.com/auth/me \
  -H "Authorization: Bearer tu_token_aqui"

# Registrarse a un torneo
curl -X POST https://tu-api.onrender.com/tournaments/123/register \
  -H "Authorization: Bearer tu_token_aqui"
```

### Endpoints de Admin (Con token de admin)
```bash
# Crear torneo (solo admin)
curl -X POST https://tu-api.onrender.com/tournaments/ \
  -H "Authorization: Bearer token_admin_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Torneo de Magic",
    "date": "2024-01-15T10:00:00Z",
    "location": "Local de juegos",
    "start_time": "10:00",
    "duration_days": 1,
    "rounds": 4
  }'
```

---

## 🔧 Códigos de Error Comunes

- `401 Unauthorized` - Token inválido o faltante
- `403 Forbidden` - No tienes permisos (rol insuficiente)
- `404 Not Found` - Recurso no encontrado
- `422 Validation Error` - Datos de entrada inválidos
- `500 Internal Server Error` - Error del servidor

---

## 🚀 Flujo Típico de Uso

1. **Usuario visita la web** → Ve torneos sin autenticación
2. **Usuario se registra/login** → Obtiene token
3. **Usuario usa token** → Se registra a torneos, propone cubos
4. **Admin usa token admin** → Gestiona torneos y cubos 