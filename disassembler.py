import sys
register_map = {
    "zero": 0, "at": 1, "v0": 2, "v1": 3,
    "a0": 4, "a1": 5, "a2": 6, "a3": 7,
    "t0": 8, "t1": 9, "t2": 10, "t3": 11, "t4": 12, "t5": 13, "t6": 14, "t7": 15,
    "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "t8": 24, "t9": 25, "k0": 26, "k1": 27, "gp": 28, "sp": 29, "fp": 30, "s8": 30, "ra": 31,
}

num_to_name = {v: k for (k, v) in register_map.items()}

def regstr(num): return f"${num_to_name.get(num,num)}"
def u(bits): return int(bits,2)
def sx16(x): return x - 0x10000 if x & 0x8000 else x 

# decode tables
funct_r = { 
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
    "100110": "xor",
    "000000": "sll",
    "000010": "srl",
    "001000": "jr",
}

opcode_i = { 
    "001000": "addi",
    "101011": "sw",
    "100011": "lw",
    "001100": "andi",
    "001101": "ori",
    "001010": "slti",
    "000100": "beq",
    "000101": "bne",
    "001111": "lui",
}

opcode_j = { 
    "000010": "j",
    "000011": "jal",
}

def all_zero(s): return set(s) <= {"0"}

#Pass 1 collect jump/branch targers to label
def collect_targets(lines):
    targets = set()
    pc = 0
    for bits in lines:
        bits = bits.strip()
        if not bits:
            pc += 4; continue
        if all_zero(bits):
            pc += 4; continue 
        
    opc = bits[0:6]
    if opc == "000000": # R-type
        funct = bits [26:32]
    elif opc in opcode_i:
        rs = u(bits[6:11]); rt = u(bits[11:16]); imm = u(bits[16:32])
        mnemonic = opcode_i[opc]
        if mnemonic in ("beq", "bne"):
            off = sx16(imm)
            tgt = pc + 4 + (off << 2)
            targets.add(tgt)
    elif opc in opcode_j:
        tgt26 = u(bits[6:32])
        tgt = (tgt26 << 2)
        targets.add(tgt)
    pc += 4
    
    label_names = {}
    for i, addr in enumerate(sorted(targets)):
        label_names[addr] = f"L{i}"
    return label_names
    
# Pass 2 disassemble and write
def disassemble(lines, out_path):
    labels = collect_targets(lines)
    pc = 0
    with open(out_path, "w") as fout:
        for bits in lines:
            bits = bits.strip()
            if pc in labels:
                fout.write(f"{labels[pc]}: \n")
            if not bits: 
                pc += 4; continue
            opc = bits [0:6]
            
            #Nop 
            if all_zero(bits):
                fout.write("    nop\n"); pc += 4; continue
            
            if opc == "000000":
                rs = u(bits[6:11]); rt = u(bits[11:16]); rd = u(bits[16:21]); shamt = u(bits[21:26]); funct = bits[26:32]
                mnem = funct_r.get(funct)
                if mnem is None:
                    fout.write("   unknown R-type\n")
                elif mnem in ("sll", "srl"):
                    fout.write(f"    {mnem} {regstr(rd)}, {regstr(rt)}, {shamt}\n")
                elif mnem == "jr":
                    fout.write(f"    jr {regstr(rs)}\n")
                else: 
                    fout.write(f"    {mnem} {regstr(rd)}, {regstr(rs)}, {regstr(rt)}\n")
            
            elif opc in opcode_i:
                rs = u(bits[6:11]); rt = u(bits[11:16]); imm = u(bits[16:32]) 
                mnem = opcode_i[opc]
                if mnem in ("addi", "slti"):
                    imm_val = sx16(imm)
                    fout.write(f"    {mnem} {regstr(rt)}, {regstr(rs)}, {imm_val}\n")
                elif mnem in ("andi", "ori"):
                    fout.write(f"    {mnem} {regstr(rt)}, {regstr(rs)}, {imm}\n")
                elif mnem == "lui":
                    fout.write(f".   {mnem} {regstr(rt)}, {imm}\n")
                elif mnem in ("lw", "sw"):
                    off = sx16(imm)
                    fout.write(f"    {mnem} {regstr(rt)}, {off}({regstr(rs)})\n")
                elif mnem in ("beq", "bne"):
                    off = sx16(imm)
                    tgt = pc + 4 + (off << 2)
                    label = labels.get(tgt, str(tgt))
                    fout.write(f"    {mnem} {regstr(rs)}, {regstr(rt)}, {label}\n")
                else: 
                    fout.write("   unknown I-type\n")
                
            elif opc in opcode_j:
                tgt26 = u(bits[6:32])
                tgt = (tgt26 << 2)
                label = labels.get(tgt26, str(tgt))
                fout.write(f"    {opcode_j[opc]} {label}\n")
            else: 
                fout.write("    unknown opcode\n")
            pc += 4
                   
def main(argv): 
    if len(argv) < 3:
        print("Usage: assembler.py <input.asm> <output.mc>")
        sys.exit(1)
    in_path, out_path = argv[1], argv[2]
    with open(in_path, "r") as f:
        lines = f.readlines()
    disassemble(lines, out_path)
    
if __name__ == "__main__":
    main(sys.argv)
        
    
    
    
    

        
        
        
        