# Skill: HC-SR04 Sensor

## Use This Skill When

Working with ultrasonic distance detection.

## Wiring

- VCC to 5V
- GND to GND
- TRIG to GPIO 12
- ECHO to GPIO 13 through voltage divider

## Rules

- Echo must not connect directly to ESP32 GPIO.
- Add echo timeout.
- Ignore invalid readings.
- Use smoothing if values are noisy.
- Add trigger cooldown to avoid alert spam.

## Suggested Logic

1. Send 10us pulse on Trig.
2. Wait for Echo high with timeout.
3. Measure high duration.
4. Convert to cm.
5. Validate range.
6. Compare to threshold.
