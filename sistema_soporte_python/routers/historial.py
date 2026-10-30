from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import obtener_conexion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/bandeja", response_class=HTMLResponse)
def bandeja_get(request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # Mostramos tickets que estén pendientes , en proceso y atentido para la bandeja de trabajo del analista
    cursor.execute("SELECT * FROM incidencias WHERE estado IN ('Pendiente', 'En Proceso', 'Atendido') ORDER BY id DESC")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "bandeja.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "resultados": resultados,
        "mensaje": None
    })

@router.post("/bandeja", response_class=HTMLResponse)
def bandeja_post(request: Request, id_ticket: int = Form(...), estado_nuevo: str = Form(...), categoria_final: str = Form(...), prioridad_final: str = Form(...)):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE incidencias 
            SET categoria_final = %s, prioridad_final = %s, estado = %s 
            WHERE id = %s
        """
        cursor.execute(sql, (categoria_final, prioridad_final, estado_nuevo, id_ticket))
        conexion.commit()
        cursor.close()
        conexion.close()
        mensaje = f"<div class='alert alert-success'>Ticket actualizado correctamente a estado: <strong>{estado_nuevo}</strong></div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al actualizar el ticket: {e}</div>"
            
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # Incluimos 'Atendido' aquí también para que al hacer clic en Actualizar sigan apareciendo en pantalla
    cursor.execute("SELECT * FROM incidencias WHERE estado IN ('Pendiente', 'En Proceso', 'Atendido') ORDER BY id DESC")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "bandeja.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "resultados": resultados,
        "mensaje": mensaje
    })

@router.get("/historial", response_class=HTMLResponse)
def historial_get(request: Request, mensaje: str = None):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # Historial general con todos los tickets
    cursor.execute("SELECT * FROM incidencias ORDER BY id DESC")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "historial.html", {
        "nombre": request.session.get("nombre"),
        "rol": request.session.get("rol"),
        "resultados": resultados,
        "mensaje": mensaje
    })

@router.post("/historial", response_class=HTMLResponse)
def historial_post(
    request: Request, 
    id_ticket: int = Form(...), 
    categoria_final: str = Form(...), 
    prioridad_final: str = Form(...)
):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Actualizamos únicamente la categoría y prioridad final sin sobreescribir el estado actual
        sql = """
            UPDATE incidencias 
            SET categoria_final = %s, prioridad_final = %s 
            WHERE id = %s
        """
        cursor.execute(sql, (categoria_final, prioridad_final, id_ticket))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        mensaje = "<div class='alert alert-success alert-dismissible fade show' role='alert'>¡Validación final actualizada con éxito!<button type='button' class='btn-close' data-bs-dismiss='alert'></button></div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al actualizar la incidencia: {e}</div>"
        
    return historial_get(request, mensaje=mensaje)

@router.get("/eliminar-ticket/{ticket_id}", response_class=HTMLResponse)
def eliminar_ticket(request: Request, ticket_id: int):
    if not request.session.get("usuario_id") or request.session.get("rol") not in ["Administrador", "Analista"]:
        return RedirectResponse(url="/login", status_code=303)
        
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM incidencias WHERE id = %s", (ticket_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        mensaje = "<div class='alert alert-success alert-dismissible fade show' role='alert'>¡Incidencia eliminada correctamente!<button type='button' class='btn-close' data-bs-dismiss='alert'></button></div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al eliminar la incidencia: {e}</div>"
        
    return historial_get(request, mensaje=mensaje)