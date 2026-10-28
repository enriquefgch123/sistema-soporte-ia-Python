import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
from database import obtener_conexion

def reentrenar_modelo():
    print("Iniciando proceso de reentrenamiento optimizado...")

    # 1. Conexión a la base de datos usando el módulo centralizado
    conexion = obtener_conexion()

    # 2. Consultar solo los registros validados por el analista
    query = """
        SELECT descripcion_texto, categoria_final 
        FROM incidencias 
        WHERE estado = 'Validado' AND categoria_final IS NOT NULL
    """
    df = pd.read_sql(query, conexion)
    conexion.close()

    if len(df) < 2:
        print("Advertencia: No hay suficientes tickets validados para reentrenar.")
        return

    print(f"Reentrenando con {len(df)} registros validados...")

    # 3. Preparar los datos
    X = df['descripcion_texto']
    y = df['categoria_final']

    # 4. Vectorizador TF-IDF
    vectorizador = TfidfVectorizer(ngram_range=(1, 2))
    X_vec = vectorizador.fit_transform(X)

    # 5. Regresión Logística con balance de clases
    modelo_categoria = LogisticRegression(max_iter=1000, class_weight='balanced')
    modelo_categoria.fit(X_vec, y)

    # 6. Guardar los nuevos archivos .pkl en la raíz del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(modelo_categoria, os.path.join(base_dir, 'modelo_categoria.pkl'))
    joblib.dump(vectorizador, os.path.join(base_dir, 'vectorizador.pkl'))

    print("Modelo reentrenado con éxito. Sesgo corregido.")

if __name__ == "__main__":
    reentrenar_modelo()