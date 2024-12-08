from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las direcciones
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

#Funcion para compilar codigo de lenguajes no interpretados
def compile_code(filename: str, language="c"):
    #Preparamos el comando para ejecutar el archivo
    if language == "c":
        comando = ["gcc", filename, "-o", "script"]
    elif language == "cpp":
        comando = ["g++", filename, "-o", "script"]

    #Compilamos segun sea linux o windows
    if os.name == "nt":
        comando2 = [r".\script"]
    else:
        comando2 = ["./script"]
    
    # Compilar y ejecutar el archivo desde la terminal
    try:
        compilacion = subprocess.run(
            comando,
            text=True,
            capture_output=True
        )
        
        if compilacion.returncode != 0:{
            "salida": "",
            "error": compilacion.stderr,
            "return_code": compilacion.returncode
        }
        
        ejecucion = subprocess.run(
            comando2,
            text=True,
            capture_output=True
        )
        # Retornar la salida y los errores
        return {
            "output": ejecucion.stdout,
            "error": ejecucion.stderr,
            "return": ejecucion.returncode
        }
    except Exception as e:
        return {
            "error": f"Error al ejecutar el archivo: {str(e)}"
        }
    finally:
        os.remove(filename)

def execute_code(codigo: str, language="python"):
    # Ponemos la extension correspondiente al lenguaje
    if language == "python":
        filename = "script.py"
    elif language == "javascript":
        filename = "script.js"
    elif language == "c":
        filename = "script.c"
    else:
        return {
            "error": f"Lenguaje no soportado: {language}"
        }
        
    # Guardar el código en un archivo
    with open(filename, "w") as archivo:
        archivo.write(codigo)
        
    #Preparamos el comando para ejecutar el archivo
    if language == "python":
        comando = ["python", filename]
    elif language == "javascript":
        comando = ["node", filename]
    elif language == "c":
        return compile_code(filename, language)
    
    # Compilar y ejecutar el archivo desde la terminal
    try:
        resultado = subprocess.run(
            comando,
            text=True,
            capture_output=True
        )
        # Retornar la salida y los errores
        return {
            "output": resultado.stdout,
            "error": resultado.stderr,
            "return": resultado.returncode
        }
    except Exception as e:
        return {
            "error": f"Error al ejecutar el archivo: {str(e)}"
        }
    # PENDIENTE: Eliminar el archivo creado
    finally:
        os.remove(filename)

@app.post("/code/")
async def receive_code(request: Request):
    data = await request.json()
    code = data.get("code")
    language = data.get("language")
    
    if not code or not language:
        return {"output": "Code and language are required"}
    
    salida = execute_code(code, language)

    return salida