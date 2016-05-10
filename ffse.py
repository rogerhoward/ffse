#!/usr/bin/env python
import re
import click
import subprocess

from pathlib import Path
from terminaltables import AsciiTable
from progressbar import ProgressBar

import config
from utils import colorize as clrz


class Encoder(object):
    def convert(self):
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
            return str(destination / new_filename)
        else:
            return str(original.parent / new_filename)

    @property
    def command(self):
        data = {'input': self.original, 'output': self.output}
        command_string = config.presets[self.preset]['template'].format(**data)
        return command_string

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

    @staticmethod
    def _get_ffmpeg_info(path):
        process = subprocess.Popen([config.ffmpeg, "-i", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = process.communicate()
        return stdout.decode()

    def _get_print_info(self):
        table_data = [
            [clrz('source', 'cyan'), clrz(self.original, 'white')],
            [clrz('output', 'cyan'), clrz(self.output, 'white')],
            [clrz('preset', 'cyan'), clrz(self.preset, 'magenta')],
            [clrz('duration', 'cyan'), clrz(str(self.duration), 'red')],
            [clrz('framerate', 'cyan'), clrz(str(self.frame_rate), 'red')],
            [clrz('frames', 'cyan'), clrz(str(int(self.duration * self.frame_rate)), 'red')],
        ]
        table = AsciiTable(table_data, ' FFSE - the FFS Encoder ')
        table.inner_heading_row_border = False
        return table.table

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

    with ProgressBar(max_value=100) as this_encoder.progressbar:
        print(this_encoder._get_print_info())
        this_encoder.convert()


if __name__ == '__main__':
    handle()