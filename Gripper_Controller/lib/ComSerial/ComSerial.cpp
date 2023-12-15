#include <Arduino.h>
#include "ComSerial.h"
#include "Memory.h"

ComSerial::ComSerial(uint16_t baudrate)
{
  BAUD_RATE = baudrate;
}
ComSerial::~ComSerial() {}

float ComSerial::getSerialData()
{
  String SETUP_COMMAND = "setup";
  if (Serial.available() > 0)
  {
    // Lee un carácter
    char digit = Serial.read();

    if (isdigit(digit) || digit == '.' || digit == '-')
    {
      DATA_INPUT += digit;
    }
    else if (SETUP_COMMAND.indexOf(tolower(digit)) != -1)
    {
      DATA_INPUT += digit;
    }
    else if (digit == '\n')
    {
      if (DATA_INPUT.equalsIgnoreCase(SETUP_COMMAND))
      {
        DATA_INPUT = "";
        return -2.0;
      }
      else if (DATA_INPUT.indexOf('.') != -1)
      {
        // Si hay un punto, asumimos que es un número flotante
        float DATA_FLOAT = DATA_INPUT.toFloat();
        DATA_INPUT = ""; // Reinicia el buffer
        return DATA_FLOAT;
      }
      else
      {
        DATA_INPUT = "";
        return -1.0;
      }
    }
  }
  return -1.0;
}

void ComSerial::initializeComSerial()
{
  Serial.begin(BAUD_RATE);
}