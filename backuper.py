#!/usr/bin/env python3

# Adaptation script for 7-zip(win) from 'A Byte of Python' book
# Backup files to one compressed file.
# Only for Windows, using external software

import os
import time

# 0. Archive type
# 7z, xz, split, zip, gzip, bzip2, tar

ar = '7z'

# 1. The files and directories to be backed up are
# specified in a list.
source = ['d:\\Python\\Pytozagadka\Pytozadania']

# 2. The backup must be stored in a
# main backup directory

target_dir = 'd:\\Python\\Pytozagadka'

# Create target directory if it is not present
if not os.path.exists(target_dir):
    os.mkdir(target_dir)  # make directory

# 3. The files are backed up into a zip file.
# 4. The current day is the name of the subdirectory
# in the main directory.
today = target_dir + os.sep + time.strftime('%Y%m%d')
# The current time is the name of the zip archive.
now = time.strftime('%H%M%S')

# The name of the zip file
target = today + os.sep + now + '.' + ar

# Create the subdirectory if it isn't already there
if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)

# 5. We use the zip command to put the files in a zip archive
zip_command = 'c:\\"Program Files"\\7-Zip\\7z.exe a -t{0} {1} {2}'.format(ar, target,
                                      ' '.join(source))

# Run the backup
print('Zip command is:')
print(zip_command)
print('Running:')
if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')
