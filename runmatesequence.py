#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal
import subprocess

commands = ['./mategif.py matelight.cbrp3.c-base.org gifs/flappy.gif']

for cmd in commands:
    pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    raw_input("Press Enter to continue...")
    os.killpg(pro.pid, signal.SIGTERM)

print "Last image reached."
