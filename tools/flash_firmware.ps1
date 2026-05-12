<#
.SYNOPSIS
    Flash camera-enabled MicroPython firmware to ESP32-CAM.

.DESCRIPTION
    Erases ESP32 flash and writes LeMaRiva MicroPython camera firmware.
    Prompts for confirmation before erasing.

.PARAMETER Port
    COM port of the ESP32-CAM (e.g. COM3, COM5).

.PARAMETER FirmwarePath
    Path to the .bin firmware file.

.PARAMETER Baud
    Baud rate for flashing. Default is 460800.

.EXAMPLE
    .\tools\flash_firmware.ps1 -Port COM3 -FirmwarePath firmware_bin\micropython_camera_feeeb5ea3_esp32_idf4_4.bin

.EXAMPLE
    .\tools\flash_firmware.ps1 -Port COM5 -FirmwarePath firmware_bin\micropython_camera_feeeb5ea3_esp32_idf4_4.bin -Baud 115200
#>

param(
    [Parameter(Mandatory = $true, HelpMessage = "COM port (e.g. COM3)")]
    [string]$Port,

    [Parameter(Mandatory = $true, HelpMessage = "Path to .bin firmware file")]
    [string]$FirmwarePath,

    [Parameter(Mandatory = $false)]
    [int]$Baud = 460800,

    [Parameter(Mandatory = $false)]
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

# Validate firmware file exists
if (-not (Test-Path -LiteralPath $FirmwarePath)) {
    Write-Error "Firmware file not found: $FirmwarePath"
    exit 1
}

$firmwareSize = (Get-Item -LiteralPath $FirmwarePath).Length
Write-Host "========================================"
Write-Host " ESP32-CAM Firmware Flashing"
Write-Host "========================================"
Write-Host " Port:          $Port"
Write-Host " Firmware:      $FirmwarePath"
Write-Host " Size:          $firmwareSize bytes"
Write-Host " Baud:          $Baud"
Write-Host " Flash address: 0x1000"
Write-Host "========================================"
Write-Host ""
Write-Host "WARNING: This will ERASE the entire flash."
Write-Host "All existing data on the ESP32-CAM will be lost."
Write-Host ""

# Check esptool is available
$esptoolCheck = py -m esptool version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "esptool not found. Install it: py -m pip install esptool"
    exit 1
}

Write-Host "esptool detected OK"

# Confirmation
if (-not $Force) {
    $confirm = Read-Host "Type YES to proceed with flash erase and write"
    if ($confirm -ne 'YES') {
        Write-Host "Aborted by user."
        exit 0
    }
}
else {
    Write-Host "Force flag set. Skipping confirmation."
}

Write-Host ""
Write-Host "[1/2] Erasing flash..."
py -m esptool --chip esp32 --port $Port erase_flash
if ($LASTEXITCODE -ne 0) {
    Write-Error "Flash erase failed."
    exit 1
}
Write-Host "Flash erase complete."

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[2/2] Writing firmware..."
py -m esptool --chip esp32 --port $Port --baud $Baud write_flash -z 0x1000 $FirmwarePath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Firmware write failed."
    exit 1
}
Write-Host "Firmware write complete."

Write-Host ""
Write-Host "========================================"
Write-Host " Flash complete."
Write-Host "========================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Disconnect and reconnect the ESP32-CAM."
Write-Host "2. Open Thonny IDE."
Write-Host "3. Select the correct COM port and 'MicroPython (ESP32)' interpreter."
Write-Host "4. In REPL, run: import camera"
Write-Host "5. If no error, the firmware is ready."
