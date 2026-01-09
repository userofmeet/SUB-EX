#include <Servo.h>

Servo thrusterLeft;     
Servo thrusterRight;   
Servo thrusterVertical; 

const int PIN_LEFT = 3;
const int PIN_RIGHT = 5;
const int PIN_VERTICAL = 6;

int speedLeft = 0;
int speedRight = 0;
int speedVertical = 0;

void setup() {
  Serial.begin(115200);
  
  Serial.println("Arduino Reset Detected!");
  Serial.println("DONT CONNECT THE BATTERY");
  Serial.println("Waiting 3 seconds...");
  delay(3000);
  
  thrusterLeft.attach(PIN_LEFT);
  thrusterRight.attach(PIN_RIGHT);
  thrusterVertical.attach(PIN_VERTICAL);
  
  Serial.println(" all motors to OFF position...");
  thrusterLeft.write(0);
  thrusterRight.write(0);
  thrusterVertical.write(0);
  
  Serial.println("");
  Serial.println("CONNECT BATTERY");
  Serial.println("ESCs will beep to confirm arming.");
  
  // Wait for ESCs to arm 
  delay(5000);
  
  Serial.println("");
  Serial.println("ESCs should be armed now!");
  Serial.println("Motors are OFF and waiting for controller.");
  Serial.println("Ready to receive input...");
  Serial.println("");
}

void loop() {
  // Check for serial data from Python
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    int firstComma = data.indexOf(',');
    int secondComma = data.indexOf(',', firstComma + 1);
    
    if (firstComma > 0 && secondComma > 0) {
      speedLeft = data.substring(0, firstComma).toInt();
      speedRight = data.substring(firstComma + 1, secondComma).toInt();
      speedVertical = data.substring(secondComma + 1).toInt();
      
      speedLeft = constrain(speedLeft, 0, 180);
      speedRight = constrain(speedRight, 0, 180);
      speedVertical = constrain(speedVertical, 0, 180);
      
      thrusterLeft.write(speedLeft);
      thrusterRight.write(speedRight);
      thrusterVertical.write(speedVertical);
      
      Serial.print("Thrusters -> L:");
      Serial.print(speedLeft);
      Serial.print(" R:");
      Serial.print(speedRight);
      Serial.print(" V:");
      Serial.println(speedVertical);
    }
  }
  
  delay(20);
}
