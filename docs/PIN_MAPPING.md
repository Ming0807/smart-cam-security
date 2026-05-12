# Pin Mapping

## Board

AI-Thinker ESP32-CAM

## Sensor Pins

| Function | GPIO | Direction | Notes |
|---|--:|--:|---|
| HC-SR04 TRIG | GPIO 12 | Output | Sends ultrasonic trigger pulse |
| HC-SR04 ECHO | GPIO 13 | Input | Must pass through voltage divider |
| HC-SR04 VCC | 5V | Power | Sensor usually requires 5V |
| HC-SR04 GND | GND | Ground | Shared ground with ESP32-CAM |

## SD Card Pins

| Mode | GPIOs | Conflicts |
|---|---|---|
| SD 4-bit | 2, 4, 12, 13, 14, 15 | Flash(GPIO4), Sensor(GPIO12,13) |
| SD 1-bit | 2, 14, 15 | None — frees 4, 12, 13 |

Use 1-bit mode to use flash + sensor simultaneously.

## Flash LED

| Function | GPIO | Direction | Notes |
|---|--:|--:|---|
| Flash LED | GPIO 4 | Output | Built-in white LED. Active HIGH. |

### Flash LED / SD Card Conflict

GPIO4 is also used as **SD_MMC_DATA1** in 4-bit SD card mode.
If you use both flash LED and SD card in 4-bit mode simultaneously,
SD reads/writes will fail or corrupt data.

**Solutions:**
- Use 1-bit SD mode (frees GPIO4, GPIO12, GPIO13)
- Turn flash OFF before any SD card operation
- Accept that flash and SD cannot be used at the same time in 4-bit mode

## Critical Warning

Do not connect HC-SR04 Echo directly to ESP32 GPIO.

HC-SR04 Echo is 5V. ESP32 GPIO supports 3.3V.

Use a voltage divider.

## SD Card Constraint

ESP32-CAM uses many pins for camera and SD card.

To use GPIO 12 and GPIO 13 for HC-SR04, SD card should be configured in 1-bit mode where supported.

## Do Not Change Without Review

Do not change these pins unless:

1. You verify camera pin conflicts.
2. You verify SD card mode.
3. You update this file.
4. You update firmware configuration.
