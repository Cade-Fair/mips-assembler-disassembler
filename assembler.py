'''

                            Online Python Compiler.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

'''
import sys

register_map = {
    "zero": 0, "at": 1, "v0": 2, "v1": 3,
    "a0": 4, "a1": 5, "a2": 6, "a3": 7,
    "t0": 8, "t1": 9, "t2": 10, "t3": 11, "t4": 12, "t5": 13, "t6": 14, "t7": 15,
    "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "t8": 24, "t9": 25, "k0": 26, "k1": 27, "gp": 28, "sp": 29, "fp": 30, "s8": 30, "ra": 31,
}

opcodes = {
    "addi": "001000",
    "sw":   "101011",
    "lw":   "100011",
    "andi": "001100",
    "ori":  "001101",
    "slti": "001010",
    "beq":  "000100",
    "bne":  "000101",
    "lui":  "001111",
    "j":    "000010",
    "jal":  "000011",
}

functs = { 
    "add": "100000",
    "sub": "100010",
    "and": "100100",
    "or":  "100101",
    "slt": "101010",
    "xor": "100110",
    "sll": "000000",
    "srl": "000010",
    "jr":  "001000",
}

def to_bits(value: int, width: int) -> str:
    mask = (1 << width) - 1
    return format(value & mask, f"0{width}b")

def parse_register(token: str) -> int:
    if not token.startswith("$"):
        raise ValueError(f"Invalid register: {token}")
    name = token[1:].lower()
    if name.isdigit():
        num = int(name)
        if 0 <= num <= 31:
            return num
        raise ValueError(f"Register out of range: {token}")
    if name in register_map:
        return register_map[name]
    raise ValueError(f"Unknown register: {token}")

def strip_comments(line: str) -> str:
    return line.split("#", 1)[0].strip()
    
def parse_offset_addr(token: str):
    # Expects offset(rs) for example 16($t0)
    if "(" not in token or not token.endswith(")"):
        raise ValueError(f"Bad address syntax: {token}")
    off_str, rs_tok = token.split("(", 1)
    rs_tok = rs_tok[:-1] # Remove the last character
    offset = int(off_str, 0)
    rs = parse_register(rs_tok)
    return offset, rs

def translate_line(line: str, pc = None, labels = None) -> str:
    line = strip_comments(line)
    if not line:
        return ""
    tokens = line.replace(",", " ").split()
    mnemonic = tokens[0].lower()

    if mnemonic == "addi" and len(tokens) == 4:
        _, rt_tok, rs_tok, imm_tok = tokens
        opcode = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(int(imm_tok, 0), 16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"
    
    if  mnemonic in {"add", "sub", "and", "or", "xor", "slt"}:
        if len(tokens) != 4:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rd, rs, rt")
        _, rd_tok, rs_tok, rt_tok = tokens
        
        opcode_bits = "000000"
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        rd_bits = to_bits(parse_register(rd_tok), 5)
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        
        return f"{opcode_bits}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"
        
    
    if mnemonic == "nop":
        if len(tokens) != 1:
            raise ValueError("nop takes no operands")
        return "0" * 32 + "\n"
    
    if mnemonic == "lui":
        if len(tokens) !=3:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rt, imm")
        _, rt_tok, imm_tok = tokens
        
        opcode_bits = opcodes[mnemonic]
        rs_bits = "00000"
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(int(imm_tok, 0), 16)
        
        return f"{opcode_bits}{rs_bits}{rt_bits}{imm_bits}\n"
    
    if mnemonic in ("sll", "srl"):
        if len(tokens) != 4:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rd, rt, shamt")
        _, rd_tok, rt_tok, shamt_tok = tokens
         
        shamt_val = int(shamt_tok, 0)
        opcode_bits = "000000"
        rs_bits = "00000"
        rt_bits = to_bits(parse_register(rt_tok), 5)
        rd_bits = to_bits(parse_register(rd_tok), 5)
        shamt_bits = to_bits(shamt_val, 5)
        funct_bits = functs[mnemonic]
        return f"{opcode_bits}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"

    
    if mnemonic in ("j", "jal"): 
        if len(tokens) != 2:
            raise ValueError("Expects: {mnemonic} label")
        _, target_tok = tokens
        opcode_bits = opcodes[mnemonic]
        
        try: 
            addr = int(target_tok,0)
        except ValueError:
            if labels is None:
                raise ValueError("Jump needs labels")
            if target_tok not in labels:
                raise ValueError(f"Unknown label {target_tok}")
            addr = labels[target_tok]
        target26 = addr >> 2 #store word address
        if not (0 <= target26 < (1 << 26)):
            raise ValueError(f"{mnemonic} target out of range")
        target_bits = to_bits(target26, 26)
        return f"{opcode_bits}{target_bits}\n"
    
        
    
    
    if mnemonic == "jr": 
        if len(tokens) != 2:
            raise ValueError("jr expects: jr rs")
        _, rs_tok = tokens
        opcode_bits = "000000"
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = "00000"
        rd_bits = "00000"
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode_bits}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"

    
    if mnemonic in ("lw", "sw"):
        if len(tokens) !=3:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rt, offset(rs)")
        _, rt_tok, addr_tok = tokens
        
        opcode_bits = opcodes[mnemonic]
        offset, rs_num = parse_offset_addr(addr_tok)
        rs_bits = to_bits(rs_num, 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(offset, 16)
        
        return f"{opcode_bits}{rs_bits}{rt_bits}{imm_bits}\n"
        
    
    if mnemonic in ("andi", "ori", "slti"):
        if len(tokens) != 4:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rt, rs, imm")
        _, rt_tok, rs_tok, imm_tok = tokens
        
        opcode_bits = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(int(imm_tok, 0), 16)
        return f"{opcode_bits}{rs_bits}{rt_bits}{imm_bits}\n"
    
    
    if mnemonic in ("beq", "bne"):
        if len(tokens) != 4:
            raise ValueError(f"Wrong number of operands for {mnemonic} expects: {mnemonic} rs, rt, imm")
        _, rs_tok, rt_tok, imm_tok = tokens
        
        opcode_bits = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        
        try: 
            offset = int(imm_tok,0) # Try numeric first
        except ValueError:
            if labels is None or pc is None:
                raise ValueError("Need labels and pc")
            if imm_tok not in labels:
                raise ValueError(f"Unknown label {imm_tok}")
            offset = (labels[imm_tok] - (pc + 4)) // 4 
        imm_bits = to_bits(offset, 16)
        return f"{opcode_bits}{rs_bits}{rt_bits}{imm_bits}\n"
        
    return "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"

def build_labels(lines):
    labels = {}
    pc = 0
    program = []
    
    for line_number, line in enumerate(lines, start=1):
        clean = strip_comments(line).strip()
        if not clean: #if line empty skip it
            continue
        
        while ":" in clean:
            parts = clean.split(":",1)
            label = parts[0].strip() # remove spaces near lable
            
            if not label.isidentifier(): 
                #check valid python style lable
                raise ValueError(f"Invalid label name {label} at line {line_number}")
            
            if label in labels:
                #avoid duplicates
                raise ValueError(f"Duplicate label {label} at line {line_number}")
            
            labels[label] = pc
            # store label's address 
            
            clean = parts[1].strip() 
            # Keep part after :
            
            if not clean:
                # if no remaning code then break
                break
            
        if clean: 
            program.append((pc, clean, line_number))
            # add a tuple
            pc += 4 
    return labels, program

def main(argv):
    if len(argv) < 3:
        print("Usage: assembler.py <input.asm> <output.mc>")
        sys.exit(1)

    in_path, out_path = argv[1], argv[2]
    
    try: 
        # Pass 1 read all lines and build the build the labels
        with open(in_path, "r") as fin:
            lines = fin.readlines()
            
        labels, program = build_labels(lines)
        
        
        # Pass 2 assemble and write
        with open(out_path, "w") as fout:
            for pc, line, line_number in program:
                try:
                    fout.write(translate_line(line, pc = pc, labels = labels))
                except Exception as exc:
                    fout.write("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                    sys.stderr.write(f"[Line {line_number}] {exc}\n")
                    
    except FileNotFoundError as exc:
        print(f"File error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
#import disassembler

#if __name__ == "__main__":
  #disassembler.main(sys.argv)

