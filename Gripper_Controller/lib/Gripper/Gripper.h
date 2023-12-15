#ifndef GRIPPER_H
#define GRIPPER_H
#include "ComSerial.h"
#include "Memory.h"
#include "Motor.h"

class Gripper : public Motor, public Memory
{
private:
  /* data */
  float LENGTH_X_LAP;
  float MAX_LENGTH_CM;
  uint8_t PULSE_LAP;
  uint8_t GRIPPER_SPEED;
  uint8_t GRIPPER_VALUE;
  uint8_t GRIPPER_STATUS;

public:
  uint8_t FLAG_SETUP_GRIPPER = 0;
  Gripper(uint8_t speed, uint8_t pulseXLap, float maxLengthOpen_cm, uint8_t speedEmpty, uint8_t mvPerAmp = 100);
  ~Gripper();
  void setConectMotorGripper(uint8_t pin_encoder_1, uint8_t pin_encoder_2, uint8_t pin_pwm, uint8_t pin_cw, uint8_t pin_ccw, uint8_t pin_enable, uint8_t pin_cs);
  void initialSetupGripper();
  void initializeGripper();
  void setGripperPosition();
  void stopGripper();
};

#endif