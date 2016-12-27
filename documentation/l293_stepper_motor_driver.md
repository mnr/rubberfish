wiring diagram for L293d Stepper Motor Driver
======

Rewired to allow for the isolation of mouth

| pin | L293d | L293d | pin |
|---|---|---|---|
|  control from op-amp  | 1,2 enable | v1 | +5v |
|   | 1 in | 4 in | GPIO 7 - fishHEAD |
|   | 1 out | 4 out | HEAD OUT to fish |
| gnd | GND | GND | gnd |
| gnd | GND | GND | gnd |
| MOUTH to fish  | 2 out | 3 out | TAIL to fish  |
| GPIO 13 - fishMOUTH | 2 in | 3 in | GPIO 11 - fishTAIL  |
| +12v | v2 | 3,4 enable | Rpi Board 18 - PWM |
