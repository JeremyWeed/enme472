PORT=/dev/ttyACM0
ARD=arduino:avr:uno
FOLDER=../controller

compile:
	arduino-cli compile --fqbn $(ARD) $(FOLDER)

flash:
	arduino-cli upload -p $(PORT) --fqbn $(ARD) $(FOLDER)
