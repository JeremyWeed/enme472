/*
 * Jeremy Weed
 * jweed262@umd.edu
 */

#include <Arduino.h>

#define PIN_SCALE A0
#define PIN_MOTOR 0
#define MAX_SPEED 128

#define CMD_READ_SCALE 0
#define CMD_MOTOR 1

struct __attribute__ ((packed)) Msg {
  uint8_t cmd;
  union {
    int32_t val_i;
    float val_f;
  };
} msg;
Msg response;


void setup() {
  Serial.begin(115200);
  pinMode(PIN_MOTOR, OUTPUT);
}

void loop() {

  /* Wait for a message, read it and parse it, then respond with a message
   * acknowledging it or with the data requested */

  if (Serial.available() >= sizeof(Msg)) {
    Serial.readBytes((uint8_t*)&msg, sizeof(msg));

    switch (msg.cmd) {

    case CMD_READ_SCALE:
      response.val_i = analogRead(PIN_SCALE);
      response.cmd = CMD_READ_SCALE;
      Serial.write((uint8_t*)&response, sizeof(response));
      break;

    case CMD_MOTOR:
      analogWrite(PIN_MOTOR, msg.val_f * MAX_SPEED);
      response.cmd = CMD_MOTOR;
      Serial.write((uint8_t*)&response, sizeof(response));
      break;
    default:
      break;
    }
  }
}
