import sys
import itertools

def makeDictOfByteOptions():
    bases = 'ACTG'
    products = list(itertools.product(bases, repeat=4)) # https://docs.python.org/3/library/itertools.html#itertools.product
    byteOptions = {}
    i = 0
    for baseProduct in products:
        byteOptions[''.join(baseProduct)] = i
        i += 1
    return byteOptions # { 'AAAA': 0, 'AAAC': 1 etc.

byteOptions = makeDictOfByteOptions()

def compressDNA(dnaSeq, outputFile):
    lengthDNA = len(dnaSeq)
    outputFile.write('DNAZIP START: {}\n'.format(lengthDNA).encode('utf-8')) # Add amount of BP's to header for deflating
    lastByteLen = len(dnaSeq) % 4 # 0 if full
    if lastByteLen: # 1 2 or 3
        dnaSeq += 'A' * (4 - lastByteLen) # Pad with A's to a full byte
    byteBuffer = [byteOptions[dnaSeq[i:i+4]] for i in range(0, len(dnaSeq), 4)] # transform bases string into list of 8 bit ints
    outputFile.write(bytearray(byteBuffer)) # write compressed bytes to file

def compress(inputFile, outputFile, MAX_DNA_SEQ_LEN = 10 * 1048576): # max size to keep in memory for dnaBuffer (1,048,576 bytes in MB)
    outputFile.write('dnazip file; v0.1; https://github.com/Bartvelp/dnazip\n'.encode('utf-8')) # Encode header because of binary mode
    dnaBuffer = '' # Accumulator to increase effiency

    for line in inputFile:
        if line.startswith('>'): # It's a header line, don't bother with it
            if (len(dnaBuffer) > 0): # Need to finish writing DNA before starting to write new header
                compressDNA(dnaBuffer, outputFile)
                dnaBuffer = '' # reset dnaBuffer
            outputFile.write(line.encode('utf-8')) # copy header to output
            
        else: # Not a header line
            line = line.strip().upper() # remove newlines and convert to uppercase
            ratioDNA = (line.count('A') + line.count('C') + line.count('T') + line.count('G')) / len(line) if len(line) > 0 else 0 # Line length can be zero
            
            if ratioDNA == 1: # It's a line fully composed of ACTG
                dnaBuffer += line
                if (len(dnaBuffer) > MAX_DNA_SEQ_LEN): # Buffer is full, clean it
                    compressDNA(dnaBuffer, outputFile)
                    dnaBuffer = '' # reset dnaBuffer
            else: # This line contains something else than ACTG and isn't a header? (Maybe N's)
                if (len(dnaBuffer) > 0): # If anything is the buffer write it
                    compressDNA(dnaBuffer, outputFile)
                    dnaBuffer = '' # reset dnaBuffer
                outputFile.write(line.encode('utf-8') + '\n'.encode('utf-8')) # copy unknown line to output, and readd the stripped newline
    # done with every line, check if anything is left in the buffer
    if (len(dnaBuffer) > 0):
        compressDNA(dnaBuffer, outputFile)


if __name__ == "__main__": # execute if not included and is main script
    inputF = open('{}.fa'.format(sys.argv[1]), 'r')
    outputF = open('{}.dnazip'.format(sys.argv[1]), 'wb')

    compress(inputF, outputF)
    print('Done compressing')
    inputF.close()
    outputF.close()