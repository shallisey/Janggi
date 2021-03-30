# Janggi

This is a PyGame representation of the board game Janggi. Janggi is similar to chess but has some key differences.
The game is played on a 9x10 board where the object is to place the opponents General in checkmate.

### Features to add
- <del>*CheckMate algorithm*</del>
- <del>*Players can not move to a place that will put them in check*</del>
- <del>*Reset button after a game has been played*</del>
- AI for a one player game.
- Add in rule that will check if enemy generals are facing each other.
- <del>*Add assets to pieces that will make the game look better/more appealing.*<del>

# Updated Board 3/30
  <img width="50%" alt="Updated Janggi" src="https://user-images.githubusercontent.com/47544304/113047977-9e64d780-9167-11eb-955b-fd43ca4da98e.png">

### Rules and movement

[Link to a game played at 4x speed](https://www.youtube.com/watch?v=dv5mZsji8hM)

- Soldier
  - The Soldier is similar to a pawn in chess.
  - The soldier piece may move one space left or right or in the advancing position.
  - There is a special case where the Soldier can move in a diagonal but only in the Palace/Fortress.
  <img width = 50% alt="Soldier moves" src="https://user-images.githubusercontent.com/47544304/112735458-25247500-8f1a-11eb-85b9-1ec8a1f3d6d6.png">
- Chariot
  - The Chariot can move as many spaces in a straight line on the board. 
  - The Chariot can not jump or take over a piece of the same color, but can capture a piece of a different color.
  <img width= 50% alt="Chariot moves" src="https://user-images.githubusercontent.com/47544304/112735515-949a6480-8f1a-11eb-86cf-c72c47d075be.png">
- Elephant
  - The Elephant starts one place forward, left, right, or backward, and then moves two spaces diagonally.
  - The Elephant can be blocked if there is a piece along the path to the placement.
  <img width= 50% alt="Elephant moves" src="https://user-images.githubusercontent.com/47544304/112735540-b98ed780-8f1a-11eb-82fe-c2d005e3b35a.png">
- Horse
  - The Horse starts one place forward, left, right, or backward, and then moves one space diagonally.
  - Like the Elephant the Horse can be blocked along the path.
  <img width= 50% alt="Horse moves" src="https://user-images.githubusercontent.com/47544304/112735546-cad7e400-8f1a-11eb-8b19-176d0548fdab.png">
- Guard
  - The Guard must stay inside the Palace/Fortress, and can only move one space along any line in the Fortress/Palace.
  <img width= 50% alt="Guard moves" src="https://user-images.githubusercontent.com/47544304/112735553-d75c3c80-8f1a-11eb-82b5-00039a21f8bd.png">
- Cannon
  - The Cannon moves along any straight line, including Palace/Fortress lines, but must have ONE piece, any color, to jump over.
  - The only exceptions are that the Cannon can not jump over another Cannon, and the Cannon can not capture another Cannon piece. \
  <img width= 50% alt="Cannon moves" src="https://user-images.githubusercontent.com/47544304/112735561-ecd16680-8f1a-11eb-83f8-87f5732a4f66.png">
- General
  - The General, like the Guard, must stay inside the Palace/Fortress, and can only move one space along any line in the Fortress/Palace.
  <img width= 50% alt="General moves" src="https://user-images.githubusercontent.com/47544304/112735568-f955bf00-8f1a-11eb-859f-438e8f2bf607.png">
  
  


### Prerequisites
You will need to have installed the at least Python 3.7.7 because that is what is recommended by the next requirement.         
PyGame needs to be installed on your device to display and play Janggi.


- [Python](https://www.python.org/downloads/) - Instructions to download and install Python on your device of choice.
- [Pygame](https://www.pygame.org/wiki/GettingStarted) - Instructions to install PyGame.

Type into your command line
```
$ python --version
--python version here-- if installed correctly
```

This will execute a simple game if PyGame was installed correctly.
```
python3 -m pygame.examples.aliens
```

## Built With

* [Python](https://www.python.org/)
* [Pygame](https://www.pygame.org/news)

## Authors

* **Sean Hallisey**
