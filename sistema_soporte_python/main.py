from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, tickets, historial, admin

app = FastAPI()

# Middleware de sesiones (necesario para manejar el login de usuarios)
app.add_middleware(SessionMiddleware, secret_key="clave_secreta_super_segura_sistema_soporte")

# Montar la carpeta de recursos estáticos (CSS, imágenes, logos)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir todos los routers de la aplicación
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(historial.router)
app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)