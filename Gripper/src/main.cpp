#include <Arduino.h>

int countEncoder = 0;
unsigned long previousTime = 0;
const int interval = 1000;
const int ENCODER = 3;

// put function declarations here:
// int myFunction(int, int);

void setup()
{
  // pinMode(ENCODER, INPUT);
  Serial.begin(115200);
  Serial.print("hello");

  // attachInterrupt(1, countSteps, RISING);
}

void loop()
{
  // unsigned long currentTime = millis();
  // if (currentTime - previousTime >= interval)
  //{
  // Serial.print('pulsos/seg: ');
  //  Serial.println(countEncoder);
  //}
}

// put function definitions here:
void countSteps()
{
  countEncoder++;
}