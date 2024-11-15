from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import  pymongo  as pym
from typing import Optional


# Configuración de la base de datos MongoDB
client = pym.MongoClient("mongodb+srv://cluster0.1578n.mongodb.net/", 27017,
                connect=False, username='tarea_bigdata', password='admin..')
db = client["invernaderodb"]  # Base de datos donde guardaremos los datos
collection = db["datos_p1"]  # Colección donde se almacenarán los datos

app = FastAPI()

# Modelo Pydantic para validar los datos recibidos
class SensorData(BaseModel):
    temperatura: float
    humedad_ambiente: float
    humedad_suelo:float

@app.post("/insertar/")
async def insertar_datos(sensor_data: SensorData):
    try:
        # Insertar los datos en MongoDB
        data = sensor_data.dict()
        result = collection.insert_one(data)
        return {"message": "Datos insertados correctamente", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar los datos: {str(e)}")
