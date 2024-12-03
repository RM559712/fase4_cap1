#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int8_t ledPin = 23;
int8_t buttonPin = 17;

void search12C() {
  Serial.println("Escaneando endereços I2C...");
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.print("Endereço I2C encontrado: ");
      Serial.println(i, DEC);
    }
  }
}

float executeMeasurement(int8_t minValue, int8_t maxValue) {
  return minValue + (rand() % (maxValue - minValue + 1)) + (rand() % 100) / 100.0;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // > Importante: Utilizar apenas para mapear o endereço do LCD caso necessário
  //search12C();

  lcd.begin(16, 2);
  lcd.backlight();
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int8_t buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) 
    digitalWrite(ledPin, LOW);

  else {
    digitalWrite(ledPin, HIGH);

    lcd.setCursor(0, 0);
    lcd.print("Processando...");
    delay(500);

    // > Regras: Está sendo utilizando um método para geração aleatória para simular um ambiente real
    float float_humidity = executeMeasurement(0, 100.00);

    Serial.print("Umidade: ");
    Serial.print(float_humidity);
    Serial.print("%");
    Serial.println("");

    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print(float_humidity);
    lcd.print("%");
  }

  int8_t sensorValue = analogRead(A0);
  Serial.println(sensorValue); 
  delay(1000);
}
