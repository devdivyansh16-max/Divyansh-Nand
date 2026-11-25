#!/usr/bin/env python3
"""Two-pass Hack assembler. Usage: python assembler.py File.asm [K]
Implements all three K-based features (symbols.txt, error messages, duplicate-label warning)."""
import sys, os

COMP = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','!D':'0001101',
 '!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111','A+1':'0110111','D-1':'0001110',
 'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111','D&A':'0000000','D|A':'0010101',
 'M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010','D+M':'1000010',
 'D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
DEST = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()

def assemble(path, k=None):
    symbols = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
    symbols.update({f'R{i}': i for i in range(16)})
    predefined = set(symbols)
    lines = []  # (line_number, instruction)
    errors, warnings = [], []
    # ---- First pass: labels ----
    addr = 0
    with open(path) as f:
        for n, raw in enumerate(f, 1):
            s = clean(raw)
            if not s: continue
            if s.startswith('('):
                if not s.endswith(')') or len(s) < 3:
                    errors.append(f'Line {n}: invalid label'); continue
                name = s[1:-1]
                if name in symbols:
                    warnings.append(f'Warning: Line {n}: label ({name}) already defined')
                else:
                    symbols[name] = addr
            else:
                lines.append((n, s)); addr += 1
    # ---- Second pass: translate ----
    out, nxt = [], 16
    for n, s in lines:
        if s[0] == '@':
            v = s[1:]
            if v.isdigit(): val = int(v)
            else:
                if not v or v[0].isdigit():
                    errors.append(f'Line {n}: invalid instruction "{s}"'); continue
                if v not in symbols:
                    symbols[v] = nxt; nxt += 1
                val = symbols[v]
            if val > 32767:
                errors.append(f'Line {n}: address out of range'); continue
            out.append(format(val, '016b'))
        else:
            dest, rest = ('', s)
            if '=' in s: dest, rest = s.split('=', 1)
            comp, jump = rest, ''
            if ';' in rest: comp, jump = rest.split(';', 1)
            if comp not in COMP or dest not in DEST or jump not in JUMP:
                errors.append(f'Line {n}: invalid instruction "{s}"'); continue
            out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
    for w in warnings: print(w)
    if errors:
        for e in errors: print(e)
        print('Assembly failed.'); return False
    base = os.path.splitext(path)[0]
    with open(base + '.hack', 'w') as f: f.write('\n'.join(out) + '\n')
    print(f'Wrote {base}.hack ({len(out)} instructions)')
    if k is None or k % 3 == 0:   # feature for K mod 3 == 0
        with open(os.path.join(os.path.dirname(path) or '.', 'symbols.txt'), 'w') as f:
            for name, a in symbols.items():
                if name not in predefined: f.write(f'{name} = {a}\n')
        print('Wrote symbols.txt')
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit('Usage: python assembler.py File.asm [K]')
    ok = assemble(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
    sys.exit(0 if ok else 1)
