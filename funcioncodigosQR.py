import csv
import qrcode
import os

#
archivo_csv = 'basededatosempleados.csv'
columna_cedula = 'cedula'
columna_nombre = 'nombre'
directorioSalida = 'codigos_qr'


def generarCodigosQR(nombreArchivo,colcedula,colnombre, dir_salida):
    if not os.path.exists (dir_salida):
        os.makedirs (dir_salida)
        print (f"Carpeta creada con exito")

    try:
        with open (nombreArchivo, mode = "r", encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for fila in reader: 
                cedula = fila [colcedula].strip()
                nombre = fila[colnombre].strip()

                datos_qr= f"{cedula}"

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )

                #añadir datos al qr

                qr.add_data (datos_qr)
                qr.make(fit=True)

                #crear la imagen
                img= qr.make_image(fit_color="black",back_color= "white")


                #guardar imagen 
                nombreArchivo = os.path.join(dir_salida,f"{cedula}.png")
                img.save(nombreArchivo)
                
                print (f"el codigo QR con cedula {colcedula} fue creado con exito")
    except Exception as e:
        print (f"Error al generar tu codigo QR {e}")

generarCodigosQR(archivo_csv,columna_cedula,columna_nombre,directorioSalida)


