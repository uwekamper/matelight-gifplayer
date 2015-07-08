matelight-gifplayer
===================

Plays and loops an animated gif file on the [Matelight](https://github.com/jaseg/matelight) display
via the Matelight CRAP protocol.

Installation
------------

```
git clone https://github.com/uwekamper/matelight-gifplayer.git
cd matelight-gifplayer
virtualenv --distribute --no-site-packages .
source bin/activate
pip install -r requirements.txt
```

Usage
-----

```
cd matelight-gifplayer
source bin/activate
./mategif.py HOSTNAME PATH/TO/ANIMATED.GIF
```
Example:
```
./mategif.py ml.jaseg.net gifs/flappy.gif
```
