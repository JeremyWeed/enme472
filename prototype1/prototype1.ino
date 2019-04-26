/*
 * Jeremy Weed
 * jweed262@umd.edu
 *
 * Using https://github.com/laurb9/StepperDriver
 */

#include <Arduino.h>
/* #include <BasicStepperDriver.h> */
#include <DRV8880.h>
/* #include <DRV8834.h> */

#define STEPS 200
#define PIN_DIR 9
#define PIN_STEP 10
#define PIN_M0 3
#define PIN_M1 4
#define PIN_M2 5

struct __attribute__ ((packed)) Msg {
  uint8_t cmd;
  union {
    int32_t val_i;
    float val_f;
    };
} msg;

DRV8880 stepper(STEPS, PIN_DIR, PIN_STEP, PIN_M0, PIN_M1);
/* DRV8834 stepper(STEPS, PIN_DIR, PIN_STEP, PIN_M0, PIN_M1); */

int rpm = 30;
int microstep = 16;

void setup() {
  Serial.begin(9600);
  stepper.begin(rpm);
  stepper.setMicrostep(microstep);
}

void loop() {
  if(Serial.available() >= sizeof(Msg)) {
    stepper.stop();
    Serial.readBytes((uint8_t*)&msg, sizeof(Msg));
    switch (msg.cmd) {
    case 0:
      rpm = msg.val_i;
      stepper.setRPM(rpm);
      break;
    case 1:
      stepper.startMove((msg.val_f * microstep * STEPS * rpm) / 60);
      break;
    case 2:
      microstep = msg.val_i;
      stepper.setMicrostep(microstep);

    case 3:
      stepper.startRotate(msg.val_i);
      break;
    default:
      break;

    }
  }
  stepper.nextAction();

  /* stepper.rotate(360); */
  /* stepper.rotate(-360); */
  /* delay(1); */
}
