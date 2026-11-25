"use strict";

class HackEmulator {
  constructor() {
    this.rom = new Uint16Array(32768);
    this.ram = new Uint16Array(32768);
    this.programLength = 0;
    this.a = 0;
    this.d = 0;
    this.pc = 0;
    this.cycles = 0;
  }

  load(machineCode) {
    const instructions = machineCode.split(/\r?\n/).map(function (line) {
      return line.trim();
    }).filter(Boolean);

    if (instructions.length === 0 || instructions.length > this.rom.length) {
      throw new Error("Box.hack is empty or larger than the Hack ROM.");
    }

    this.rom.fill(0);
    for (let index = 0; index < instructions.length; index += 1) {
      if (!/^[01]{16}$/.test(instructions[index])) {
        throw new Error("Invalid 16-bit machine instruction on line " + (index + 1) + ".");
      }
      this.rom[index] = parseInt(instructions[index], 2);
    }
    this.programLength = instructions.length;
    this.reset();
  }

  reset() {
    this.ram.fill(0);
    this.a = 0;
    this.d = 0;
    this.pc = 0;
    this.cycles = 0;
  }

  setKeyboard(keyCode) {
    this.ram[24576] = keyCode & 0xffff;
  }

  step() {
    const instruction = this.rom[this.pc];
    const oldA = this.a;

    if ((instruction & 0x8000) === 0) {
      this.a = instruction & 0x7fff;
      this.pc = (this.pc + 1) & 0x7fff;
      this.cycles += 1;
      return;
    }

    const useMemory = (instruction & 0x1000) !== 0;
    let x = this.d;
    let y = useMemory ? this.ram[oldA & 0x7fff] : oldA;

    if (instruction & 0x0800) x = 0;
    if (instruction & 0x0400) x = (~x) & 0xffff;
    if (instruction & 0x0200) y = 0;
    if (instruction & 0x0100) y = (~y) & 0xffff;

    let result = instruction & 0x0080 ? (x + y) & 0xffff : x & y;
    if (instruction & 0x0040) result = (~result) & 0xffff;

    const isZero = result === 0;
    const isNegative = (result & 0x8000) !== 0;
    const destination = (instruction >> 3) & 0x7;

    if (destination & 0x1 && (oldA & 0x7fff) !== 24576) {
      this.ram[oldA & 0x7fff] = result;
    }
    if (destination & 0x2) this.d = result;
    if (destination & 0x4) this.a = result;

    const jump = instruction & 0x7;
    const jumpTaken =
      ((jump & 0x1) !== 0 && !isNegative && !isZero) ||
      ((jump & 0x2) !== 0 && isZero) ||
      ((jump & 0x4) !== 0 && isNegative);
    this.pc = jumpTaken ? oldA & 0x7fff : (this.pc + 1) & 0x7fff;
    this.cycles += 1;
  }

  run(instructionCount) {
    for (let index = 0; index < instructionCount; index += 1) {
      this.step();
    }
  }
}

window.HackEmulator = HackEmulator;
