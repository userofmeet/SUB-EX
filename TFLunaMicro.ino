#include <SoftwareSerial.h>
#include <TFMPlus.h>  // Include TFMini Plus Library v1.5.0

SoftwareSerial mySerial(10, 11); // RX, TX
TFMPlus tfmP;                    // Create a TFMini Plus object

int16_t tfDist = 0;    // Distance to object in centimeters
int16_t tfFlux = 0;    // Strength or quality of return signal
int16_t tfTemp = 0;    // Internal temperature of Lidar sensor chip

void setup() {
  Serial.begin(115200); // Initialize Serial Monitor
  mySerial.begin(115200); // Initialize Software Serial
  Serial.println("TFMPlus Library Example - Arduino Uno");

  tfmP.begin(&mySerial);   // Initialize device library object and pass device serial port to the object.
  
  // Send some example commands to the TFMini-Plus
  Serial.print("Soft reset: ");
  if (tfmP.sendCommand(SOFT_RESET, 0)) {
    Serial.println("passed.");
  } else {
    tfmP.printReply();
  }
  
  delay(500);  // Allow time for reset to complete

  // Display firmware version
  Serial.print("Firmware version: ");
  if (tfmP.sendCommand(GET_FIRMWARE_VERSION, 0)) {
    Serial.print(tfmP.version[0]);
    Serial.print(".");
    Serial.print(tfmP.version[1]);
    Serial.print(".");
    Serial.println(tfmP.version[2]);
  } else {
    tfmP.printReply();
  }

  // Set data frame rate
  Serial.print("Data-Frame rate: ");
  if (tfmP.sendCommand(SET_FRAME_RATE, FRAME_20)) {
    Serial.print(FRAME_20);
    Serial.println("Hz.");
  } else {
    tfmP.printReply();
  }
}

void loop() {
  delay(50); // Loop delay to match the 20Hz data frame rate

  if (tfmP.getData(tfDist, tfFlux, tfTemp)) { // Get data from the device
    float distanceInMeters = tfDist; // Convert distance from cm to m
    Serial.print("Dist: ");
    Serial.print(distanceInMeters, 2); // Print distance in meters with 2 decimal places
    Serial.print(" cm, Flux: ");
    Serial.print(tfFlux);
    Serial.print(", Temp: ");
    Serial.print(tfTemp);
    Serial.println(" C");
  } else { // If the command fails...
    tfmP.printFrame();  // Display the error and HEX data
  }
}
