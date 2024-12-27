#include <Wire.h>

// I2C addresses
#define ADXL375_ADDRESS_1 0x53
#define ADXL375_ADDRESS_2 0x1D
#define BNO055_ADDRESS    0x28

// ADXL375 registers
#define POWER_CTL 0x2D
#define DATAX0 0x32
#define DATAY0 0x34
#define DATAZ0 0x36


// BNO055 registers
#define BNO055_OPR_MODE 0x3D
#define BNO055_ACCEL_DATA_X_LSB 0x08

//BNO055 Pinout:
//VIN → 5V
//GND → GND
//SCL → A5 (Nano I2C Clock)
//SDA → A4 (Nano I2C Data)

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize sensors
  initializeADXL375(ADXL375_ADDRESS_1);
  initializeADXL375(ADXL375_ADDRESS_2);
  initializeBNO055();

  Serial.println("Sensors initialized. Reading data...");
}

void loop() {
  // Read and print data from the first ADXL375
  //Serial.print("ADXL375 Sensor 1:");
  float accel_1 = readAndPrintADXL375Univalue(ADXL375_ADDRESS_1);

  // Read and print data from the second ADXL375
  //Serial.print("ADXL375 Sensor 2:");
  float accel_2 = readAndPrintADXL375Univalue(ADXL375_ADDRESS_2);

  Serial.print(accel_1, 4);
  Serial.print(",");
  Serial.println(accel_2, 4);
  //Serial.println("Hello from Arduino!");

  // Read and print data from the BNO055
  //Serial.println("BNO055:");
  //readAndPrintBNO055();

  delay(500); // Delay between readings
}

void initializeADXL375(uint8_t address) {
  Wire.beginTransmission(address);
  Wire.write(POWER_CTL);
  Wire.write(0x08); // Set to measurement mode
  Wire.endTransmission();
}

void initializeBNO055() {
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(BNO055_OPR_MODE);
  Wire.write(0x0C); // Set to NDOF mode
  Wire.endTransmission();
}

int16_t readAxis(uint8_t address, uint8_t axisAddress) {
  Wire.beginTransmission(address);
  Wire.write(axisAddress);
  Wire.endTransmission(false);
  Wire.requestFrom(address, 2);

  int16_t axisData = Wire.read() | (Wire.read() << 8);
  return axisData;
}

void readAndPrintADXL375(uint8_t address) {
  int16_t x = readAxis(address, DATAX0);
  int16_t y = readAxis(address, DATAY0);
  int16_t z = readAxis(address, DATAZ0);

  float x_g = x * 0.049;
  float y_g = y * 0.049;
  float z_g = z * 0.049;

  Serial.print("X: ");
  Serial.print(x_g, 2);
  Serial.print(" g, Y: ");
  Serial.print(y_g, 2);
  Serial.print(" g, Z: ");
  Serial.print(z_g, 2);
  Serial.println(" g");
}
float readAndPrintADXL375Univalue(uint8_t address) {
  int16_t x = readAxis(address, DATAX0);
  int16_t y = readAxis(address, DATAY0);
  int16_t z = readAxis(address, DATAZ0);

  float x_g = x * 0.049;
  float y_g = y * 0.049;
  float z_g = z * 0.049;

  float a_g = sqrt(sq(x_g) + sq(y_g) + sq(z_g));

  
  return a_g;
}


void readAndPrintBNO055() {
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(BNO055_ACCEL_DATA_X_LSB);
  Wire.endTransmission(false);
  Wire.requestFrom(BNO055_ADDRESS, 6);

  int16_t x = Wire.read() | (Wire.read() << 8);
  int16_t y = Wire.read() | (Wire.read() << 8);
  int16_t z = Wire.read() | (Wire.read() << 8);

  // Convert raw data to m/s^2 (1 LSB = 0.01 m/s^2)
  float x_mps2 = x * 0.01;
  float y_mps2 = y * 0.01;
  float z_mps2 = z * 0.01;

  Serial.print("X: ");
  Serial.print(x_mps2, 2);
  Serial.print(" m/s^2, Y: ");
  Serial.print(y_mps2, 2);
  Serial.print(" m/s^2, Z: ");
  Serial.print(z_mps2, 2);
  Serial.println(" m/s^2");
}
