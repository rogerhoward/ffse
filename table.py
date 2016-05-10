#!/usr/bin/env python
import re
import config
import click
import subprocess
from pathlib import Path


from terminaltables import AsciiTable
table_data = [
    ['row1 column1', 'row1 column2'],
    ['row2 column1', 'row2 column2']
]
table = AsciiTable(table_data, 'title')
table.inner_heading_row_border = False
print(table.table)