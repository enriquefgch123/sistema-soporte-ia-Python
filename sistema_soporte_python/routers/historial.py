from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import obtener_conexion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/historial", response_class=HTMLResponse)
def historial_get(request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
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

@router.post("/historial", response_class=HTMLResponse)
def historial_post(request: Request, id_ticket: int = Form(...), accion: str = Form(...), categoria_final: str = Form(...), prioridad_final: str = Form(...)):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    mensaje = ""
    if accion == "validar":
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            sql = "UPDATE incidencias SET categoria_final = %s, prioridad_final = %s, estado = 'Validado' WHERE id = %s"
            cursor.execute(sql, (categoria_final, prioridad_final, id_ticket))
            conexion.commit()
            cursor.close()
            conexion.close()
            mensaje = "<div class='alert alert-success'>¡Incidencia validada correctamente por el analista!</div>"
        except Exception as e:
            mensaje = f"<div class='alert alert-danger'>Error al actualizar: {e}</div>"
            
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
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