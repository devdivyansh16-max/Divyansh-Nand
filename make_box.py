#!/usr/bin/env python3
"""Generates Box.asm for your K. Usage: python make_box.py K"""
import sys
K = int(sys.argv[1]); W = (K % 4) + 1
START = 16384 + 32 * K; SKIP = 32 - W
asm = f"""// Box.asm  K={K}: rows {K}..{K+19}, width {16*W}px ({W} words), left edge
// Start address = SCREEN + 32*{K} = {START}
(MAIN)
    @KBD
    D=M
    @PRESSED
    D;JNE
    @COLOR
    M=0            // no key -> white
    @DRAW
    0;JMP
(PRESSED)
    @COLOR
    M=-1           // key -> black
(DRAW)
    @{START}
    D=A
    @ADDR
    M=D
    @ROW
    M=0
(ROWLOOP)
    @ROW
    D=M
    @20
    D=D-A
    @MAIN
    D;JGE          // 20 rows done
    @COL
    M=0
(COLLOOP)
    @COL
    D=M
    @{W}
    D=D-A
    @NEXTROW
    D;JGE          // row finished
    @COLOR
    D=M
    @ADDR
    A=M
    M=D            // write word
    @ADDR
    M=M+1
    @COL
    M=M+1
    @COLLOOP
    0;JMP
(NEXTROW)
    @{SKIP}
    D=A
    @ADDR
    D=D+M
    M=D            // jump to start of next row
    @ROW
    M=M+1
    @ROWLOOP
    0;JMP
"""
open('Box.asm', 'w').write(asm); print(f'Box.asm written (K={K}, width={16*W}px)')
