#include <Arduino.h>
#include "Measure.h"

Measure::Measure(float lengthOpening)
{
  this->lengthOpening = lengthOpening;
}

Measure::~Measure()
{
}

int getPulseByLength(float length)
{
  return 0;
}