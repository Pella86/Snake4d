# Snake 4d
This program is a 4 spatial dimensions snake game. The snake is inspired by the nokia game, or the arcades before that
The implementation is a simple perspective projection from the 4d space to the 2d screen


## Usage
The game requires python (3.0) to be installed and the tkinter package.
To run the game just use

```python main.py```

## Trailer - rendered in Blender3d
https://youtu.be/M1nB-Q0JOBA

## How to play
![Instruction image](/images/Labelled_instructions.png)  

The snake can move in 8 directions (in 2 dimensions there are 4, in 3 dimensions there are 6 and in the 4 space there are 8 possible directions).  
The directions are mapped to the keys WASD and IJKL.
To help visualize where the snake is going there are 3 screens, 1 having a perspective projection of the game, which in general is quite confusing (although looks cool).
There are two more screens, where the snake game is flat projected on the major planes. These flat prjection can help to follow where the snake is going.  
The flat screens are set so that the direction of the snakes corresponds to the keyboard direction. Namely pressing A will turn the snake left in the YX plane, while pressing L will turn the snake right in the WZ plane.  
The food is a blue cube randomly spawned in the game, catching the food gives one point.
going outside the borders or crossing the snake with itself ends the game.



