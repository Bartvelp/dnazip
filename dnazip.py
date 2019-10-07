import argparse
import sys
import compress, decompress
# https://docs.python.org/3/library/argparse.html
# Similar to gzip's arguments
parser = argparse.ArgumentParser(description='Compress FASTA files, using 2 bits per base')
parser.add_argument('FILE', nargs='?', help='Input file name', default='stdin') # If no input is given, use stdin
parser.add_argument('-l', '--linelength', help='Characters per line', default=60, type=int) # If no input is given, use stdin
parser.add_argument('-d', '--decompress', help='Decompress file', action='store_true') # True or False Flag
parser.add_argument('-c', '--stdout', help='Write to standard output', action='store_true')
parser.add_argument('--debug', help='Show debugging statements', action='store_true')

args = parser.parse_args()

debug = args.debug
if debug:
    print('Showing debug info')

inputFilename = args.FILE

outputFilename = '' # Determined below
if args.FILE == 'stdin' or args.stdout:
    outputFilename = 'stdout'
else: # calculate output filename
    inputFilenameParts = args.FILE.split('.')
    if len(inputFilenameParts) == 1: # no extension present, add a placeholder
        inputFilenameParts.append('.txt') # This will be removed
    if args.decompress:
        outputFilename = '.'.join(inputFilenameParts[:-1]) + '.out.fa' # Remove old extension and add .fa
    else:
        outputFilename = '.'.join(inputFilenameParts[:-1]) + '.dnazip' # Remove old extension and add .dnazip

if debug:
    print('Reading from: {}'.format(inputFilename))
    print('Writing to: {}'.format(outputFilename))

if args.decompress:
    inputFile = None
    outputFile = None
    if inputFilename == 'stdin': # Do some magic to open a filehandle to stdin
        inputFile = sys.stdin.buffer # This dict has the same methods as a filehandle
    else:
        inputFile = open(inputFilename, 'rb')
    # Do the same for output
    if outputFilename == 'stdout':
        outputFile = sys.stdout
    else:
        outputFile = open(outputFilename, 'w')
    
    decompress.decompress(inputFile, outputFile, args.linelength)
    if debug:
        print('Done decompressing')
else:
    inputFile = None
    outputFile = None
    # Same thing as above
    if inputFilename == 'stdin':
        inputFile = sys.stdin
    else:
        inputFile = open(inputFilename, 'r')

    if outputFilename == 'stdout':
        outputFile = sys.stdout.buffer
    else:
        outputFile = open(outputFilename, 'wb')
    
    compress.compress(inputFile, outputFile)
    if debug:
        print('Done compressing')