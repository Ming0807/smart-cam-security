# Flashing Guide — Windows

## Prerequisites

### Hardware

- AI-Thinker ESP32-CAM with ESP32-CAM-MB programmer board
- Micro-USB data cable (not charge-only)
- 5V 2A power supply recommended

### Software

Install the following on Windows:

```powershell
# Install esptool
py -m pip install esptool

# Verify installation
py -m esptool version
```

Install Thonny IDE from https://thonny.org/

## Step 1: Download Firmware

Download the LeMaRiva camera-enabled MicroPython firmware from:

https://github.com/lemariva/micropython-camera-driver

- Navigate to the `firmware/` directory in the repository.
- Download `micropython_camera_feeeb5ea3_esp32_idf4_4.bin`.
- Place it in the `firmware_bin/` folder of this project.

## Step 2: Identify COM Port

1. Connect the ESP32-CAM-MB to your PC via USB.
2. DO NOT attach the ESP32-CAM to the programmer board yet — first check the port.
3. Open **Device Manager** (press Win+X, select Device Manager).
4. Expand **Ports (COM & LPT)**.
5. Note the COM port number (e.g. `COM3`, `COM5`).

If no COM port appears:
- The USB cable may be charge-only. Try a known data cable.
- Install CP210x or CH340 USB-to-UART drivers for your programmer board.

6. Attach the ESP32-CAM to the programmer board.
7. The same COM port should still appear. If it disappears, the board may be shorted or faulty.

## Step 3: Flash Firmware

Use the PowerShell flashing script:

```powershell
.\tools\flash_firmware.ps1 -Port COM3 -FirmwarePath firmware_bin\micropython_camera_feeeb5ea3_esp32_idf4_4.bin
```

Replace `COM3` with your actual COM port.

Optional: use a slower baud rate if flashing fails:

```powershell
.\tools\flash_firmware.ps1 -Port COM3 -FirmwarePath firmware_bin\micropython_camera_feeeb5ea3_esp32_idf4_4.bin -Baud 115200
```

The script will:
1. Verify `esptool` is installed.
2. Display firmware details and a warning.
3. Ask you to type `YES` to confirm.
4. Run `erase_flash` to wipe the device.
5. Run `write_flash` at address `0x1000`.

## Step 4: Verify in Thonny

1. Disconnect and reconnect the ESP32-CAM USB cable.
2. Open **Thonny IDE**.
3. Bottom-right corner: click the interpreter selector, choose **MicroPython (ESP32)**.
4. Select the correct COM port.
5. Click **Stop/Restart backend** (red stop button) to connect.
6. You should see the MicroPython REPL prompt (`>>>`).

In the REPL, run:

```python
import camera
```

Expected result: no error.

If you see `ImportError: no module named camera`, the wrong firmware was flashed. Try again with the correct `.bin` file.

## Step 5: Test Camera

```python
import camera
camera.init()
camera.capture()
```

Expected: camera initializes and captures without error.

Then run the Phase 1 validation:

```python
import main
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `esptool` not found | `py -m pip install esptool` |
| COM port not found | Check cable, install CP210x/CH340 driver |
| Flash erase fails | Press and hold BOOT button while connecting, then release |
| Flash write fails | Lower baud rate with `-Baud 115200` |
| REPL shows garbled text | Reconnect, check baud rate in Thonny (115200) |
| `import camera` fails | Wrong firmware flashed — verify file source |
| Camera init reboots | Use 5V 2A power, check ribbon cable |

See `docs/TROUBLESHOOTING.md` for more details.
