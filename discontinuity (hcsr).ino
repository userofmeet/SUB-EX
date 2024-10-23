// Define pins for HC-SR04
const int trigPin = 9;
const int echoPin = 10;

// Variables for crack detection
float currentDistance = 0;
float previousDistance = 0;
float crackThreshold = 0.5; // Threshold to detect cracks (in cm)
int samplingInterval = 200; // Sampling interval in ms

void setup() {
  // Setup serial communication for debugging
  Serial.begin(9600);

  // Setup pins for HC-SR04
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initialize the previous distance
  previousDistance = measureDistance();
}

void loop() {
  // Measure the current distance from the sensor
  currentDistance = measureDistance();

  // Calculate the difference between the current and previous distance
  float distanceDifference = abs(currentDistance - previousDistance);

  // Print the distances and detection result
  Serial.print("Current Distance: ");
  Serial.print(currentDistance);
  Serial.print(" cm, Difference: ");
  Serial.print(distanceDifference);
  Serial.print(" cm");

  // Check if the difference is above the threshold (indicating a crack)
  if (distanceDifference > crackThreshold) {
    Serial.println(" ");
  } else {
    Serial.println(" ");
  }

  // Update the previous distance
  previousDistance = currentDistance;

  // Wait for the next sample
  delay(samplingInterval);
}

// Function to measure the distance using HC-SR04
float measureDistance() {
  long duration;
  float distance;

  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Trigger the sensor by setting the trigPin HIGH for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin and calculate the duration of the echo
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance in cm (duration/2 because sound travels to the object and back)
  distance = (duration * 0.034) / 2;

  // Return the measured distance
  return distance;
}
