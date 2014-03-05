#!/bin/sh

#This one can be used in loops, e.g. for i in {1..25}; do ./pwgen.sh; done

LANG=C; tr -cd "[:upper:][:alnum:][:punct:]" < /dev/random | head -c 16 | xargs -0; LANG=en_US.UTF-8
