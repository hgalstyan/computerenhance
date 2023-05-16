import os
import sys

regtable = [['al','cl','dl','bl','ah','ch','dh','bh'],
            ['ax','cx','dx','bx','sp','bp','si','di']]

def line_to_op(line):
    line = line.replace(',', ' ')
    s1 = line.strip().split()
    s2 = [t for t in s1 if len(t.strip()) > 0]
    return s2

def op_encode(operands):
    op = operands[0]
    r  = operands[1]
    rm = operands[2]
    if op == 'mov':
        code = '100010'
        dflag = '0'
        wflag = '1' if r in regtable[1] or rm in regtable[1] else '0'
        mode = '11'
        rb  = '{0:03b}'.format(regtable[int(wflag)].index(r))
        rmb = '{0:03b}'.format(regtable[int(wflag)].index(rm))
        return int(code+dflag+wflag+mode+rmb+rb, 2).to_bytes(2, byteorder='big')
    
def op_decode(b1, b2):
    opstr = ''
    opcode = (b1 & 0b11111100) >> 2
    if opcode == 0b100010: # mov
        opstr += 'mov' + ' '
        dflag = (b1 & 0b00000010) >> 1
        wflag = b1 & 0b00000001
        o1 = regtable[wflag][(b2 & 0b00111000) >> 3]
        o2 = regtable[wflag][(b2 & 0b00000111)]
        if dflag == 0:
            o1, o2 = o2, o1
        opstr += o1
        opstr += ', '
        opstr += o2
        return opstr

def assemble(filename):
    encoded = bytearray()
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith(';') and len(line.strip()) > 0:
                if not line.startswith('bits'):
                    op = line_to_op(line)
                    encoded += op_encode(op)

def disassemble(filename):
    with open(filename, 'rb') as f:
        while (byte := f.read(2)):
            print(op_decode(byte[0], byte[1]))

if __name__ == '__main__':
    print(";" + sys.argv[2])
    print("bits 16")
    if sys.argv[1] == '-a':
        assemble(sys.argv[2])
    elif sys.argv[1] == '-d':
        disassemble(sys.argv[2])