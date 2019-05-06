PORT=/dev/ttyACM0
ARD=arduino:avr:uno
FOLDER=../controller
MOTOR_LIB=

compile:
	arduino-cli compile --fqbn $(ARD) $(FOLDER)

flash:
	arduino-cli upload -p $(PORT) --fqbn $(ARD) $(FOLDER)

install-lib:
	arduino-cli lib install "Adafruit Motor Shield V2 Library"
