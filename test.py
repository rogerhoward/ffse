#!/usr/bin/env python

import presets
import click


@click.command()
@click.option('--dir', default=False, help='Destination directory.')
@click.option('--preset', default=presets.default, help='Destination directory.')
@click.argument('file')
def initdb(dir, file):
    click.echo('Initialized the database')


if __name__ == '__main__':
    initdb()