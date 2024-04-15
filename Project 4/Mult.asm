//Initialize R2 to 0
@R2
M=0

//Actual Multiplication
@R1
D=M
@times_left
M=D
//times_left = R1
(LOOP)
//if times_left = 0 go to end
@times_left
D=M
@END
D;JEQ
//else add R0 another time to R2
@R0
D=M
@R2
M=M+D
//times_left - 1
@times_left
M=M-1
@LOOP
0;JMP
(END)
@END
0;JMP