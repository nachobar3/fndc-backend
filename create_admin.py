import asyncio
import sys
import os
from datetime import datetime, UTC
from bson import ObjectId

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import connect_to_mongo, close_mongo_connection, get_db
from app.auth import get_password_hash
from app.models import UserRole


async def create_admin_user(email: str, name: str, password: str):
    """Crear un usuario administrador"""
    try:
        # Conectar a la base de datos
        await connect_to_mongo()
        db = await get_db()
        
        # Verificar si el usuario ya existe
        existing_user = await db.users.find_one({"email": email})
        if existing_user:
            print(f"❌ El usuario {email} ya existe")
            return False
        
        # Crear el usuario admin
        now = datetime.now(UTC)
        admin_user = {
            "email": email,
            "name": name,
            "hashed_password": get_password_hash(password),
            "role": UserRole.ADMIN,
            "is_verified": True,  # Los admins se crean verificados
            "created_at": now,
            "updated_at": now
        }
        
        result = await db.users.insert_one(admin_user)
        admin_user["id"] = str(result.inserted_id)
        
        print(f"✅ Usuario admin creado exitosamente:")
        print(f"   ID: {admin_user['id']}")
        print(f"   Email: {admin_user['email']}")
        print(f"   Nombre: {admin_user['name']}")
        print(f"   Rol: {admin_user['role']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuario admin: {e}")
        return False
    finally:
        await close_mongo_connection()


async def main():
    print("🔧 Crear Usuario Administrador")
    print("=" * 40)
    
    # Solicitar datos del admin
    email = input("Email del admin: ").strip()
    name = input("Nombre del admin: ").strip()
    password = input("Contraseña del admin: ").strip()
    
    if not email or not name or not password:
        print("❌ Todos los campos son requeridos")
        return
    
    # Crear el usuario admin
    success = await create_admin_user(email, name, password)
    
    if success:
        print("\n🎉 Usuario administrador creado exitosamente!")
        print("Ahora puedes usar este usuario para acceder a funciones administrativas.")
    else:
        print("\n💥 Error al crear el usuario administrador.")


if __name__ == "__main__":
    asyncio.run(main()) 