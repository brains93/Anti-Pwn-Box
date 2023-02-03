#include "FastLED.h"

#define LED_PIN 2
#define NUM_LEDS 30
#define BRIGHTNESS 255
#define LED_TYPE WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {
  for(int j = 0; j < NUM_LEDS; j++) {
    leds[j] = CHSV((j + millis() / 10) % 256, 255, 255);
  }
  FastLED.show();
  delay(10);
}
