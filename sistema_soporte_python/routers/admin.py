import subprocess
import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from database import obtener_conexion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/reportes", response_class=HTMLResponse)
def reportes_get(request: Request, mensaje_reentreno: str = None):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM incidencias")
    total_tickets = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as total FROM incidencias WHERE estado = 'Validado'")
    total_validados = cursor.fetchone()["total"]
    
    cursor.execute("SELECT AVG(tiempo_procesamiento_ia) as promedio FROM incidencias")
    res_promedio = cursor.fetchone()["promedio"]
    tiempo_promedio = round(res_promedio, 4) if res_promedio else 0
    
    cursor.execute("SELECT COUNT(*) as total FROM incidencias WHERE categoria_sugerida = categoria_final AND prioridad_sugerida = prioridad_final AND estado = 'Validado'")
    coincidencias = cursor.fetchone()["total"]
    
    porcentaje_exactitud = round((coincidencias / total_validados) * 100, 2) if total_validados > 0 else 0
    
    cursor.execute("SELECT categoria_sugerida, COUNT(*) as total FROM incidencias GROUP BY categoria_sugerida")
    desglose_ia = cursor.fetchall()
    
    cursor.execute("SELECT categoria_final, COUNT(*) as total FROM incidencias WHERE estado = 'Validado' AND categoria_final IS NOT NULL GROUP BY categoria_final")
    desglose_reales = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "reportes.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "total_tickets": total_tickets,
        "total_validados": total_validados,
        "tiempo_promedio": tiempo_promedio,
        "porcentaje_exactitud": porcentaje_exactitud,
        "desglose_ia": desglose_ia,
        "desglose_reales": desglose_reales,
        "mensaje_reentreno": mensaje_reentreno
    })

@router.post("/reportes/reentrenar", response_class=HTMLResponse)
def reentrenar_ia_post(request: Request):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
        
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base_dir, "reentrenar.py")
        subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        mensaje_reentreno = "<div class='alert alert-success alert-dismissible fade show' role='alert'><strong>¡Éxito!</strong> La IA se ha reentrenado correctamente.<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>"
    except Exception as ex:
        mensaje_reentreno = f"<div class='alert alert-danger alert-dismissible fade show' role='alert'><strong>Error:</strong> {str(ex)}<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>"
        
    return reportes_get(request, mensaje_reentreno=mensaje_reentreno)

@router.get("/crear-usuario", response_class=HTMLResponse)
def crear_usuario_get(request: Request):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
        
    return templates.TemplateResponse(request, "crear_usuario.html", {"mensaje": None})

@router.post("/crear-usuario", response_class=HTMLResponse)
def crear_usuario_post(request: Request, nombre: str = Form(...), email: str = Form(...), password: str = Form(...), rol: str = Form(...)):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
        
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email.strip(),))
        if cursor.fetchone():
            mensaje = "<div class='alert alert-danger'>El correo electrónico ya se encuentra registrado.</div>"
        else:
            sql = "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, email.strip(), hashed_password, rol))
            conexion.commit()
            mensaje = "<div class='alert alert-success'>¡Usuario registrado con éxito en el sistema!</div>"
        cursor.close()
        conexion.close()
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al registrar el usuario: {e}</div>"
        
    return templates.TemplateResponse(request, "crear_usuario.html", {"mensaje": mensaje})