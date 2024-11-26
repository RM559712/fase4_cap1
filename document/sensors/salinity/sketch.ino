int ledPin = 23;
int buttonPin = 17;

void setup() {

  // Led
  pinMode(ledPin, OUTPUT);

  // Botão de execução do sensor
  pinMode(buttonPin, INPUT_PULLUP);
  //pinMode(buttonPin, INPUT);

  // Parâmetro utilizado para comunicação com o display
  Serial.begin(9600);

}

float executeMeasurement(int minValue, int maxValue) {

  return minValue + (rand() % (maxValue - minValue + 1)) + (rand() % 100) / 100.0;

}

void loop() {

  int buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {

      digitalWrite(ledPin, LOW);

  }

  else {

      float float_salinity = executeMeasurement(0, 49.99);

      digitalWrite(ledPin, HIGH);
      Serial.print("Salinidade: ");
      Serial.print(float_salinity);
      Serial.print(" dS/m");
      Serial.println("\r\n");

  }

  delay(1000);

}
