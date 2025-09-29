import requests
import base64
import os
import json

# --- CONFIGURACIÓN ---
# Reemplaza esta URL con la URL de tu API Gateway que obtuviste al desplegar con SAM
API_ENDPOINT_URL = "https://TU_API_ID.execute-api.us-east-1.amazonaws.com/Prod"

# Datos para la prueba
USER_ID = "test-user-001"
DOCUMENT_TYPE = "factura"
PDF_FILE_PATH = "dummy.pdf"  # Asegúrate de que este archivo exista en la misma carpeta

def test_upload_document():
    """
    Prueba el endpoint POST /documents para subir un archivo.
    """
    print("--- 🚀 Iniciando Prueba de Carga (POST) ---")
    
    upload_url = f"{API_ENDPOINT_URL}/documents"

    # Verificar que el archivo PDF de prueba existe
    if not os.path.exists(PDF_FILE_PATH):
        print(f"❌ Error: El archivo '{PDF_FILE_PATH}' no se encuentra. Crea un PDF de prueba.")
        return

    # 1. Leer el archivo y codificarlo en base64
    with open(PDF_FILE_PATH, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')

    # 2. Preparar el payload JSON
    payload = {
        "user_id": USER_ID,
        "document_type": DOCUMENT_TYPE,
        "file_base64": encoded_string
    }

    # 3. Enviar la petición POST
    try:
        response = requests.post(upload_url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.json()}")

        if response.status_code == 201:
            print("✅ ¡Prueba de Carga Exitosa!")
        else:
            print("❌ ¡Prueba de Carga Fallida!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_get_document():
    """
    Prueba el endpoint GET /documents/{user_id}/{document_type} para consultar un archivo.
    """
    print("\n--- 📥 Iniciando Prueba de Consulta (GET) ---")
    
    get_url = f"{API_ENDPOINT_URL}/documents/{USER_ID}/{DOCUMENT_TYPE}"

    try:
        # 1. Enviar la petición GET
        response = requests.get(get_url)

        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # 2. Decodificar la respuesta y guardar el archivo
            data = response.json()
            file_content_base64 = data.get("file_content_base64")
            
            if file_content_base64:
                decoded_file = base64.b64decode(file_content_base64)
                output_filename = f"descargado_{USER_ID}_{DOCUMENT_TYPE}.pdf"
                
                with open(output_filename, "wb") as f:
                    f.write(decoded_file)
                
                print(f"✅ ¡Prueba de Consulta Exitosa! Archivo guardado como '{output_filename}'")
            else:
                print("❌ Error: La respuesta no contenía el contenido del archivo en base64.")

        elif response.status_code == 404:
             print("ℹ️  Documento no encontrado, lo cual puede ser esperado.")
        else:
            print(f"❌ ¡Prueba de Consulta Fallida! Respuesta: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

# Ejecutar las pruebas
if __name__ == "__main__":
    # Primero, asegúrate de que el archivo dummy.pdf exista
    if not os.path.exists(PDF_FILE_PATH):
         print(f"Creando un archivo '{PDF_FILE_PATH}' de prueba...")
         # Crear un PDF muy simple si no existe (requiere una librería como fpdf)
         # Por simplicidad, pedimos al usuario crearlo manualmente.
         print(f"Por favor, crea un archivo llamado '{PDF_FILE_PATH}' en este directorio y vuelve a ejecutar.")
    else:
        test_upload_document()
        test_get_document()