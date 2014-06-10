# -*- encoding: utf-8 -*-
r'''
This program patches xp.exe to be able to handle the new 
SHELXL commands RIGU and ABIN.
The program is compatible with Python version 2.3.5 up to 3.4.1.
Feel free to do anything you like with this code.

Use it as "c:\bn\python\python.exe xp_patch.py c:\bn\SXTL\xp.exe"
The original executable will be backed up as "xp.exe.bak"

Daniel Kratzert
dkratzert@gmx.de
'''
import shutil
import sys


try:
    filename = sys.argv[1]
except(IndexError):
    print('Please give the xp ececutable as argument.')
    print('\nfor exmple:\nc:\\bn\\SXTL>xppatch xp.exe')
    sys.exit()

def backup_file(filename):
    try:
        shutil.copyfile(filename, filename + '.bak')
    except(IOError):
        print(('Unable to make backup file from {}.'.format(filename)))
        sys.exit(-1)

try:
    f = open(filename, 'rb+')
except(IOError):
    print('can not open file', filename)
    sys.exit()

binary = f.read()
version = 'XP - Interactive Molecular Graphics'
xp = binary.find(version.encode())
absacta = binary.find('ABSCACTAAFLS'.encode())  # need this as anchor, because
                                                # there are a lot of TIME in xp
hope = binary.find('HOPE'.encode(), absacta + 1)
time = binary.find('TIME'.encode(), absacta + 1)


if xp == -1 or xp < 1000: # don't patch myself
    print('This is not "{}"'.format(version))
    sys.exit()

if hope == -1:
    print('File seems already be patched.')
    sys.exit()

backup_file(filename)


f.seek(hope, 0)
com = f.read(4)
command = com.decode('ascii')
if command == 'HOPE':
    f.seek(hope, 0)
    f.write('RIGU'.encode()) # patch rigu
    print(('RIGU successfully patched'))
else:
    print('no HOPE to patch found')


f.seek(time, 0)
com = f.read(4)
command = com.decode('ascii')
if command == 'TIME':
    f.seek(time, 0)
    f.write('ABIN'.encode()) # patch abin
    print(('ABIN successfully patched'))
else:
    print('no TIME to patch found')


