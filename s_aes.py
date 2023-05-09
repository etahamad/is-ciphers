def substituteNibble(val, sbox):
    """Lookup table to fetch corresponding value for each nibble."""
    row = int(val[0] + val[3], 2)
    col = int(val[1] + val[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def subNib(state, sbox):
    """Substitute nibbles using S-box"""
    return [[substituteNibble('{0:04b}'.format(state[row][col]), sbox) for col in range(4)] for row in range(4)]


def shiftRow(state):
    """Shift rows as per S-AES"""
    return [state[0],
            state[1][1:] + state[1][:1],
            state[2][2:] + state[2][:2],
            state[3][3:] + state[3][:3]]


def mixCol(state):
    """Mix columns as per S-AES"""
    mul2 = lambda val: (val << 1) ^ (0x1B if (val & 0x80) else 0)
    mul4 = lambda val: mul2(mul2(val))
    mul8 = lambda val: mul2(mul4(val))
    mul9 = lambda val: mul8(val) ^ val
    mul11 = lambda val: mul9(val) ^ mul2(val)
    mul13 = lambda val: mul11(val) ^ mul2(val)
    mul14 = lambda val: mul13(val) ^ val

    state_t = [list(x) for x in zip(*state)]
    out_arr = []
    for i in range(4):
        out_col = [mul2(state_t[i][0]) ^ mul4(state_t[i][1]) ^ mul6(state_t[i][2]) ^ mul8(state_t[i][3]),
                   mul2(state_t[i][1]) ^ mul4(state_t[i][2]) ^ mul6(state_t[i][3]) ^ mul8(state_t[i][0]),
                   mul2(state_t[i][2]) ^ mul4(state_t[i][3]) ^ mul6(state_t[i][0]) ^ mul8(state_t[i][1]),
                   mul2(state_t[i][3]) ^ mul4(state_t[i][0]) ^ mul6(state_t[i][1]) ^ mul8(state_t[i][2])]
        out_arr.append(out_col)

    return [list(x) for x in zip(*out_arr)]


def keyExpansion(key):
    """Expand key using S-AES"""
    Rcon = ['10000000', '00110000', '00001100', '00000001', '10000010']  # Round constants
    sbox = [['1001', '0100', '1010', '1011'],
            ['1101', '0001', '1000', '0101'],
            ['0110', '0010', '0000', '1011'],
            ['1111', '0111', '0011', '1001']]  # substitution box

    round_keys = [key[0:4], key[4:8], key[8:12], key[12:16]]
    for i in range(4, 11):
        temp = round_keys[i-1][:]
        if (i % 4 == 0):
            temp = [temp[1], temp[2], temp[3], temp[0]]
            temp = [substituteNibble('{0:04b}'.format(int(val, 16)), sbox) for val in temp]
            temp[0] = '{0:08b}'.format(int(temp[0], 2) ^ int(Rcon[int(i/4)], 2))
        round_keys.append(['{0:02x}'.format(int(round_keys[i-4][j], 16) ^ int(temp[j], 2)) for j in range(4)])
    return round_keys


def addRoundKey(state, key):
    """XOR state and round key"""
    return [[int(state[row][col], 16) ^ int(key[row][col], 16) for col in range(4)] for row in range(4)]


def s_aes_encrypt(pt, key):
    """Encrypt plaintext using S-AES"""
    sbox = [['1001', '0100', '1010', '1011'],
            ['1101', '0001', '1000', '0101'],
            ['0110', '0010', '0000', '1011'],
            ['1111', '0111', '0011', '1001']]  # substitution box

    pt = [pt[i:i+2] for i in range(0, len(pt), 2)]
    pt = [[int(val, 16) for val in row] for row in zip(*[iter(pt)]*4)]
    key = [key[i:i+2] for i in range(0, len(key), 2)]
    key = [[int(val, 16) for val in row] for row in zip(*[iter(key)]*4)]

    round_keys = keyExpansion(['{0:08b}'.format(val) for val in key])

    state = addRoundKey(pt, key)
    for i in range(1, 10):
        state = subNib(state, sbox)
        state = shiftRow(state)
        state = mixCol(state)
        state = addRoundKey(state, [['{0:02x}'.format(int(val, 2)) for val in row] for row in round_keys[i]])

    state = subNib(state, sbox)
    state = shiftRow(state)
    state = addRoundKey(state, [['{0:02x}'.format(int(val, 2)) for val in row] for row in round_keys[10]])
    ct = ''.join([''.join(['{0:02x}'.format(val) for val in row]) for row in state])
    return ct
