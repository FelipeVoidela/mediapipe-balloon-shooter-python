const int pinLEDVerde = 12;
const int pinLEDVermelho = 11;
const int pinLEDAmarelo = 9; 
const int pinBuzzer = 10;

char ultimoComando = ' ';  

void setup() {
  pinMode(pinLEDVerde, OUTPUT);
  pinMode(pinLEDVermelho, OUTPUT);
  pinMode(pinLEDAmarelo, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Lê o comando recebido via serial
    char comando = Serial.read();  

    if (comando != ultimoComando) {
      ultimoComando = comando;  
      acionarLED(comando);      
      buzzer();             
    }
  }
}

void acionarLED(char comando) {
  digitalWrite(pinLEDVerde, LOW);
  digitalWrite(pinLEDVermelho, LOW);
  digitalWrite(pinLEDAmarelo, LOW);

  // Aciona o LED de acordo com o comando
  if (comando == 'G') {  // LED verde
    digitalWrite(pinLEDVerde, HIGH);
  }
  else if (comando == 'Y') {  // LED amarelo
    digitalWrite(pinLEDAmarelo, HIGH);
  }
  else if (comando == 'R') {  // LED vermelho
    digitalWrite(pinLEDVermelho, HIGH);
  }
}


void buzzer() {
  digitalWrite(pinBuzzer, HIGH);  
  delay(200);  
  digitalWrite(pinBuzzer, LOW);   
}
