addi $t0, $zero,1 
addi $t1, $zero, 100 
addi $t2, $zero, 3 
addi $t3, $zero, 5
loop: 
    addi $t2, $t2, -1
    addi $t3, $t3, -1
    beq $t2, $zero, fizz
    beq $t3, $zero, buzz
print: 
    j cont 
fizz: 
    beq $t3, $zero, fizzbuzz
    addi $t2, $zero, 3 
    j cont 
buzz: 
    addi $t3, $zero, 5
    j cont 
fizzbuzz:
    addi $t2, $zero, 3 
    addi $t3, $zero, 5 
cont: 
    addi $t0, $t0, 1 
    slt $at, $t1, $t0
    beq $at, $zero, loop
    nop