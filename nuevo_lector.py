import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS Y CREDENCIALES ---
#RECUERDA: Verifica que tu archivo .json esté en esta ruta exacta
RUTA_JSON = r'D:\Prueba escaneo codigos gestion\my-project-real-497923-af07a650c060.json'

#RECUERDA: Pega aquí el ID largo de tu NUEVA hoja de Google Sheets
NUEVO_ID_HOJA = "1xS5IsO63WCl8HZGFtwujXEyFEnxKN1hpLFZ2mWaR9tA"

# El alcance o permisos que necesita el robot de Python
CONEXION_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

print("Iniciando el motor de conexión...")

try:
    # Proceso de autenticación con Google
    credenciales = ServiceAccountCredentials.from_json_keyfile_name(RUTA_JSON, CONEXION_SCOPE)
    cliente_google = gspread.authorize(credenciales)
    
    # Abrimos el documento nuevo y apuntamos directo a la pestaña Escaneos
    hoja_nube = cliente_google.open_by_key(NUEVO_ID_HOJA).worksheet("Sheet1")
    print("¡CONEXIÓN EXITOSA! El canal VS Code ↔ Google Sheets está encendido.")

except Exception as error_conexion:
    print(f"ERROR CRÍTICO DE CONEXIÓN: {error_conexion}")
    print("👉 Revisa si compartiste la hoja con el correo del JSON o si el ID es correcto.")
    exit()

print("\n" + "="*50)
print("       LECTOR PEGASUS - CAPTURA DE DATOS VIVA ")
print("="*50)
print("💡 Escribe 'salir' en cualquier momento para cerrar el programa.")

# --- BUCLE DE CAPTURA EN VIVO ---
while True:
    try:
        # Recibe el código directamente desde el teclado o lector de barras
        entrada_codigo = input("\n👉 Esperando escaneo de código: ").strip()

        # Condición para cerrar el programa de forma segura
        if entrada_codigo.lower() == 'salir':
            print("\nApagando el sistema de captura...")
            break

        # Si el usuario escaneó algo válido, se procesa
        if entrada_codigo:
            # 🧹 LIMPIEZA MÁGICA: Quitamos todos los espacios invisibles o intermedios
            codigo_limpio = entrada_codigo.replace(" ", "")
            
            # Captura de la estampa de tiempo actual del sistema
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.now().strftime("%H:%M:%S")

            # Subida de la fila de datos en tiempo real a la nube
            hoja_nube.append_row([fecha_actual, hora_actual, codigo_limpio])
            
            print(f"✔ ¡Nube Actualizada! -> Código: {codigo_limpio} | Hora: {hora_actual}")
        
    except KeyboardInterrupt:
        print("\nPrograma interrumpido desde el teclado.")
        break
    except Exception as error_bucle:
        print(f"❌ Error al enviar el dato: {error_bucle}")

print("==================================================")
print("🏁 Sistema cerrado con éxito. ¡Buen trabajo!")
print("==================================================")