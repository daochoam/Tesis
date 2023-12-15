#ifndef MEMORY_H
#define MEMORY_H
class Memory

{
private:
  /* data */
  float GRIPPER_CURRENT = 32;
  uint8_t POSE_GRIPPER = 48;
  uint8_t OPEN_GRIPPER = 64;
  uint8_t CLOSE_GRIPPER = 80;

public:
  Memory();
  ~Memory();
  int getPoseGripper();
  int getInitOpenGripper();
  int getInitCloseGripper();
  float getCurrentGripperNonCharge();
  void setPoseGripper(int pose);
  void setInitOpenGripper(int open);
  void setInitCloseGripper(int close);
  void setCurrentGripperNonCharge(float current);
};

#endif
