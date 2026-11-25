import os, sys
from assembler import assemble
os.chdir(os.path.dirname(os.path.abspath(__file__)))
k = int(sys.argv[1]) if len(sys.argv) > 1 else int('2501730385'[-2:])  # roll no 2501730385 -> K = 85
import subprocess
subprocess.check_call([sys.executable, 'make_box.py', str(k)])
for f in ['Add.asm', 'Max.asm', 'Rect.asm', 'Pong.asm']:
    if os.path.exists(f):
        if not assemble(f, 1):  # 1 -> no symbols.txt for these
            raise SystemExit(f'Assembly failed for {f}')
    else:
        print(f'SKIPPED {f} (copy it from nand2tetris projects/06 into this folder)')
if not assemble('Box.asm', k):  # Box last: symbols.txt (if K%3==0) belongs to Box
    raise SystemExit('Assembly failed for Box.asm')
print('\n--- Comparison with official output (put official .hack files in official/) ---')
for f in ['Add', 'Max', 'Rect', 'Pong']:
    mine, off = f + '.hack', os.path.join('official', f + '.hack')
    if os.path.exists(mine) and os.path.exists(off):
        a = open(mine).read().split(); b = open(off).read().split()
        print(f, 'MATCH' if a == b else 'DIFFERENT')
    else:
        print(f, 'not compared (missing file)')
print(f'\nK={k}, K mod 3={k%3}, K mod 4={k%4}, box width={16*(k%4+1)}px, rows {k}..{k+19}')
