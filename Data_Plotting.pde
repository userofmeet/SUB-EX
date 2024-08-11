import processing.serial.*;

Serial myPort;
float distance; 
ArrayList<Float> distances = new ArrayList<Float>();

void setup() 
{
  size(800, 600);
  
  // Use the correct serial port for your ESP32
  String portName = Serial.list()[0]; // Adjust index based on the available ports [0 for COM4]
  myPort = new Serial(this, portName, 115200);
  
  background(255);
  stroke(0);
  noFill();
  textSize(24); // Set the text size
  fill(0);      // Set the text color to black
}

void draw() 
{
  while (myPort.available() > 0) 
  {
    String inString = myPort.readStringUntil('\n');

    if (inString != null) 
    {
      inString = trim(inString);
      distance = float(inString);
      
      // Clip the distance to be within 100 cm
      distance = constrain(distance, 0, 100);
      
      distances.add(distance);
      
      if (distances.size() > width) { // Limit the number of points to the width of the window
        distances.remove(0);
      }
      
      background(255); // Clear the background
      
      // Scale and plot the graph as a line
      float scaleX = (float)width / distances.size();
      float scaleY = (float)height / 100; // Scale for 100 cm max
      
      if (distances.size() > 1) 
      {
        // Draw lines between consecutive points
        for (int i = 0; i < distances.size() - 1; i++) {
          float x1 = i * scaleX;
          float y1 = height - distances.get(i) * scaleY;
          float x2 = (i + 1) * scaleX;
          float y2 = height - distances.get(i + 1) * scaleY;
          line(x1, y1, x2, y2);
        }
      }
      
      // Display the current distance measured in the top-right corner
      String distanceText = String.format("Distance: %.3f cm", distance); // %.3f for distance upto 3 decimal places
      float textWidth = textWidth(distanceText);
      text(distanceText, width - textWidth - 10, 30); // Position text in the top-right corner
    }
  }
}
