#!/usr/bin/env python
import re
import click
import subprocess

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