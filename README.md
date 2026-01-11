# MIPS Assembler & Disassembler

## Overview
This project implements a two-pass assembler and disassembler for a subset of
MIPS-like instructions. The assembler translates assembly code into 32-bit
machine code, and the disassembler reverses machine code back into readable
assembly.

The goal of this project was to deepen understanding of instruction encoding,
control flow, and how high-level logic maps to low-level execution.

---

## Features
- Supports arithmetic, logical, memory, branch, and jump instructions
- Two-pass assembly with label resolution
- PC-relative branching and jump handling
- Disassembler reconstructs readable assembly from binary
- Round-trip verification using a FizzBuzz program

---
## Project Structure
```text
mips-assembler-disassembler/
├── assembler.py
├── disassembler.py
├── README.md
├── .gitignore
└── examples/
    ├── fizzbuzz.asm
    ├── fizzbuzz.mc
    └── fizzbuzz_out.asm
```
Usage

Assemble 
```bash
python3 assembler.py examples/fizzbuzz.asm examples/fizzbuzz.mc
```
Disassemble
```bash
python3 disassembler.py examples/fizzbuzz.mc examples/fizzbuzz_out.asm
```
Example
```asm
addi $t0, $zero, 1
addi $t1, $zero, 100
beq  $t0, $zero, end
```

Security & Systems Relevance

Understanding how assembly instructions map to machine code is foundational for
systems programming, reverse engineering, and cybersecurity. This project builds
intuition for:
```markdown
- Binary instruction formats
- Control-flow behavior at the machine level
- How bugs and vulnerabilities can emerge from low-level logic
- Reverse engineering and static analysis concepts
```

Author

**Cade Fair**  
Computer Science Student — San Diego State University  
Cybersecurity & Systems Programming Focus


