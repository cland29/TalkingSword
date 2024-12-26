#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

// Create an instance of the BNO055 sensor
Adafruit_BNO055 bno = Adafruit_BNO055(55);

//BNO055 Pinout:
//VIN → 5V
//GND → GND
//SCL → A5 (Nano I2C Clock)
//SDA → A4 (Nano I2C Data)

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10); // Wait for Serial Monitor
  }

  // Initialize the BNO055 sensor
  if (!bno.begin()) {
    Serial.println("Error: BNO055 not detected. Check wiring or I2C address.");
    while (1);
  }

  // Set the sensor to calibration mode (optional)
  bno.setExtCrystalUse(true);

  Serial.println("BNO055 initialized. Waiting for data...");
  delay(1000); // Wait for the sensor to stabilize
}

void loop() {
  // Get the sensor event
  sensors_event_t event;
  bno.getEvent(&event);

  // Print orientation data
  Serial.print("Orientation: ");
  Serial.print("X = ");
  Serial.print(event.orientation.x, 1);
  Serial.print("°, Y = ");
  Serial.print(event.orientation.y, 1);
  Serial.print("°, Z = ");
  Serial.print(event.orientation.z, 1);
  Serial.println("°");

  // Print calibration status (optional)
  uint8_t system, gyro, accel, mag;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  Serial.print("Calibration: Sys=");
  Serial.print(system);
  Serial.print(" Gyro=");
  Serial.print(gyro);
  Serial.print(" Accel=");
  Serial.print(accel);
  Serial.print(" Mag=");
  Serial.println(mag);

  delay(500); // Update every 500ms
}
