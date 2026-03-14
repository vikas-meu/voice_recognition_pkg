#include "DFRobot_DF2301Q.h"

DFRobot_DF2301Q_I2C DF2301Q;

void setup()
{
  Serial.begin(115200);

  // Initialize voice recognition module
  while(!(DF2301Q.begin())) {
    Serial.println("Device connection failed");
    delay(3000);
  }

  Serial.println("Voice module ready");

  // Module configuration
  DF2301Q.setVolume(4);
  DF2301Q.setMuteMode(0);
  DF2301Q.setWakeTime(15);
}

void loop()
{
  uint8_t CMDID = DF2301Q.getCMDID();

  // If a command is detected
  if(CMDID != 0) {

    // Send ONLY the command number to ROS2
    Serial.println(CMDID);

  }

  delay(100);   // small delay for stability
}
