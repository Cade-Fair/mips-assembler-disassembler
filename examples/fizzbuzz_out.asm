    addi $t0, $zero, 1
    addi $t1, $zero, 100
    addi $t2, $zero, 3
    addi $t3, $zero, 5
    addi $t2, $t2, -1
    addi $t3, $t3, -1
    beq $t2, $zero, 36
    beq $t3, $zero, 48
    j 64
    beq $t3, $zero, 56
    addi $t2, $zero, 3
    j 64
    addi $t3, $zero, 5
    j 64
    addi $t2, $zero, 3
    addi $t3, $zero, 5
    addi $t0, $t0, 1
    slt $at, $t1, $t0
    beq $at, $zero, 16
    nop
