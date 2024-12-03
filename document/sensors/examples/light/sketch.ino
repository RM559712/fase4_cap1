#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int ledPin = 23;
int buttonPin = 17;

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

float executeMeasurement(int minValue, int maxValue) {
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
  int buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH)
    digitalWrite(ledPin, LOW);

  else {
    digitalWrite(ledPin, HIGH);

    lcd.setCursor(0, 0);
    lcd.print("Processando...");
    delay(500);

    // > Regras: Está sendo utilizando um método para geração aleatória para simular um ambiente real
    float float_light = executeMeasurement(0, 999999);

    Serial.print("Luminosidade: ");
    Serial.print(float_light);
    Serial.print(" lux");
    Serial.println("\r\n");

    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print(float_light);
    lcd.print(" lux");
  }

  int sensorValue = analogRead(A0);
  Serial.println(sensorValue);
  delay(1000);
}
