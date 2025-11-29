#importando las librerias adicionales del proyecto
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from datetime import datetime

#configurar el acceso a la base de datos
DB_SERVER = 'centroagsapo.mysql.database.azure.com'
DB_NAME = 'dbvideojuegos'
DB_USER ='utede'
DB_PASSWORD ='utede2025'
DB_PORT = 3306

#inicializar la api
app = FastAPI(title="Validar codigos QR")

class QRcodeData(BaseModel):
    qr_id:str

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    except pymysql.MySQLError as error:
        print(f"Error al conectar a la base de datos: {error}")
        raise HTTPException(status_code=500, detail="Error de conexión a la DB")
    
#metodo que validar el codigo QR
@app.post("/validate_qr")
async def validate_qr(data: QRcodeData):
    qr_id = data.qr_id.strip()
    
    #crear la conexion a la base de datos
    conn = get_db_connection()
    
    #utilizamos la herramienta cursor para ejecutar los datos
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        #buscar el registro en la tabla
        cursor.execute("SELECT idregistro,nombre,estado FROM controlinvitados WHERE idregistro = %s", (qr_id))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Código QR no encontrado")
        
        nombre_empleado = row['nombre']
         #Asumir que el 0 es no leido y 1 es leido
        estado_leido = row['estado'] 
        
        if estado_leido == 1:
            return{
                "status":"warning",
                "message":f"Error el colaborador '{nombre_empleado}'ya reclamo el bono."
            }
        else:
            #no haber reclamado el bono
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE controlinvitados SET estado = 1, fecharegistro = %s WHERE idregistro = %s", (now, qr_id))
            conn.commit()
            return{
                "status":"success",
                "message":f"Exito el colaborador '{nombre_empleado}' puede reclamar su bono."
            }    
    except HTTPException as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail = "Error interno")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0,0,0,0", port = 8000)