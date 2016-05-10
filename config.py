#!/usr/bin/env python
FFMPEG_PATH = '/usr/local/bin/ffmpeg'
presets = {}

presets['seventwenty'] = {
    'template': '-i {in} -y -vf scale=-1:360 -c:v libx264 -crf 22 -c:a copy {out}'
}

presets['seventwentyshort'] = {
    'template': '-i {in} -y -vf scale=-1:360 -ss 5 -t 10 -c:v libx264 -crf 22 -c:a copy {out}'
}

presets['default'] = presets['seventwenty']