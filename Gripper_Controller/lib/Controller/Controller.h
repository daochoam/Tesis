// Controller.h

#ifndef Controller_h
#define Controller_h

#include <Arduino.h>
#include <PID_v1.h>

class Controller
{
private:
  double setPulse;
  double Setpoint;
  double Input, Output;
  float Kp, Ki, Kd, Tm;
  PID myPID;

public:
  Controller(double setpoint, double kp, double ki, double kd, double tm);
  ~Controller();
  void initPID();
  void update();
  void setSetpoint(double setpoint);
  double getOutput();
};

#endif
