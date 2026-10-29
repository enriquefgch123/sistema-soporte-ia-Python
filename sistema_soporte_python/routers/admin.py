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
    
    # 1. Total de tickets
    cursor.execute("SELECT COUNT(*) as total FROM incidencias")
    total_tickets = cursor.fetchone()["total"]
    
    # 2. Total de tickets resueltos, validados o atendidos
    cursor.execute("SELECT COUNT(*) as total FROM incidencias WHERE estado IN ('Resuelto', 'Validado', 'Atendido')")
    total_resueltos = cursor.fetchone()["total"]
    
    # 3. Tiempo promedio de la IA
    cursor.execute("SELECT AVG(tiempo_procesamiento_ia) as promedio FROM incidencias")
    res_promedio = cursor.fetchone()["promedio"]
    tiempo_promedio = round(res_promedio, 4) if res_promedio else 0.0
    
    # 4. Exactitud solo por categoría
    cursor.execute("SELECT COUNT(*) as aciertos FROM incidencias WHERE categoria_final IS NOT NULL AND categoria_final = categoria_sugerida")
    aciertos_cat = cursor.fetchone()["aciertos"]
    exactitud_cat = round((aciertos_cat / total_tickets * 100), 1) if total_tickets > 0 else 0.0
    
    # 5. Exactitud por categoría y prioridad combinadas
    cursor.execute("SELECT COUNT(*) as aciertos FROM incidencias WHERE categoria_final IS NOT NULL AND categoria_final = categoria_sugerida AND prioridad_final IS NOT NULL AND prioridad_final = prioridad_sugerida")
    aciertos_ambos = cursor.fetchone()["aciertos"]
    exactitud_cat_prio = round((aciertos_ambos / total_tickets * 100), 1) if total_tickets > 0 else 0.0
    
    # 6. Desglose general por sugerencia de la IA
    cursor.execute("SELECT categoria_sugerida, COUNT(*) as total FROM incidencias GROUP BY categoria_sugerida")
    desglose = cursor.fetchall()
    
    # 7. Desglose de incidencias resueltas o validadas por categoría final
    cursor.execute("""
        SELECT COALESCE(categoria_final, categoria_sugerida) as categoria, COUNT(*) as total 
        FROM incidencias 
        WHERE estado IN ('Resuelto', 'Validado', 'Atendido') 
        GROUP BY categoria
    """)
    desglose_resueltos = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "reportes.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "total_tickets": total_tickets,
        "total_resueltos": total_resueltos,
        "tiempo_promedio": tiempo_promedio,
        "exactitud_cat": exactitud_cat,
        "exactitud_cat_prio": exactitud_cat_prio,
        "desglose": desglose,
        "desglose_resueltos": desglose_resueltos,
        "mensaje": mensaje_reentreno
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
def crear_usuario_get(request: Request, mensaje: str = None):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email, rol FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "crear_usuario.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "usuarios": usuarios,
        "mensaje": mensaje
    })

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
        
    return crear_usuario_get(request, mensaje=mensaje)

@router.get("/eliminar-usuario/{usuario_id}", response_class=HTMLResponse)
def eliminar_usuario(request: Request, usuario_id: int):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)
    
    if request.session.get("usuario_id") == usuario_id:
        mensaje = "<div class='alert alert-danger'>No puedes eliminar tu propia cuenta de administrador.</div>"
        return crear_usuario_get(request, mensaje=mensaje)

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        mensaje = "<div class='alert alert-success'>Usuario eliminado correctamente.</div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al eliminar usuario: {e}</div>"

    return crear_usuario_get(request, mensaje=mensaje)

@router.post("/restablecer-password/{usuario_id}", response_class=HTMLResponse)
def restablecer_password(request: Request, usuario_id: int, nueva_password: str = Form(...)):
    if not request.session.get("usuario_id") or request.session.get("rol") != "Administrador":
        return RedirectResponse(url="/login", status_code=303)

    hashed_password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET password_hash = %s WHERE id = %s", (hashed_password, usuario_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        mensaje = "<div class='alert alert-success'>Contraseña restablecida con éxito.</div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al restablecer contraseña: {e}</div>"

    return crear_usuario_get(request, mensaje=mensaje)