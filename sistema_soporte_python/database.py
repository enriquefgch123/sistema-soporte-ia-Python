import os
import mysql.connector

def obtener_conexion():
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "sistema_soporte_ia"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "charset": "utf8mb4"
    }
    
    # Si detecta que estamos usando Aiven en la nube, activamos SSL
    if config["host"] and "aivencloud.com" in config["host"]:
        config["ssl_disabled"] = False
        config["ssl_verify_cert"] = False

    conexion = mysql.connector.connect(**config)
    return conexion