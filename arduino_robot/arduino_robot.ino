#define in1 3
#define in2 5
#define in3 6
#define in4 11
int command; 
int Speed = 204; // Fixed speed (0-255)

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Serial.begin(9600); // HC-05 default baud rate
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    Serial.print("Received: "); // Print the received command
    Serial.println(command);    // (e.g., "F", "B", etc.)
    Stop(); // Stop before new command
    
    switch(command) {
      case 'F': forward(); break;
      case 'B': back(); break;
      case 'L': left(); break;
      case 'R': right(); break;
      case 'S': Stop(); break;
    }
  }
}

// Movement functions
void forward() {
  analogWrite(in1, Speed);
  analogWrite(in3, Speed);
}

void back() {
  analogWrite(in2, Speed);
  analogWrite(in4, Speed);
}

void left() {
  analogWrite(in3, Speed);
  analogWrite(in2, Speed);
}

void right() {
  analogWrite(in4, Speed);
  analogWrite(in1, Speed);
}

void Stop() {
  analogWrite(in1, 0);
  analogWrite(in2, 0);
  analogWrite(in3, 0);
  analogWrite(in4, 0);
}