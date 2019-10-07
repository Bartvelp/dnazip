import itertools
def makeListOfByteOptions():
    bases = 'ACTG'
    products = list(itertools.product(bases, repeat=4)) # https://docs.python.org/3/library/itertools.html#itertools.product
    baseOptions = []
    for baseProduct in products:
        baseOptions.append(''.join(baseProduct)) # 'AAAA', 'AAAC' etc.
    byteOptions = []
    for option in baseOptions:
        bits = option\
            .replace('A', '00')\
            .replace('C', '01')\
            .replace('T', '10')\
            .replace('G', '11')
        byteOptions.append([bytes([int(bits, 2)]), option.encode('utf-8')])
    return byteOptions # [[0, b'AAAA'], [1, b'AAAC'], etc.

byteOptions = makeListOfByteOptions()
inputf = open('ecoli_genome.dnazip', 'rb')
inputf.readline()
inputf.readline()
inputf.readline()
dnabytes = inputf.read(1160413)
for option in byteOptions:
    dnabytes = dnabytes.replace(option[0], option[1])

print(dnabytes.decode())
inputf.close()