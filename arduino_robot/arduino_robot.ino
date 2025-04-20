// Pin Definitions
int IN1 = 3;
int IN2 = 5;
int IN3 = 6;
int IN4 = 11;

int buzzer =9;
char command; // For incoming Bluetooth command

void setup() {
  // Set motor pins as output
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(buzzer, OUTPUT);

  // Start serial for Bluetooth communication
  digitalWrite(buzzer, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();
    Serial.println(command);

    switch (command) {
      case 'F': // Forward
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;

      case 'B': // Backward
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;

      case 'L': // Left
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;

      case 'R': // Right
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;

      case 'S': // Stop
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;

       case 'Y':  // Horn (Buzzer)
        digitalWrite(buzzer, HIGH);  // Turn buzzer on
        delay(500);                  // Buzz for half a second
        digitalWrite(buzzer, LOW);   // Turn buzzer off
        break;

    }
  }
}
