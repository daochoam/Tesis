#ifndef MEASURE_H
#define MEASURE_H
#include "ComSerial.h"
#include "Memory.h"

class Measure : public ComSerial, public Memory
{
private:
  /* data */
  float lengthOpening;
  Memory dataMemory;

public:
  Measure(float lengthOpening);
  ~Measure();
  int getPulseByLength(float length);
};

#endif