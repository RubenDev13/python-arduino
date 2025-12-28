import speech_recognition as sr
import serial
import time

# === CONFIGURACIÓN DEL PUERTO SERIE ===
# Cambia 'COM5' por el puerto donde tengas conectado el Arduino
PUERTO = 'COM5'
BAUDIOS = 9600

def conectar_arduino():
    try:
        arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
        time.sleep(2)  # Esperar a que el Arduino se reinicie
        print(f"[OK] Conectado a Arduino en {PUERTO} a {BAUDIOS} baudios")
        return arduino
    except Exception as e:
        print(f"[ERROR] No se pudo conectar con Arduino en {PUERTO}: {e}")
        return None

def enviar_comando(arduino, comando: str):
    """
    Envía un comando de texto al Arduino (por ejemplo: 'ROJO_ON')
    """
    if arduino is None:
        print("[ADVERTENCIA] Arduino no está conectado.")
        return

    texto = comando.strip() + '\n'
    arduino.write(texto.encode('utf-8'))
    print(f"→ Enviado a Arduino: {comando}")

def reconocer_voz():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nAjustando ruido ambiental... Espera un momento")
        reconocedor.adjust_for_ambient_noise(source, duration=1)

        print("¡Listo! Habla ahora...")
        try:
            audio = reconocedor.listen(source, timeout=5)
            print("Procesando audio...")

            texto = reconocedor.recognize_google(audio, language='es-ES')
            print(f"Has dicho: {texto}")
            return texto

        except sr.WaitTimeoutError:
            print("No se detectó ningún audio")
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento: {e}")
    return None

def interpretar_y_enviar(texto, arduino):
    """
    Interpreta el texto en español y envía el comando correspondiente al Arduino.
    """
    t = texto.lower()

    # ROJO
    if "rojo" in t:
        if "enciende" in t or "prender" in t:
            enviar_comando(arduino, "ROJO_ON")
            return
        if "apaga" in t:
            enviar_comando(arduino, "ROJO_OFF")
            return

    # VERDE
    if "verde" in t:
        if "enciende" in t or "prender" in t:
            enviar_comando(arduino, "VERDE_ON")
            return
        if "apaga" in t:
            enviar_comando(arduino, "VERDE_OFF")
            return

    # AZUL
    if "azul" in t:
        if "enciende" in t or "prender" in t:
            enviar_comando(arduino, "AZUL_ON")
            return
        if "apaga" in t:
            enviar_comando(arduino, "AZUL_OFF")
            return

    # Comando para salir
    if "salir" in t or "terminar" in t:
        print("Comando 'salir' detectado. Para el programa con Ctrl+C.")
        # No cerramos aquí directamente, lo manejamos en el bucle principal
        return

    print("No se reconoció un comando válido (rojo/verde/azul + encender/apagar).")

if __name__ == "__main__":
    print("=== Control por voz de 3 LEDs (rojo, verde, azul) con Arduino ===")
    print("Ejemplos de comandos de voz:")
    print("  - 'encender rojo'")
    print("  - 'apagar rojo'")
    print("  - 'encender verde'")
    print("  - 'apagar verde'")
    print("  - 'encender azul'")
    print("  - 'apagar azul'")
    print("  - 'salir' o 'terminar' para cerrar el programa\n")

    arduino = conectar_arduino()

    try:
        while True:
            texto = reconocer_voz()
            if not texto:
                print("\n" + "-"*50)
                continue

            if "salir" in texto.lower() or "terminar" in texto.lower():
                print("Cerrando programa por comando de voz...")
                break

            interpretar_y_enviar(texto, arduino)
            print("\n" + "-"*50)

    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario (Ctrl+C)")

    # Cerrar puerto serie
    if arduino and arduino.is_open:
        arduino.close()
        print("Puerto serie cerrado.")