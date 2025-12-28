// === Control de 3 LEDs por comandos seriales ===
// Comandos esperados desde Python (sin comillas):
//   ROJO_ON   / ROJO_OFF
//   VERDE_ON  / VERDE_OFF
//   AZUL_ON   / AZUL_OFF

const int LED_ROJO  = 8;
const int LED_VERDE = 9;
const int LED_AZUL  = 10;

String comando = "";

void setup() {
  pinMode(LED_ROJO, OUTPUT); 
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AZUL, OUTPUT);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AZUL, LOW);

  Serial.begin(9600);
  Serial.println("Arduino listo. Esperando comandos...");
}

void loop() {
  // Leer datos del puerto serie
  while (Serial.available() > 0) {
    char c = Serial.read();

    // Fin de línea = fin de comando
    if (c == '\n' || c == '\r') {
      if (comando.length() > 0) {
        procesarComando(comando);
        comando = "";  // limpiar para el siguiente
      }
    } else {
      comando += c;   // acumular
    }
  }
}

void procesarComando(String cmd) {
  cmd.trim();  // eliminar espacios y saltos extra

  Serial.print("Comando recibido: ");
  Serial.println(cmd);

  // ROJO
  if (cmd == "ROJO_ON") {
    digitalWrite(LED_ROJO, HIGH);
    Serial.println("LED ROJO encendido");
  } else if (cmd == "ROJO_OFF") {
    digitalWrite(LED_ROJO, LOW);
    Serial.println("LED ROJO apagado");
  }

  // VERDE
  else if (cmd == "VERDE_ON") {
    digitalWrite(LED_VERDE, HIGH);
    Serial.println("LED VERDE encendido");
  } else if (cmd == "VERDE_OFF") {
    digitalWrite(LED_VERDE, LOW);
    Serial.println("LED VERDE apagado");
  }

  // AZUL
  else if (cmd == "AZUL_ON") {
    digitalWrite(LED_AZUL, HIGH);
    Serial.println("LED AZUL encendido");
  } else if (cmd == "AZUL_OFF") {
    digitalWrite(LED_AZUL, LOW);
    Serial.println("LED AZUL apagado");
  }

  else {
    Serial.println("Comando no reconocido");
  }
}