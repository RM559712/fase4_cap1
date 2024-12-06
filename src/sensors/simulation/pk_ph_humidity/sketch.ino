#include <DHT.h>

// PINOS

// Definições do DHT22
#define pinoDHT 16
#define modelo DHT22
DHT dht(pinoDHT, modelo);

// Definições do HC-SR04
#define trigPin 22
#define echoPin 19
#define pinLED 22

// Definições do PIR
#define pinPIR 32
#define pinLED1 23

// Definições do LDR
#define ldrPin 13

// PushButtom1
#define buttonPPin 35  // Pino GPIO conectado ao push button P - Fosfato
#define ledPPin 27     // Pino GPIO conectado ao LEDP

// PushButtom2
#define buttonKPin 25  // Pino GPIO conectado ao push button K - Potássio
#define ledKPin 26     // Pino GPIO conectado ao LEDK

// Definições do Relé
#define relePin 15  // Pino 15 do ESP32 conectado ao Relé
#define pinLED2 17  // Pino GPIO conectado ao LED2

// Variáveis de Controle
bool fosfatoAtivado = false;  // Estado do sensor de Fosfato
bool potassioAtivado = false; // Estado do sensor de Potássio

void setup() {
    Serial.begin(115200);
    Serial.println("Sistema de Controle Inteligente Iniciado.");
    Serial.println("Digite um número para ativar sensores:");
    Serial.println("1: Fosfato");
    Serial.println("2: Potássio");
    Serial.println("3: Ambos");

    // Configuração dos pinos
    pinMode(buttonPPin, INPUT_PULLUP);
    pinMode(ledPPin, OUTPUT);
    pinMode(buttonKPin, INPUT_PULLUP);
    pinMode(ledKPin, OUTPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(pinPIR, INPUT);
    pinMode(pinLED, OUTPUT);
    pinMode(pinLED1, OUTPUT);
    pinMode(pinLED2, OUTPUT);
    pinMode(ldrPin, INPUT);
    pinMode(relePin, OUTPUT);

    dht.begin();  // Inicialização do DHT

    // Esperar entrada do usuário
    while (!fosfatoAtivado && !potassioAtivado) {
        if (Serial.available() > 0) {
            int escolha = Serial.parseInt();
            switch (escolha) {
                case 1:
                    fosfatoAtivado = true;
                    Serial.println("Leitura de Fosfato ativada!");
                    break;
                case 2:
                    potassioAtivado = true;
                    Serial.println("Leitura de Potássio ativada!");
                    break;
                case 3:
                    fosfatoAtivado = true;
                    potassioAtivado = true;
                    Serial.println("Leitura de ambos ativada!");
                    break;
                default:
                    Serial.println("Entrada inválida. Escolha 1, 2 ou 3.");
                    break;
            }
        }
    }
}

void loop() {
    // Controle do LED de Fosfato
    if (fosfatoAtivado || digitalRead(buttonPPin) == LOW) {
        digitalWrite(ledPPin, HIGH);
    } else {
        digitalWrite(ledPPin, LOW);
    }

    // Controle do LED de Potássio
    if (potassioAtivado || digitalRead(buttonKPin) == LOW) {
        digitalWrite(ledKPin, HIGH);
    } else {
        digitalWrite(ledKPin, LOW);
    }

    // Leitura do DHT (Umidade e Temperatura)
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (!isnan(h) && !isnan(t)) {
        Serial.print("Umidade: ");
        Serial.print(h);
        Serial.print(" %\t");
        Serial.print("Temperatura: ");
        Serial.print(t);
        Serial.println(" C");

        if (t > 30.0) {
            Serial.println("Alerta: Temperatura alta!");
        } else {
            Serial.println("Temperatura dentro do normal.");
        }
    } else {
        Serial.println("Erro ao ler DHT!");
    }

    // Leitura do HC-SR04 (Distância)
    long duration;
    int distance;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;

    Serial.print("Distância: ");
    Serial.print(distance);
    Serial.println(" cm");

    if (distance < 20) {
        digitalWrite(pinLED, HIGH);
    } else {
        digitalWrite(pinLED, LOW);
    }

    // Leitura do PIR
    int pirState = digitalRead(pinPIR);
    if (pirState == HIGH) {
        Serial.println("Movimento detectado!");
        digitalWrite(pinLED1, HIGH);
    } else {
        digitalWrite(pinLED1, LOW);
    }

    // Leitura do LDR
    int ldrValue = analogRead(ldrPin);
    Serial.print("Nível de Luz: ");
    Serial.println(ldrValue);

    // Controle do Relé
    static bool releState = false;
    static unsigned long lastMillis = 0;

    if (millis() - lastMillis >= 2000) {
        lastMillis = millis();
        releState = !releState;
        digitalWrite(relePin, releState ? HIGH : LOW);
        Serial.println(releState ? "Relé ligado." : "Relé desligado.");
    }

    delay(500); // Pequeno atraso para evitar leituras excessivas
}

