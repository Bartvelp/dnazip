import math # needed for rounding up amount of bases in bytes

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

def decompressDNA(dnaBytes, lastChunkLen, outputFile):
    dnaSeq = ''
    for byte in dnaBytes:
        dnaSeq += byteToFourBases(byte)
    dnaSeq = dnaSeq[:(4 - lastChunkLen) * -1] # Remove padding
    outputFile.write(dnaSeq)

def decompress(inputFile, outputFile):
    header = inputFile.readline().decode('utf-8')
    if header != 'dnazip file; v0; https://github.com/Bartvelp/dnazip\n':
        raise ValueError('Invalid dnazip file provided') # Raise errors for invalid bitpair

    for line in inputFile:
        if line.decode('utf-8').startswith('DNAZIP START'): # It's a start line, read the next x bytes
            amountOfBases = int(line[14:-1]) # Remove 'DNAZIP START: ' and trailing newline
            amountOfBytes = math.ceil(amountOfBases / 4) # end is padded with 0's
            amountOfBasesInLastChunk = amountOfBases % 4
            dnaBytes = inputFile.read(amountOfBytes)
            decompressDNA(dnaBytes, amountOfBasesInLastChunk, outputFile) # parse the bits and write to output file
        else: # it's likely a header line, just copy it to the output file
            outputFile.write(line.decode('utf-8'))

if __name__ == "__main__": # execute if not included and is main script
    ecoliDNAzip = open('./ecoli_genome.dnazip', 'rb')
    ecoliNewOut = open('./ecoli_genome.out.fa', 'w')

    decompress(ecoliDNAzip, ecoliNewOut)
    print('Done decompressing')
    ecoliNewOut.close()
    ecoliDNAzip.close()