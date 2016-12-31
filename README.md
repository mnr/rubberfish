rubberfish
==========

## Embedding a Raspberry Pi into a Big Mouth Billy Bass

Before you read any further, it's important to review this excellent write-up titled [Installing Linux on a Dead Badger: User's Notes](http://strangehorizons.com/non-fiction/articles/installing-linux-on-a-dead-badger-users-notes/) by Lucy A. Snyder. If I am asked, I will name this as the source of my inspiration.

*The Truth ... I was well into my fish conversion before my friend [David D. Levine](http://www.daviddlevine.com/) pointed out this article.*

This github project documents my progress on connecting a raspberry pi to a [Big Mouth Billy Bass](https://en.wikipedia.org/wiki/Big_Mouth_Billy_Bass).

## Other Bass Masters
* In 2009, [Steve Ravet](http://mbed.org/cookbook/Big-Mouth-Billy-Bass) connected an ARM mbed to Billy.
* In 2016, [Brian Kane connected a fish to Amazon Alexa](https://www.facebook.com/hdadd/videos/10157576067105265/).

## Problems I've solved

### How to access and drive the fish motors
I've documented my experiments at [gutting the fish](https://github.com/mnr/rubberfish/wiki/Gutting-the-fish) and connecting to a [motor driver](https://github.com/mnr/rubberfish/wiki/l293_stepper_motor_driver.md). **Quick take-away:** don't be afraid to cut your fish apart (they're only $5 at GoodWill) and don't try to drive the fish directly from the Raspberry Pi GPIO. Instead, use a motor driver such as the L293.

### How to supply power
A fresh-off-the-shelf fish uses four D-cells and seems to be happiest if supplied with somewhere between six and ten volts. It uses small motors to activate the mouth, head and tail and can pull enough current to burn out a TIP31 power transistor. A Raspberry Pi *really* wants 5 volts at 2 amps. Plus, it's a bad idea to drive motors directly from the Raspberry Pi GPIO.

I've tried a lot of options, finally settling on using a full-blown ATX power supply. [Here are full details](https://github.com/mnr/rubberfish/wiki/Power-Supplies.md).

### How to sync mouth movements to audio
Whoo-boy. This was a tough nut to crack. I've tried timing text to speech and I've tried [Watson](https://www.ibm.com/watson/developercloud/text-to-speech.html). I'm currently using a hardware solution. [Here's a bunch of details](https://github.com/mnr/rubberfish/wiki/textToSpeech.md).

### How to convert text to speech
This is an ongoing problem. I started with software solutions, flipped to the Watson web service and may switch back to running something locally. I don't have this solved yet.

### How to control the front panel meter
working on this...[link to here](https://github.com/mnr/rubberfish/wiki/front_panel.md)

### How to read the front panel switches
working on this...

### How to reduce audio noise
working on this...

### Electrical connections between the fish and the RPi
working on this...
