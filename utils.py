#!/usr/bin/env python
from colorclass import Color


def colorize(string, color):
    opentag = '{' + color + '}'
    closetag = '{/' + color + '}'
    return Color('{}{}{}'.format(opentag, string, closetag))
