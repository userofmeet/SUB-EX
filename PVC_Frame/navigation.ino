#include <Servo.h>
#include <ArduinoJson.h>

Servo escL, escR, escV;

int pwmL = 1000;
int pwmR = 1000;
int pwmV = 1000;

unsigned long last_signal = 0;

void setup() {
  Serial.begin(115200);

  escL.attach(3);
  escR.attach(5);
  escV.attach(6);

  // ARM ESCs (SimonK needs minimum throttle)
  escL.writeMicroseconds(1000);
  escR.writeMicroseconds(1000);
  escV.writeMicroseconds(1000);
  
  delay(3000);   // Let ESCs ARM
}

void loop() {

  if (Serial.available()) {
    String json_str = Serial.readStringUntil('\n');
    StaticJsonDocument<128> doc;

    if (deserializeJson(doc, json_str) == DeserializationError::Ok) {

      if (doc.containsKey("L")) pwmL = doc["L"];
      if (doc.containsKey("R")) pwmR = doc["R"];
      if (doc.containsKey("V")) pwmV = doc["V"];

      pwmL = constrain(pwmL, 1000, 2000);
      pwmR = constrain(pwmR, 1000, 2000);
      pwmV = constrain(pwmV, 1000, 2000);

      last_signal = millis();
    }
  }

  // FAILSAFE: if PC disconnects → STOP motors
  if (millis() - last_signal > 500) {
    pwmL = pwmR = pwmV = 1000;
  }

  // Update ESC signals
  escL.writeMicroseconds(pwmL);
  escR.writeMicroseconds(pwmR);
  escV.writeMicroseconds(pwmV);
}
