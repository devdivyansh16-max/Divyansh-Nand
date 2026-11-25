// Box.asm  K=85: rows 85..104, width 32px (2 words), left edge
// Start address = SCREEN + 32*85 = 19104
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
    @19104
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
    @2
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
    @30
    D=A
    @ADDR
    D=D+M
    M=D            // jump to start of next row
    @ROW
    M=M+1
    @ROWLOOP
    0;JMP
