#!/usr/bin/env python

presets = {}

presets['seventwenty'] = {
    'template': 'ffmpeg -i {input} -vf scale=-1:360 -c:v libx264 -crf 22 -c:a copy {output}'
}

presets['default'] = presets['seventwenty']