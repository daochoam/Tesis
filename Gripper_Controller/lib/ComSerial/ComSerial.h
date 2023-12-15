#ifndef COMSERIAL_H
#define COMSERIAL_H
#include <Arduino.h>
#include <stdint.h>
#include "Memory.h"

class ComSerial
{
private:
  /* data */
  uint16_t BAUD_RATE;
  String DATA_INPUT = "";

public:
  ComSerial(uint16_t baudrate = 9600);
  ~ComSerial();
  void longToPulse(float length, float maxLength);
  void initializeComSerial();
  float getSerialData();
};

#endif
