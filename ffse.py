#!/usr/bin/env python
import re
import config
import click
import subprocess
from pathlib import Path

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AbsoluteETA, AdaptiveTransferSpeed

class Encoder(object):
    def convert_subprocess(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
        for line in process.stdout:
            line = line.strip()

            if line.startswith('frame='):
                try:
                    self.frame = int(re.match(r'frame=\s*(\d+)', line).group(1))
                except:
                    pass

            self.progress()

    def progress(self):
        self.progressbar.update(int(self.status * 100))

    @property
    def filename(self):
        return Path(self.original).name

    @property
    def output(self):
        original = Path(self.original)
        new_filename = '{}_{}.{}'.format(original.stem, self.preset, self.extension)
        if self.destination:
            destination = Path(self.destination)
            return destination / new_filename
        else:
            return original.parent / new_filename


    @property
    def command(self):
        data = {'input': self.original, 'output': self.output}
        command_string = config.presets[self.preset]['template'].format(**data)
        # print('command_string: {}'.format(command_string))
        return command_string

    @staticmethod
    def _get_ffmpeg_info(path):
        process = subprocess.Popen([config.ffmpeg, "-i", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = process.communicate()
        return stdout.decode()

    @property
    def resolution(self):
        match_dict = re.search(r"\s(?P<h>\d+?)x(?P<v>\d+?)\s", self.ffmpeg_info).groupdict()
        return {key: int(match_dict[key]) for key in match_dict}

    @property
    def frame_rate(self):
        match_dict = re.search(r"\s(?P<fps>[\d\.]+?)\stbr", self.ffmpeg_info).groupdict()
        return float(match_dict["fps"])

    @property
    def duration(self):
        match_dict = re.search(r"Duration:\s(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),",
                               self.ffmpeg_info).groupdict()
        return float(match_dict["hours"])*60**2\
               + float(match_dict["minutes"])*60\
               + float(match_dict["seconds"])

    @property
    def status(self):
        value = self.frame / (self.duration * self.frame_rate)
        if value > 1:
            value = 1.0
        return value

    def __init__(self, dir, preset, file):
        self.frame = 0
        self.original = file
        self.preset = preset
        self.destination = dir
        self.extension = 'mp4'
        self.ffmpeg_info = self._get_ffmpeg_info(self.original)

    def __str__(self):
        return self.filename


@click.command()
@click.option('--dir', default=False, help='Destination directory.')
@click.option('--preset', default='default', help='Destination directory.')
@click.argument('file')
def handle(dir, preset, file):
    click.echo('Converting {} using preset "{}"'.format(file, preset))
    this_encoder = Encoder(dir, preset, file)

    print('duration: {}'.format(this_encoder.duration))
    print('frame rate: {}'.format(this_encoder.frame_rate))
    print('frames: {}'.format(this_encoder.duration * this_encoder.frame_rate))

    with ProgressBar(max_value=100) as this_encoder.progressbar:
        this_encoder.convert_subprocess()


if __name__ == '__main__':
    handle()