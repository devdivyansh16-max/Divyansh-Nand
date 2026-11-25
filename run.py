import subprocess, sys
k = int(sys.argv[1]) if len(sys.argv) > 1 else int('2501730385'[-2:])  # roll no 2501730385 -> K = 85
subprocess.check_call([sys.executable, 'make_box.py', str(k)])
subprocess.check_call([sys.executable, 'assembler.py', 'Box.asm', str(k)])
print('Done. Load hdl/Computer.hdl in CPU Emulator, then load Box.hack.')
