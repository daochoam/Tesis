// Controller.cpp
#include <Arduino.h>
#include "Controller.h"

Controller::Controller(double setpoint, double kp, double ki, double kd, double tm)
    : setPulse(0), Setpoint(setpoint), Input(0), Output(0), Kp(kp), Ki(ki), Kd(kd), Tm(tm), myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT)
{
}

Controller::~Controller()
{
}

void Controller::initPID()
{
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(1); // Refresh rate if PID controller
  myPID.SetOutputLimits(-255, 255);
}

void Controller::update()
{
  myPID.Compute();
}

void Controller::setSetpoint(double setpoint)
{

  Setpoint = setpoint;
}

double Controller::getOutput()
{
  return Output;
}
