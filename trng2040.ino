#include <SHA256.h>

SHA256 sha;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);
}

uint8_t raw_byte() {
  uint16_t a0 = analogRead(A0);   // antenna 1
  uint16_t a1 = analogRead(A1);   // antenna 2
  uint8_t led = digitalRead(2);
  
  uint8_t out = (a0 & 0x0F) ^ ((a0 >> 4) & 0x0F);
  out ^= (a1 & 0x0F) ^ ((a1 >> 4) & 0x0F);
  out ^= led;
  out ^= micros() & 0xFF;
  return out;
}

void loop() {
  uint8_t entropy[128];
  for (int i = 0; i < 128; i++) {
    entropy[i] = raw_byte();
  }
  
  sha.reset();
  sha.update(entropy, 128);
  uint8_t hash[32];
  sha.finalize(hash, 32);
  
  for (int i = 0; i < 32; i++) {
    Serial.write(hash[i]);
  }
}