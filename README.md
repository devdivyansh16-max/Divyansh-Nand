# Capstone - how to run
1. Extract zip and open the folder in VS Code terminal.
2. Start the interactive dashboard with `python dashboard.py`, then open http://127.0.0.1:8000.
   The preview reacts to key presses; **Run build** invokes the project Python workflow.
3. Or run `python run_all.py` directly (roll no 2501730385 -> K=85 by default; or: `python run_all.py 85`).
   -> makes Box.asm/Box.hack, assembles Add, Max, Rect (+Pong if you copy Pong.asm here)
4. Compare: save official assembler outputs in official/ (Add.hack, Max.hack, Rect.hack, Pong.hack); run_all.py reports MATCH/DIFFERENT.
5. HDL: the CPU, Memory and Computer implementations are in `hdl/`. Open the folder
   in the nand2tetris Hardware Simulator and run the official Project 5 tests. The
   course-standard ALU, registers, PC, RAM16K, Screen, Keyboard and ROM32K chips are
   simulator built-ins, as permitted by the capstone instructions.
6. Browser simulation: the dashboard fetches the generated `Box.hack` and simulates
   the Hack CPU, RAM, keyboard and screen. Use Run, Pause, Step and Reset.
7. CPU Emulator: load `hdl/Computer.hdl`, load `Box.hack`, press a key.

The dashboard simulation runs the assembled machine code in a browser-based Hack CPU.
Run the official HDL tests in the nand2tetris Hardware Simulator as a separate check.
Add Pong.asm and official assembler outputs if you want to compare all four programs.
