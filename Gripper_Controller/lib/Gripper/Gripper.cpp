#include <Arduino.h>
#include "Gripper.h"
#include "Memory.h"
#include "Motor.h"

Gripper::Gripper(uint8_t speed, uint8_t pulseXLap, float maxLengthOpen_cm, uint8_t speedEmpty, uint8_t mvPerAmp)
    : Motor(speedEmpty, pulseXLap, mvPerAmp), Memory()
{
  GRIPPER_SPEED = speed;
  MAX_LENGTH_CM = maxLengthOpen_cm;
  PULSE_LAP = pulseXLap;
}

Gripper::~Gripper() {}

void Gripper::setConectMotorGripper(uint8_t pin_encoder_1, uint8_t pin_encoder_2, uint8_t pin_pwm, uint8_t pin_cw, uint8_t pin_ccw, uint8_t pin_enable, uint8_t pin_cs)
{
  setMotorConnect(pin_encoder_1, pin_encoder_2, pin_pwm, pin_cw, pin_ccw, pin_enable, pin_cs);
}

void Gripper::initialSetupGripper()
{
  if (FLAG_SETUP_GRIPPER == 0)
  {
    if (getCurrentMotor() <= getCurrentGripperNonCharge())
    {
      setMotorAddress(false);
      setMotorSpeed(100);
    }
    else
    {
      stopMotor();
      setInitCloseGripper(0);
      resetEncoderCount();
      FLAG_SETUP_GRIPPER = 1;
    }
  }
  else if (FLAG_SETUP_GRIPPER == 1)
  {
    if (getCurrentMotor() <= getCurrentGripperNonCharge())
    {
      setMotorAddress(true);
      setMotorSpeed(100);
      updateEncoderCountStatic();
    }
    else
    {
      stopMotor();
      setInitOpenGripper(getEncodeCount() - 1);
      resetEncoderCount();
      FLAG_SETUP_GRIPPER = 2;
    }
  }
}

void Gripper::setGripperPosition()
{
}

void Gripper::stopGripper()
{
  setMotorSpeed(0);
}

int ComSerial::longToPulse(float length)
{
  int upperLimit = getInitOpenGripper();
  return map(length, 0.0, MAX_LENGTH_CM, 0.0, upperLimit);
}

void Gripper::initializeGripper()
{
  initializeMotor();
}
