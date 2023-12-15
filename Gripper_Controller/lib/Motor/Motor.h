#ifndef MOTOR_H
#define MOTOR_H
#include <stdint.h>

class Motor
{
private:
  /* data */
  uint8_t MOTOR_CW;
  uint8_t MOTOR_CCW;
  uint8_t MOTOR_PWM;
  uint8_t MOTOR_ENABLE;
  uint8_t MOTOR_ENCODER[2];
  uint8_t MOTOR_CS;
  uint8_t mvPerAmp;
  uint8_t speedEmpty;
  uint8_t pulseXLap;
  static volatile int encoderCount;
  static Motor *MotorInstance;

public:
  Motor(uint8_t speedEmpty, uint8_t pulseXLap, uint8_t mvPerAmp = 100);
  ~Motor();
  const short BREAK = 0;
  void stopMotor();
  void initializeMotor();
  float getCurrentMotor();
  void setMotorConnect(uint8_t pin_encoder_1, uint8_t pin_encoder_2, uint8_t pin_pwm, uint8_t pin_cw, uint8_t pin_ccw, uint8_t pin_enable, uint8_t pin_cs);
  void setMotorSpeed(const uint8_t &speed);
  void setMotorAddress(bool address = false);
  int getEncodeCount();
  void resetEncoderCount();
  void updateEncoderCount();
  static void updateEncoderCountStatic();
};

#endif