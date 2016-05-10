#!/usr/bin/env python
FFMPEG_PATH = '/usr/local/bin/ffmpeg'
presets = {}

"""
Presets can contain the following named substitutions:
    in:  the input filepath
    out: the output filepath
"""

presets['threesixty'] = {
    'template': '-i {in} -y -vf scale=-1:360 -c:v libx264 -crf 22 -c:a copy {out}',
    'extension': 'mp4',
    'description': '',
}

presets['seventwenty'] = {
    'template': '-i {in} -y -vf scale=-1:720 -c:v libx264 -crf 22 -c:a copy {out}',
    'extension': 'mp4',
    'description': '',
}

presets['seventwentyshort'] = {
    'template': '-i {in} -y -vf scale=-1:360 -ss 5 -t 10 -c:v libx264 -crf 22 -c:a copy {out}',
    'extension': 'mp4',
    'description': '',
}

presets['default'] = presets['threesixty']