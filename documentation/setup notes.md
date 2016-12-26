General Notes
======
The fish wifi shows up at 10.0.0.31

I have not installed vnc. Instead, use "ssh pi@10.0.0.31"

Startup
======
/etc/init.d/fish_config.sh is started as part of the init process

bmbb_fish.py is initiated by fish_config.sh - as part of bmbb_fish.py




Set Up pyttsx
======

## pyttsx is the text-to-speech tool. ##

### Install espeak ###
sudo apt-get install python-espeak

### Install pyttsx for python3 ###

mkdir gitFiles

cd gitFiles

sudo python3 setup.py install

### Further description of the install process is at... ###

https://python-packaging.readthedocs.io/en/latest/minimal.html

There is a discussion of pyttsx for python3 at...

http://stackoverflow.com/questions/24963638/import-pyttsx-works-in-python-2-7-but-not-in-python3

## are you getting "'libruby2.1:armhf' is missing final newline" ##

https://blog.bartbania.com/raspberry_pi/files-list-file-missing-final-newline/

dpkg -c /var/cache/apt/archive/libruby2.1.deb | \
awk '{if ($6 == './'){ print '/.'; } else if \
(substr($6, length($6), 1) == '/'){print \
substr($6, 2, length($6) - 2); } else { print \
substr($6, 2, length($6) - 1);}}' > \
/var/lib/dpkg/info/libruby2.1.list
