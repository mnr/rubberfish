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
Whoo-boy. This was a tough nut to crack. I've tried timing text to speech and I've tried [Watson](https://www.ibm.com/watson/developercloud/text-to-speech.html). I'm currently using a hardware solution. [Here's a bunch of details](https://github.com/mnr/rubberfish/wiki/syncMouthToAudio.md).

### How to convert text to speech
This is an ongoing problem. I started with software solutions, flipped to the Watson web service and may switch back to running something locally. I don't have this solved yet.

### How to control the front panel meter
The front panel includes an analog voltage meter. It's an unreliable narrator controlled by the AtoD module which is controlled by software. It means what I want it to mean. [Here's how it works](https://github.com/mnr/rubberfish/wiki/front_panel.md)

### How to read the front panel switches
This is easy. I'm just feeding 3.5 volts through the switches into the GPIO. [Here's how it works](https://github.com/mnr/rubberfish/wiki/front_panel.md)


### How to reduce audio noise
The Raspberry Pi is electronically noisy. I've improved things by installing a separate audio amplifier and isolating the power to that amplifier. I still hear chatter every time the Raspberry Pi accesses the internet. It's kind of cute. [Here's how it works](https://github.com/mnr/rubberfish/wiki/Audio.md)

### Using the web camera
I'm currently using an old web cam, connected via USB. Lots of work to be done. [Here's what I have so far](https://github.com/mnr/rubberfish/wiki/cameraAndVision.md)

### Electrical connections between the fish and the RPi
I've built a box that contains the Raspberry Pi, electronics, fish and webcam. The fish and webcam are attached to the lid, which slides out of the base. It's not ideal, but in order to take the lid off to access the electronics, the fish and webcam need to be disconnected from the guts. [I've used connectors to do this](https://github.com/mnr/rubberfish/wiki/FishtoDB9pinout.md).

## Other stuff

### Documenting the Raspberry Pi GPIO
[look here](https://github.com/mnr/rubberfish/wiki/gpio_pinout.md)

### Other setup Notes
[Stuff to keep track of](https://github.com/mnr/rubberfish/wiki/setupNotes.md)
