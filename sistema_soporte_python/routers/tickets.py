import time
import os
import joblib
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import obtener_conexion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO_PATH = os.path.join(BASE_DIR, 'modelo_categoria.pkl')
VECTORIZADOR_PATH = os.path.join(BASE_DIR, 'vectorizador.pkl')

if os.path.exists(MODELO_PATH) and os.path.exists(VECTORIZADOR_PATH):
    model_categoria = joblib.load(MODELO_PATH)
    vectorizador = joblib.load(VECTORIZADOR_PATH)
else:
    model_categoria = None
    vectorizador = None

@router.get("/", response_class=HTMLResponse)
def index_get(request: Request, mensaje: str = None):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
    
    usuario_id = request.session.get("usuario_id")
    rol = request.session.get("rol")
    nombre = request.session.get("nombre")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    if rol == "Cliente":
        cursor.execute("SELECT * FROM incidencias WHERE usuario_id = %s ORDER BY id DESC", (usuario_id,))
    else:
        cursor.execute("SELECT * FROM incidencias ORDER BY id DESC")
        
    mis_tickets = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return templates.TemplateResponse(request, "index.html", {
        "nombre": nombre,
        "rol": rol,
        "mis_tickets": mis_tickets,
        "mensaje": mensaje
    })

@router.post("/", response_class=HTMLResponse)
def index_post(request: Request, descripcion: str = Form(...)):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
    
    usuario_id = request.session.get("usuario_id")
    rol = request.session.get("rol")
    nombre = request.session.get("nombre")
    
    if not model_categoria or not vectorizador:
        mensaje = "<div class='alert alert-danger'>Error: No se encontraron los archivos del modelo de IA (.pkl).</div>"
        return index_get(request, mensaje=mensaje)

    codigo_ticket = f"TICK-{int(time.time())}"
    inicio = time.time()
    
    texto_vectorizado = vectorizador.transform([descripcion])
    categoria_sugerida = model_categoria.predict(texto_vectorizado)[0]
    prioridad_sugerida = "Media"
    
    fin = time.time()
    tiempo_ia = round(fin - inicio, 4)
    
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO incidencias (codigo_ticket, descripcion_texto, categoria_sugerida, prioridad_sugerida, tiempo_procesamiento_ia, estado, usuario_id) 
            VALUES (%s, %s, %s, %s, %s, 'Pendiente', %s)
        """
        cursor.execute(sql, (codigo_ticket, descripcion, categoria_sugerida, prioridad_sugerida, tiempo_ia, usuario_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        mensaje = f"<div class='alert alert-success alert-dismissible fade show' role='alert'>¡Incidencia registrada y clasificada por la IA con éxito! Ticket: <strong>{codigo_ticket}</strong> | Categoría Sugerida: <strong>{categoria_sugerida}</strong><button type='button' class='btn-close' data-bs-dismiss='alert'></button></div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al guardar en la BD: {e}</div>"
        
    return index_get(request, mensaje=mensaje)

@router.post("/resolver-ticket/{ticket_id}", response_class=HTMLResponse)
def resolver_ticket_cliente(request: Request, ticket_id: int):
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    usuario_id = request.session.get("usuario_id")
    
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE incidencias SET estado = 'Resuelto' WHERE id = %s AND usuario_id = %s"
        cursor.execute(sql, (ticket_id, usuario_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        mensaje = "<div class='alert alert-success alert-dismissible fade show' role='alert'>¡Gracias por confirmar! Tu ticket ha sido marcado como <strong>Resuelto</strong>.<button type='button' class='btn-close' data-bs-dismiss='alert'></button></div>"
    except Exception as e:
        mensaje = f"<div class='alert alert-danger'>Error al actualizar el ticket: {e}</div>"
        
    return index_get(request, mensaje=mensaje)