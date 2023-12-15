#include <Arduino.h>
#include "Motor.h"

volatile int Motor::encoderCount = 0;
Motor *Motor::MotorInstance = nullptr;

Motor::Motor(uint8_t speedEmpty, uint8_t pulseXLap, uint8_t mvPerAmp = 100)
{
  this->speedEmpty = speedEmpty;
  this->pulseXLap = pulseXLap;
  this->mvPerAmp = mvPerAmp;
  MotorInstance = this;
}

Motor::~Motor() {}

void Motor::setMotorConnect(uint8_t pin_encoder_1, uint8_t pin_encoder_2, uint8_t pin_pwm, uint8_t pin_cw, uint8_t pin_ccw, uint8_t pin_enable, uint8_t pin_cs)
{
  MOTOR_ENCODER[0] = pin_encoder_1;
  MOTOR_ENCODER[1] = pin_encoder_2;
  MOTOR_PWM = pin_pwm;
  MOTOR_CCW = pin_ccw;
  MOTOR_CW = pin_cw;
  MOTOR_ENABLE = pin_enable;
  MOTOR_CS = pin_cs;
}

void Motor::initializeMotor()
{
  // Configura la frecuencia del PWM en el pin 6
  TCCR0B = (TCCR0B & B11111000) | B00000001; // Configura el divisor de 1

  // Define PWM del Motor
  pinMode(MOTOR_PWM, OUTPUT);

  // Configuración pines del motor 1
  pinMode(MOTOR_CW, OUTPUT);
  pinMode(MOTOR_CCW, OUTPUT);
  pinMode(MOTOR_ENABLE, OUTPUT);
  pinMode(MOTOR_CS, INPUT);

  digitalWrite(MOTOR_CW, LOW);
  digitalWrite(MOTOR_CCW, LOW);
  digitalWrite(MOTOR_ENABLE, LOW);

  attachInterrupt(digitalPinToInterrupt(MOTOR_ENCODER[0]), updateEncoderCountStatic, RISING);
  setMotorAddress(false);
  setMotorSpeed(BREAK);
}

float Motor::getCurrentMotor()
{
  float currentAmps = this->MOTOR_CS / 1023.0 * 5000 / mvPerAmp;
  return currentAmps;
}

void Motor::setMotorSpeed(const uint8_t &speed) // Cambié 'long int' a 'int' para motor
{
  int _speed = speed;
  if (speed > 255)
  {
    _speed = 255;
  }
  else if (speed <= 0)
  {
    _speed = BREAK;
    digitalWrite(MOTOR_CW, LOW);
    digitalWrite(MOTOR_CCW, LOW);
  }
  analogWrite(MOTOR_PWM, _speed);
}

void Motor::setMotorAddress(bool address = false)
{
  digitalWrite(MOTOR_CW, address ? LOW : HIGH);
  digitalWrite(MOTOR_CCW, address ? HIGH : LOW);
  digitalWrite(MOTOR_ENABLE, HIGH);
}

void Motor::stopMotor()
{
  setMotorSpeed(BREAK);
}

void Motor::updateEncoderCount()
{
  if (digitalRead(MOTOR_ENCODER[0]) > digitalRead(MOTOR_ENCODER[1]))
  {
    encoderCount++;
  }
  else
  {
    encoderCount--;
  }
}

void Motor::updateEncoderCountStatic()
{
  if (MotorInstance != nullptr)
  {
    MotorInstance->updateEncoderCount();
  }
}

void Motor::resetEncoderCount()
{
  encoderCount = 0;
}

int Motor::getEncodeCount()
{
  return encoderCount;
}
