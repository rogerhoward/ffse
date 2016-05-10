#!/usr/bin/env python
ffmpeg = '/usr/local/bin/ffmpeg'
presets = {}

presets['seventwenty'] = {
    'template': '/usr/local/bin/ffmpeg -i {input} -y -vf scale=-1:360 -c:v libx264 -crf 22 -c:a copy {output}'
}

presets['seventwentyshort'] = {
    'template': '/usr/local/bin/ffmpeg -i {input} -y -vf scale=-1:360 -ss 5 -t 10 -c:v libx264 -crf 22 -c:a copy {output}'
}

presets['default'] = presets['seventwenty']