const int trigPin = 9;
const int echoPin = 10;

float currentDistance = 0;
float previousDistance = 0;
float crackThreshold = 0.5;
int samplingInterval = 200; 

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  currentDistance = measureDistance();
  Serial.println(currentDistance); 
  delay(samplingInterval);
}

float measureDistance() {
  long duration;
  float distance;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration * 0.034) / 2;
  return distance;
}
