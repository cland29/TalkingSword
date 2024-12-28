#include <Wire.h>

// I2C addresses
#define ADXL375_ADDRESS_1 0x53
#define ADXL375_ADDRESS_2 0x1D
#define BNO055_ADDRESS    0x28

// ADXL375 registers
#define DATA_FORMAT 0x31
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

  //Serial.println("Sensors initialized. Reading data...");
}

void loop() {
  // Read and print data from the first ADXL375
  //Serial.print("ADXL375 Sensor 1:");
  float gyro_x, gyro_y, gyro_z;
  readBNO055(&gyro_x, &gyro_y, &gyro_z);

  float accel_1_x, accel_1_y, accel_1_z;
  readADXL375(ADXL375_ADDRESS_1, &accel_1_x, &accel_1_y, &accel_1_z);
  // Read and print data from the second ADXL375
  //Serial.print("ADXL375 Sensor 2:");
  float accel_2_x, accel_2_y, accel_2_z;
  readADXL375(ADXL375_ADDRESS_2, &accel_2_x, &accel_2_y, &accel_2_z);

  /*
  sprintf(output_str, "%f, %.1f, %.1f, %.1f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n",
                0.0,
                gyro_x, gyro_y, gyro_z,
                accel_1_x, accel_1_y, accel_1_z,
                accel_2_x, accel_2_y, accel_2_z);
                */

  Serial.print(millis());
  Serial.print(",");
  Serial.print(gyro_x, 1);
  Serial.print(",");
  Serial.print(gyro_y, 1);
  Serial.print(",");
  Serial.print(gyro_z, 1);
  Serial.print(",");

  Serial.print(accel_1_x, 2);
  Serial.print(",");
  Serial.print(accel_1_y, 2);
  Serial.print(",");
  Serial.print(accel_1_z, 2);
  Serial.print(",");

  Serial.print(accel_2_x, 2);
  Serial.print(",");
  Serial.print(accel_2_y, 2);
  Serial.print(",");
  Serial.print(accel_2_z, 2);
  Serial.print("\n");

  // Read and print data from the BNO055
  //Serial.println("BNO055:");
  //readAndPrintBNO055();

  delay(5); // Delay between readings
}

void initializeADXL375(uint8_t address) {
  Wire.beginTransmission(address);
  Wire.write(POWER_CTL);
  Wire.write(0x08); // Set to measurement mode
  Wire.endTransmission();

   // Set the range to ±200g
  Wire.beginTransmission(address);
  Wire.write(DATA_FORMAT);
  Wire.write(0x0B); // Full resolution (bit 3 = 1), range = ±200g (bits 0-1 = 11)
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

void readADXL375(uint8_t address, float* x_g, float* y_g, float* z_g) {
  int16_t x = readAxis(address, DATAX0);
  int16_t y = readAxis(address, DATAY0);
  int16_t z = readAxis(address, DATAZ0);

  *x_g = x * 0.049;
  *y_g = y * 0.049;
  *z_g = z * 0.049;
}



float readBNO055(float* x_mps2, float* y_mps2, float* z_mps2) {
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(BNO055_ACCEL_DATA_X_LSB);
  Wire.endTransmission(false);
  Wire.requestFrom(BNO055_ADDRESS, 6);

  int16_t x = Wire.read() | (Wire.read() << 8);
  int16_t y = Wire.read() | (Wire.read() << 8);
  int16_t z = Wire.read() | (Wire.read() << 8);

  // Convert raw data to m/s^2 (1 LSB = 0.01 m/s^2)
  *x_mps2 = x * 0.01;
  *y_mps2 = y * 0.01;
  *z_mps2 = z * 0.01;
}
