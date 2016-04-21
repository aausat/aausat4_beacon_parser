import re
import binascii
import parser
import config

f = open('gmsk.bin', 'rb')
raw = f.read()
f.close()

bits = ''.join([chr(int(int(b.encode('hex'),16))+48) for b in raw])
 

#print bits
#bits = bits[334000:334080+500]

result = re.search("(01001111010110100011010001000011)(.{24})(.{2000})", bits)
#print result.group(3)

hex_str = hex(int(result.group(3),2))[2:-1] # 2 for at fjerne 0x,-1 fordi der var et 'L'?
print result.group(2)
print hex(int(result.group(2),2))

qth = (0,0,0)
config = config.Config()
parser = parser.Parser(qth, config)
parser.parse_data(binascii.a2b_hex(hex_str), False)
