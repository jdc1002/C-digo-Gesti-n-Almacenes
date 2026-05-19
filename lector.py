import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. CONFIGURACIÓN DE GOOGLE SHEETS ---
archivo_json = r'D:\Prueba escaneo codigos gestion\infra-tempo-496615-n4-eced965378d7.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(archivo_json, scope)
    client = gspread.authorize(creds)
    # Usamos tu ID de hoja confirmado
    sheet = client.open_by_key("1TD-g0MfpAZjNdOMHOVxzoQ2EcWVAtyP9b9mGwN-16Qs").sheet1
    print("✅ Conexión exitosa. El limpiador de espacios está ACTIVO.")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit()

print("\n" + "="*40)
print("LECTOR PEGASUS - MODO LIMPIEZA AUTOMÁTICA")
print("="*40)

while True:
    try:
        # Recibe el código del celular (con o sin espacios)
        entrada_sucia = input("\n👉 Esperando escaneo: ").strip()

        if entrada_sucia.lower() == 'salir':
            break

        if entrada_sucia:
            # --- LIMPIEZA DE DATOS ---
            # Esto quita los espacios para que "2003 5 7" sea "200357"
            codigo_limpio = entrada_sucia.replace(" ", "")
            
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")

            # Subir el dato limpio a la nube
            sheet.append_row([fecha, hora, codigo_limpio])
            
            print(f"✔ Registrado: {codigo_limpio} | Hora: {hora}")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"❌ Error al procesar: {e}")

print("Sistema cerrado.")