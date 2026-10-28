from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from database import obtener_conexion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    if request.session.get("usuario_id"):
        rol = request.session.get("rol")
        if rol == "Administrador":
            return RedirectResponse(url="/reportes", status_code=303)
        elif rol == "Analista":
            return RedirectResponse(url="/historial", status_code=303)
        else:
            return RedirectResponse(url="/", status_code=303)
            
    return templates.TemplateResponse(request, "login.html", {"error": ""})

@router.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email.strip(),))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    if not usuario:
        return templates.TemplateResponse(request, "login.html", {"error": "El correo electrónico no está registrado."})
    
    if not bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
        return templates.TemplateResponse(request, "login.html", {"error": "Contraseña incorrecta."})
    
    # Guardar datos en la sesión
    request.session["usuario_id"] = usuario["id"]
    request.session["nombre"] = usuario["nombre"]
    request.session["rol"] = usuario["rol"]
    
    # Redirigir limpiamente según el rol
    rol = usuario["rol"]
    if rol == "Administrador":
        return RedirectResponse(url="/reportes", status_code=303)
    elif rol == "Analista":
        return RedirectResponse(url="/historial", status_code=303)
    else:
        return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)