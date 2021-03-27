# Janggi

This is a PyGame representation of the board game Janggi. Janggi is similar to chess but has some key differences.
The game is played on a 9x10 board where the object is to place the opponents General in checkmate.

### Features to add
- <del>*CheckMate algorithm*</del>
- <del>*Players can not move to a place that will put them in check*</del>
- <del>*Reset button after a game has been played*</del>
- AI for a one player game.
- Add in rule that will check if enemy generals are facing each other.
- Add assets to pieces that will make the game look better/more appealing.

### Gameplay and rules
 

- Soldier
  - The Soldier is similar to a pawn in chess.
  - The soldier piece may move one space left or right or in the advancing position.
  - There is a special case where the Soldier can move in a diagonal but only in the Palace/Fortress.
- Chariot
  - The Chariot can move as many spaces in a straight line on the board. 
  - The Chariot can not jump or take over a piece of the same color, but can capture a piece of a different color.
- Elephant
  - The Elephant starts one place forward, left, right, or backward, and then moves two spaces diagonally.
  - The Elephant can be blocked if there is a piece along the path to the placement.
- Horse
  - The Horse starts one place forward, left, right, or backward, and then moves one space diagonally.
  - Like the Elephant the Horse can be blocked along the path.
- Guard
  - The Guard must stay inside the Palace/Fortress, and can only move one space along any line in the Fortress/Palace.
- Cannon
  - The Cannon moves along any straight line, including Palace/Fortress lines, but must have ONE piece, any color, to jump over.
  - The only exceptions are that the Cannon can not jump over another Cannon, and the Cannon can not capture another Cannon piece. 
- General
  - The General, like the Guard, must stay inside the Palace/Fortress, and can only move one space along any line in the Fortress/Palace.

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