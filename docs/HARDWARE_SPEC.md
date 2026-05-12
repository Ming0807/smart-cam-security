# Hardware Specification

## Main Components

| Component | Model / Requirement | Notes |
|---|---|---|
| Microcontroller | AI-Thinker ESP32-CAM | OV2640 camera module |
| Camera | OV2640 | Built into ESP32-CAM module |
| Sensor | HC-SR04 | Ultrasonic distance sensor |
| Storage | MicroSD 16GB | FAT32 |
| Power Supply | 5V 2A | Recommended minimum |
| Programming Board | ESP32-CAM-MB | Micro-USB upload and power |

## Power Requirement

ESP32-CAM can become unstable when Wi-Fi and camera are active together. Use a stable 5V power supply with at least 2A capacity.

Symptoms of weak power:

- random reboot
- brownout messages
- camera init failure
- Wi-Fi disconnect
- SD write failure

## HC-SR04 Voltage Warning

HC-SR04 Echo output is normally 5V.

ESP32 GPIO is 3.3V logic and is not 5V tolerant.

Use a voltage divider before connecting Echo to GPIO 13.

Example divider:

```text
HC-SR04 Echo
  ↓
R1 = 1kΩ
  ↓---- GPIO 13
R2 = 2kΩ
  ↓
GND
```

Alternative resistor values are acceptable if the output is reduced to about 3.3V or lower.

## SD Card

- Format as FAT32.
- Use reliable brand.
- Avoid cheap or damaged cards.
- Test mount before camera capture integration.

## Development Tools

Recommended:

- Thonny IDE
- esptool.py
- USB data cable
- Multimeter
- Breadboard
- Jumper wires
