#!/usr/bin/env python
import re
import click
import subprocess

from pathlib import Path
from terminaltables import AsciiTable
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AbsoluteETA, AdaptiveTransferSpeed

import config
from utils import colorize as clrz


class Encoder(object):
    def convert(self):
        """
        Actually runs the encoder.
        Currently uses Subprocess synchronously, but may switch to sh and Celery.
        """
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
        """
        Updates Encoders progressbar display.
        """
        if int(self.frame) > self.frames:
            self.progressbar.update(int(self.frames))
        else:
            self.progressbar.update(int(self.frame))


    @property
    def filename(self):
        """
        Filename of input file.
        """
        return Path(self.original).name

    @property
    def output(self):
        """
        Absolute path to output file.
        """
        original = Path(self.original)
        data = {'stem': original.stem, 'preset': self.preset_name, 'ext': self.preset['extension']}
        new_filename = '{stem}_{preset}.{ext}'.format(**data)
        if self.destination:
            destination = Path(self.destination)
            return str(destination / new_filename)
        else:
            return str(original.parent / new_filename)

    @property
    def command(self):
        """
        Returns fully formatted command line string for processing input
        file according to the selected preset.
        """
        data = {'in': self.original, 'out': self.output}
        options_string = self.preset['template'].format(**data)
        command_string = '{} {}'.format(config.FFMPEG_PATH, options_string)
        return command_string

    @property
    def frames(self):
        """
        Returns number of frames in the input file, for showing progress.
        Value is calculated from duration and framerate retrieved from
        result of _get_ffmpeg_info()
        """
        return int(self.duration * self.frame_rate)

    @property
    def resolution(self):
        """
        Returns pixel dimensions of input file as a tuple.
        Resolution extracted from result of _get_ffmpeg_info()
        """
        match_dict = re.search(r"\s(?P<h>\d+?)x(?P<v>\d+?)\s", self.ffmpeg_info).groupdict()
        return {key: int(match_dict[key]) for key in match_dict}

    @property
    def frame_rate(self):
        """
        Returns framerate of input file as a float number of frames per second.
        Framerate extracted from result of _get_ffmpeg_info()
        """
        match_dict = re.search(r"\s(?P<fps>[\d\.]+?)\stbr", self.ffmpeg_info).groupdict()
        return float(match_dict["fps"])

    @property
    def duration(self):
        """
        Returns length of input file as a float number of seconds.
        Duration extracted from result of _get_ffmpeg_info()
        """
        match_dict = re.search(r"Duration:\s(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),",
                               self.ffmpeg_info).groupdict()
        return float(match_dict["hours"])*60**2\
               + float(match_dict["minutes"])*60\
               + float(match_dict["seconds"])

    @property
    def status(self):
        """
        Returns output of ffmpeg -i command, providing basic ffmpeg metadata.
        Can be optimized and improved, but works for now.
        """
        try:
            value = self.frame / (self.duration * self.frame_rate)
            if value > 1:
                value = 1.0
            return value
        except:
            return 0.0

    @staticmethod
    def _get_ffmpeg_info(path):
        """
        Returns output of ffmpeg -i command, providing basic ffmpeg metadata.
        Can be optimized and improved, but works for now.
        """
        process = subprocess.Popen([config.FFMPEG_PATH, "-i", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = process.communicate()
        result = stdout.decode()
        return result

    def _get_print_info(self):
        """
        Returns console-formatted table showing essential values to end user.
        """
        table_data = [
            [clrz('source', 'cyan'), clrz(self.original, 'white')],
            # [clrz('source', 'cyan'), click.style(self.original, fg='green', blink=True, bold=True)],
            [clrz('output', 'cyan'), clrz(self.output, 'white')],
            [clrz('preset', 'cyan'), clrz(self.preset_name, 'magenta')],
            [clrz('duration', 'cyan'), clrz(str(self.duration), 'red')],
            [clrz('framerate', 'cyan'), clrz(str(self.frame_rate), 'red')],
            [clrz('frames', 'cyan'), clrz(str(int(self.duration * self.frame_rate)), 'red')],
        ]

        table = AsciiTable(table_data, clrz(' FFSE - the FFS Encoder ', 'yellow'))
        table.inner_heading_row_border = False
        return table.table

    def __init__(self, dir, preset, file):
        """
        Instance constructor for Encoder class.
        """
        self.frame = 0
        self.original = file
        self.preset_name = preset
        self.preset = config.presets[self.preset_name]
        self.destination = dir
        self.ffmpeg_info = self._get_ffmpeg_info(self.original)

    def __str__(self):
        return self.filename


# Setup command line options using Python Click
@click.command()
@click.option('--dir', default=False, help='Destination directory.')
@click.option('--preset', default='default', help='Destination directory.')
@click.argument('file')
def handle(dir, preset, file):
    # Initialize this_encoder instance
    this_encoder = Encoder(dir, preset, file)

    # Display info table for command line users
    print(this_encoder._get_print_info())

    # Haven't settled on a ProgressBar format yet, so leaving a couple options here
    widgets = [ETA(), ' ', Timer(), Bar('>'), ' ', ' #', Counter(), ' ' , Percentage(), ' ', ReverseBar('<') ]
    widgets = [ETA(), ' ', ' #', Counter(), ' of {}'.format(this_encoder.frames) , '  ', Percentage(), Bar('>'), ]

    # Initialize ProgressBar as an instance attribute of this_encoder
    with ProgressBar(max_value=this_encoder.frames, widgets=widgets) as this_encoder.progressbar:
        this_encoder.convert()


if __name__ == '__main__':
    handle()