import math # needed for rounding up amount of bases in bytes
import sys
def byteToFourBases(byte):
    binaryString = format(byte, 'b').rjust(8, '0') # format to string and heading 00's are removed by python and should be added again
    twobitBases = [binaryString[i:i+2] for i in range(0, 8, 2)] # list of 2 bits

    bases = ''
    for twobitBase in twobitBases:
        bases += bitsToBase(twobitBase)
    return bases

def bitsToBase(bits):
    if bits == '00':
        return 'A'
    elif bits == '01':
        return 'C'
    elif bits == '10':
        return 'T'
    elif bits == '11':
        return 'G'
    else:
        raise ValueError('Not a valid bitpair was provided') # Raise errors for invalid bitpair

def decompressDNA(dnaBytes, amountOfBases, outputFile, basesInLine = 80):
    dnaSeq = ''
    for byte in dnaBytes:
        dnaSeq += byteToFourBases(byte)
    
    # Fix padding needed for full bytes
    lastChunkLen = amountOfBases % 4 # 0 if it's a full byte
    if lastChunkLen != 0: # Only remove padding if there is padding
        print(lastChunkLen)
        dnaSeq = dnaSeq[:(4 - lastChunkLen) * -1] # Remove padding

    # Write to file
    dnaLines = [dnaSeq[i:i+basesInLine] for i in range(0, len(dnaSeq), basesInLine)] # list of 2 bits
    for line in dnaLines:
        outputFile.write(line + '\n')
    

def decompress(inputFile, outputFile, lineLength = 60):
    header = inputFile.readline().decode('utf-8')
    if header != 'dnazip file; v0; https://github.com/Bartvelp/dnazip\n':
        raise ValueError('Invalid dnazip file provided') # Raise errors for non dnazip file

    for line in inputFile:
        # The random DNA byts are always fully read so the pointer in the filehandle is always moved forward to either
        # a new FASTA header or to another 'DNAZIP START', meaning the next bytes python reads are handled as a new line, even though
        # no newline character is present before them. That is why .startswith works
        if line.decode('utf-8').startswith('DNAZIP START'): # It's a start line, read the next x bytes
            amountOfBases = int(line[14:-1]) # Remove 'DNAZIP START: ' and trailing newline
            amountOfBytes = math.ceil(amountOfBases / 4) # end is padded (with zero's)
            dnaBytes = inputFile.read(amountOfBytes) # read the DNA bytes here, also moves forward the pointer
            decompressDNA(dnaBytes, amountOfBases, outputFile, lineLength) # parse the bits and write to output file
        else: # it's likely a header line, just copy it to the output file
            outputFile.write(line.decode('utf-8'))

if __name__ == "__main__": # execute if not included and is main script
    inputF = open('{}.dnazip'.format(sys.argv[1]), 'rb')
    outputF = open('{}.out.fa'.format(sys.argv[1]), 'w')

    decompress(inputF, outputF)
    print('Done decompressing')
    inputF.close()
    outputF.close()