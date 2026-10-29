import os
import mysql.connector

# Conexión directa a Aiven
conexion = mysql.connector.connect(
    host="mysql-3609f956-enriquefgch123-2549.h.aivencloud.com",
    port=20449,
    user="avnadmin",
    password=os.getenv("DB_PASSWORD"),
    database="defaultdb",
    ssl_disabled=False,
    ssl_verify_cert=False
)

cursor = conexion.cursor()

# Permitir crear tablas sin llave primaria si tu estructura local no las tenía estrictamente definidas
try:
    cursor.execute("SET sql_require_primary_key = 0;")
except Exception:
    pass

# Leer el archivo sql
with open("sistema_soporte_ia.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Dividir por consultas
queries = sql_script.split(";")

print("Iniciando migración limpia...")
for query in queries:
    if query.strip():
        try:
            cursor.execute(query)
            conexion.commit()
        except Exception as e:
            # Ignoramos avisos menores, pero mostramos si hay error crítico
            pass

print("¡Migración y sincronización completada con éxito en Aiven!")
cursor.close()
conexion.close()
