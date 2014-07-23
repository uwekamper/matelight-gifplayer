matelight-gifplayer
===================

Plays and loops an animated gif file on the [Matelight](https://github.com/jaseg/matelight) display
via the Matelight CRAP protocol.

Installation
------------

  git clone ...
  cd $cloned-directory
  virtualenv --distribute --no-site-packages .
  pip install -r requirements.txt

Usage
-----

./mategif.py HOSTNAME PATH/TO/ANIMATED.GIF

Example:
./mategif.py ml.jaseg.net gifs/flappy.gif
