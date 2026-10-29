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
    # Mostramos tickets que estén pendientes o en proceso para la bandeja de trabajo del técnico
    cursor.execute("SELECT * FROM incidencias WHERE estado IN ('Pendiente', 'En Proceso') ORDER BY id DESC")
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
    cursor.execute("SELECT * FROM incidencias WHERE estado IN ('Pendiente', 'En Proceso') ORDER BY id DESC")
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
def historial_get(request: Request):
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
        "mensaje": None
    })