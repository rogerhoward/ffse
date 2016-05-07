#!/usr/bin/env python

import config
import click
import os
import subprocess

class Encoder(object):

    def convert_subprocess(self):
        print('convert_subprocess: {}'.format(self.command))
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
        for line in process.stdout:
            print(line)

    @property
    def filename(self):
        return os.path.basename(self.original)

    @property
    def output(self):
        new_filename = '{}_{}.{}'.format(os.path.splitext(self.filename)[0], self.preset, self.extension)
        if dir:
            return os.path.join(self.destination, new_filename)
        else:
            return os.path.join(os.path.dirname(self.original), new_filename)

    @property
    def command(self):

        data = {'input': self.original, 'output': self.output}
        command_string = config.presets[self.preset]['template'].format(**data)
        print('command_string: {}'.format(command_string))

        return command_string

    def __init__(self, dir, preset, file):
        print(dir, preset, file)
        self.original = file
        self.preset = preset
        self.destination = dir
        self.extension = 'mp4'
        print('init complete')

    def __str__(self):
        return self.original
        # return '{} -> {}'.format(self.filename, os.path.basename(self.output))



@click.command()
@click.option('--dir', default=False, help='Destination directory.')
@click.option('--preset', default='default', help='Destination directory.')
@click.argument('file')
def handle(dir, preset, file):
    click.echo('Converting {} using preset "{}"'.format(file, preset))
    this_encoder = Encoder(dir, preset, file)
    print('this_encoder: {}'.format(this_encoder))
    print('this_encoder.output: {}'.format(this_encoder.output))
    print('this_encoder.command: {}'.format(this_encoder.command))
    this_encoder.convert_subprocess()



if __name__ == '__main__':
    handle()