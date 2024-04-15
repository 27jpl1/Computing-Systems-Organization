// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

// screen = SCREEN
// Forever {
//	if key == pressed (!= 0):
//		set screen to -1
//	if key != pressed (== 0):
//		set screen to 0
//	screen += 1
//	if screen > length of screen:
//		screen == SCREEN
// }

//Set screen to SCREEN
@SCREEN
D=A
@screen
M=D

// Forever Loop
(FOREVER)

//Check keyboard
@KBD
D=M
@CLEAR
D;JEQ //If keyboard == 0 go to clear

// if not clear the goes on to darken the screen
@screen
A=M
M=-1

@ADD //goes to add to add 1 to screen 
0;JMP //goes to add to add 1 to screen 

//Clear the screen
(CLEAR)
@screen
A=M
M=0

(ADD)
@screen
M=M+1 //set the screen to += 1

// check if screen is too big
//the screen end is 24575
@24575
D=A
@screen
D=M-D
@END
D;JLE //if screen - 24575 <= 0 then don't reset screen

(RESET) // resets the screen to SCREEN
@SCREEN
D=A
@screen
M=D

(END) // jumps here if no need to reset
@FOREVER
0;JMP //Go back to top of loop


