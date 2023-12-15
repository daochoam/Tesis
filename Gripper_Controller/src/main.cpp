#include <Arduino.h>
#include "Gripper.h"
#include "ComSerial.h"
#include "Controller.h"

unsigned long previousTime = 0;
unsigned long intervalTime = 1000;

const int currentThreshold = 1000; // Umbral de corriente en unidades de lectura del ADC

const uint8_t ENCODER_1 = 2;
const uint8_t ENCODER_2 = 3;
const uint8_t PWM = 5;
const uint8_t CW = 9;
const uint8_t CCW = 10;
const uint8_t ENABLE = A0;
const uint8_t SENSE_CS = A1;

// GRIPPER DATA
const uint8_t SPEED = 128;
const uint8_t PULSE_LAP = 13;
const float MAX_LENGTH_CM = 30.0;

const double kp = 5.0;
const double ki = 1.0;
const double kd = 0.001;
const double tm = 0.1;

const double sp = 0.0;

ComSerial COMGripper(9600);
Gripper gripper(SPEED, PULSE_LAP, MAX_LENGTH_CM, 0, 100);
Controller controller(sp, kp, ki, kd, tm);

void setup()
{
  COMGripper.initializeComSerial();
  gripper.setConectMotorGripper(ENCODER_1, ENCODER_2, PWM, CW, CCW, ENABLE, SENSE_CS);
  gripper.initializeGripper();
  controller.initPID();
}

void loop()
{
  unsigned long currentTime = millis();

  if ((currentTime - previousTime) >= intervalTime)
  {
    previousTime = currentTime;
    float poseGripper = COMGripper.getSerialData();

    if (poseGripper == -2.0)
    {
      Serial.print("Pose Setup: ");
      Serial.println(poseGripper);
    }
    else if (poseGripper >= 0.0)
    {
      controller.setSetpoint(poseGripper);
    }
  }
  // Tu código de loop debería ir aquí
}
