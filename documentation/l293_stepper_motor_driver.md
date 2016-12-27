wiring diagram for L293d Stepper Motor Driver
======

http://www.ti.com/lit/ds/symlink/l293.pdf

Rewired to allow for the isolation of mouth

| pin | L293d | L293d | pin |
|---|---|---|---|
|  +5v  | 1,2 enable | v1 | +5v |
|  signal from op amp TL082  | 1 in | 4 in | GPIO 7 - fishHEAD |
| MOUTH to fish  | 1 out | 4 out | HEAD OUT to fish |
| gnd | GND | GND | gnd |
| gnd | GND | GND | gnd |
|   | 2 out | 3 out | TAIL to fish  |
| GPIO 13 - fishMOUTH | 2 in | 3 in | GPIO 11 - fishTAIL  |
| +12v | v2 | 3,4 enable | Rpi Board 18 - PWM |
