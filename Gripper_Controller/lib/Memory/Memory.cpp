#include <Arduino.h>
#include "Memory.h"
#include <EEPROM.h> // Incluye la librería EEPROM

// Dato float ocupa como minimo 4 posiciones de la memoria EEPROM
// Dato Int ocupa como minimo 2 posiciones de la memoria EEPROM

Memory::Memory() {}

Memory::~Memory() {}

int Memory::getPoseGripper()
{
  int readValue = EEPROM.read(POSE_GRIPPER); // Lee el valor almacenado en la dirección
  return readValue;
}

int Memory::getInitOpenGripper()
{
  int readValue = EEPROM.read(OPEN_GRIPPER); // Lee el valor almacenado en la dirección
  return readValue;
}

int Memory::getInitCloseGripper()
{
  int readValue = EEPROM.read(CLOSE_GRIPPER); // Lee el valor almacenado en la dirección
  return readValue;
}

float Memory::getCurrentGripperNonCharge()
{
  float value;
  byte *p = (byte *)(void *)&value;
  for (int i = 0; i < sizeof(value); i++)
  {
    *p = EEPROM.read(GRIPPER_CURRENT + i);
    p++;
  }
  return value;
}

void Memory::setPoseGripper(int pose)
{
  EEPROM.write(POSE_GRIPPER, pose);
}

void Memory::setInitOpenGripper(int open)
{
  EEPROM.write(OPEN_GRIPPER, open);
}

void Memory::setInitCloseGripper(int close)
{
  EEPROM.write(CLOSE_GRIPPER, close);
}

void Memory::setCurrentGripperNonCharge(float current)
{
  byte *p = (byte *)(void *)&current;
  for (int i = 0; i < sizeof(current); i++)
  {
    EEPROM.write(GRIPPER_CURRENT + i, *p);
    p++;
  }
}