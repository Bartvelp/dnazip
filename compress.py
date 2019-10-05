def fourBasesToByte(bases):
    byteString = ''
    for base in bases:
        byteString += baseToBits(base)
    return int(byteString, 2) # return a 8 bit integer

def baseToBits(base):
    if base == 'A':
        return '00'
    elif base == 'C':
        return '01'
    elif base == 'T':
        return '10'
    elif base == 'G':
        return '11'
    else:
        raise ValueError('Not a valid base was provided') # Raise errors for invalid chars

def compressDNA(dnaSeq, outputFile):
    lengthDNA = len(dnaSeq)
    outputFile.write('DNAZIP START: {}\n'.format(lengthDNA).encode('utf-8')) # Add amount of BP's to header for deflating
    dnaChunks = [dnaSeq[i:i+4] for i in range(0, lengthDNA, 4)] # Create a list of chunks of 4 BP https://stackoverflow.com/a/9475354
    if len(dnaChunks[-1]) != 4:
        dnaChunks[-1] = dnaChunks[-1].ljust(4, 'A') # Pad last DNA seq with A's https://stackoverflow.com/a/5676676
    for chunk in dnaChunks: # every chunk is guaranteed to be 4 bases (1 byte)
        curByte = fourBasesToByte(chunk)
        outputFile.write(bytearray([curByte])) # write compressed byte to file
    # Done writing DNA, write newline so new start always is on a new line
    outputFile.write('\n'.encode('utf-8'))

def compress(inputFile, outputFile):
    outputFile.write('dnazip file; v0; https://github.com/Bartvelp/dnazip\n'.encode('utf-8')) # Encode header because of binary mode
    currentDNAseq = '' # Accumulator to increase effiency
    MAX_DNA_SEQ_LEN = 1 * 1048576 # max size to keep in memory for currentDNAseq (1,048,576 bytes in MB)
    for line in inputFile:
        if line.startswith('>'): # It's a header line, don't bother with it
            if (len(currentDNAseq) > 0): # Need to finish writing DNA before starting to write new header
                compressDNA(currentDNAseq, outputFile)
                currentDNAseq = '' # reset currentDNAseq
            outputFile.write(line.encode('utf-8')) # copy header to output
            
        else: # Not a header line
            line = line.strip() # remove newlines
            ratioDNA = (line.count('A') + line.count('C') + line.count('T') + line.count('G')) / len(line)
            if ratioDNA != 1:
                raise ValueError('Ratio DNA not 1 for {}'.format(line))
            currentDNAseq += line
            if (len(currentDNAseq) > MAX_DNA_SEQ_LEN):
                compressDNA(currentDNAseq, outputFile)
                currentDNAseq = '' # reset currentDNAseq
    # done with every line, check if anything is left in the buffer
    if (len(currentDNAseq) > 0):
        compressDNA(currentDNAseq, outputFile)


if __name__ == "__main__": # execute if not included and is main script
    ecoliFasta = open('./ecoli_genome.fa', 'r')
    ecoliDNAzip = open('./ecoli_genome.dnazip', 'wb')

    compress(ecoliFasta, ecoliDNAzip)
    print('Done compressing')
    ecoliFasta.close()
    ecoliDNAzip.close()