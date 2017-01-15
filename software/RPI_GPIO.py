# Rubberfish Raspberry Pi GPIO pinouts
# all pins in board notation

# 1 - 3v3 feeds PCF8591 Vcc
# 3 - PCF8591 SDA - DtoA to voltage meter
# 5 - PCF8591 SCL - DtoA to voltage meter
# 6 - GND to PCF8591
fishHEAD = 7 # connected to BMBB head
boxHEAT = 10 # front panel switch labeled "HEAT"
fishTAIL = 11 # connected to BMBB tail
boxVENT = 12 # front panel switch labeled "VENT"
fishIsSpeaking = 13 #Reads from TL082 to see if fish is speaking
boxLIGHT = 16 # front panel switch labeled "LIGHT"
fishMotorEnable = 18 # PWM channel - controls L293 enable - aka ENTHUSIASM
