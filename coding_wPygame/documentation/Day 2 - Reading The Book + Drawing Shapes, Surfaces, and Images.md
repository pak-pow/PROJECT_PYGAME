Tags: [[Current Reading]], [[Books]], [[Programming]], [[Python]], [[PyGame]]

---
## 🧠 CONCEPT SUMMARY

#### Primitives:
The `pygame.draw` module contains functions to render simple geometric shapes directly to a surface.

> [!note] 
> Common functions include `rect`, `circle`, `line`, and `polygon`. They all require a target Surface and a Color.

#### RGB Colors:
Colors in Pygame are defined as tuples of three integers `(Red, Green, Blue)`, where 0 is no intensity and 255 is full intensity.

> [!note] 
> Examples: `(255, 0, 0)` is Red, `(0, 0, 0)` is Black, `(255, 255, 255)` is White.

#### Surface Objects:
A Surface is a rectangular object in memory containing pixel data. The main window is a Surface, but images loaded from files are also Surfaces.

> [!note] 
> You can create blank surfaces in code `pygame.Surface((w, h))` or load them from files using `pygame.image.load()`.

#### Blitting:
The method `blit()` stands for "Block Transfer". It copies the pixels of one surface onto another.

> [!note] 
> Syntax: `destination_surface.blit(source_surface, (x, y))`. This is how you draw characters and backgrounds.

## 🛠️ WHAT I DID TODAY

* **Mastered Colors:** Defined custom colors using RGB tuples.
* **Drew Shapes:** Used `pygame.draw.circle()` and `pygame.draw.line()` to create geometric graphics.
* **Created Surfaces:** Generated a synthetic image (a green square) in memory using `pygame.Surface()`.
* **Used Blit:** Successfully drew the synthetic image onto the main screen using the `screen.blit()` command.
* **Layering:** Learned the "Painter's Algorithm"—drawing order matters (background first, then shapes, then surfaces).

---

## 💻 SOURCE CODE

> [!example]- SOURCE CODE
> ```python
> import pygame, sys
> from pygame.locals import *
> 
> pygame.init()
> screen = pygame.display.set_mode((500,400))
> button_rect = pygame.Rect(100,100,200,50)
> color = (255, 0, 0)
> 
> # Create a "Dummy" Image Surface
> my_image = pygame.Surface((50, 50))
> my_image.fill((0, 255, 0)) # Green
> 
> while True:
>     for event in pygame.event.get():
>         if event.type == QUIT:
>             pygame.quit()
>             sys.exit()
>             
>         if event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
>             print("Button was clicked!")
>             if color == (0, 0, 255):
>                 color = (255, 0, 0)
>             else:
>                 color = (0, 0, 255)
> 
>     # 1. Background
>     screen.fill((255, 255, 255))
>     
>     # 2. Primitives
>     pygame.draw.rect(screen, color, button_rect)
>     pygame.draw.circle(screen, color, (350, 125), 25)
>     pygame.draw.line(screen, color, (0, 0), (500,400), 5)
> 
>     # 3. Blitting (Images)
>     screen.blit(my_image, (200,200))
> 
>     pygame.display.set_caption("TEST PYGAME")
>     pygame.display.update()
> ```

---

## 🧠 LEARNED TODAY

* **Drawing Order:** Things drawn *later* in the loop appear *on top* of things drawn earlier (Painter's Algorithm).
* **Width Argument:** For most shapes (circle, rect, ellipse), a width of `0` fills the shape, while a width > `0` draws an outline.
* **Image Coordinates:** When blitting an image, the coordinates `(x, y)` refer to the top-left corner of that image.

---

## 🧪 PRACTICE / EXERCISES

**Exercise: The "Face" Drawing**
Goal: Draw a face using primitives.

```python
# Head
pygame.draw.circle(screen, GREEN, (250, 200), 100, 0)
# Eyes
pygame.draw.circle(screen, BLUE, (220, 180), 15, 0)
pygame.draw.circle(screen, BLUE, (280, 180), 15, 0)
# Mouth
pygame.draw.line(screen, RED, (220, 240), (280, 240), 5)
````

---

## 💡 NOTES TO SELF

> [!important] Blitting is Copying:
> 
> blit does not "move" an object; it takes a stamp of it and stamps it onto the screen.

> [!important] Variable Order:
> 
> blit takes the source (what you want to draw) first, and the position second. screen.blit(player_image, player_pos).

---

## 🎯 GOALS FOR TOMORROW

> [!todo] ⌨️ **Day 3: Events & Input**
> 
> - Learn to detect specific key presses (Arrow keys, Spacebar).
>     
> - Differentiate between `KEYDOWN` (press) and `KEYUP` (release).
>     
> - Move a shape around the screen using keyboard input.
>     

---
# READING
### BOOK: [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf]]

---
#### **Chapter 1**: Interactive Shell

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=37&selection=154,0,158,68&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.8]]
> 
> > In this chapter, you learned the basics of writing Python instructions. Because computers don’t have common sense and only understand specific instructions, Python needs you to tell it exactly what to do.
> 

So basically in the this chapter just a rewind of what the basics of Python Language is like simple Math and how some of the operations is and how it is used for. 
#### **Chapter 2**: Writing Programs

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=49&selection=94,0,123,54&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.20]]
> 
> > Once you understand how to use strings and functions, you can start mak ing programs that interact with users. 
> > 
> > This is important because text is the main way the user and the computer will communicate with each other. 
> > 
> > The user enters text through the keyboard with the input() function, and the computer displays text on the screen with the print() function. Strings are just values of a new data type. 
> > 
> > All values have a data type, and the data type of a value affects how the + operator functions. Functions are used to carry out complicated instructions in your pro gram. Python has many built in functions that you’ll learn about in this book. 
> > 
> > Function calls can be used in expressions anywhere a value is used. The instruction or step in your program where Python is currently working is called the execution. 
> > 
> > In Chapter 3, you’ll learn more about mak ing the execution move in ways other than just straight down the program. Once you learn this, you’ll be ready to create games!
> 

And in this chapter its about learning some the basics of the Language with strings and inputs
#### **Chapter 3**: Guess The Number

> [!PDF|note] SUMMARY
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=65&selection=92,0,107,50&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.36]]
> > Programming is just the action of writing code for programs—that is, creating programs that can be executed by a computer. 
> > 
> > When you see someone using a computer program (for example, playing your Guess the Number game), all you see is some text appearing on the screen. 
> > 
> > The program decides what text to display on the screen (the program’s output) based on its instructions and on the text that the player typed with the keyboard (the program’s input). 
> > 
> > A program is just a collection of instructions that act on the user’s input.
> 
> 

##### 4 Core Types of Instructions

Basically, everything boils down to just four main building blocks. Here’s the breakdown:

1. **Expressions (The "Calculator" Part)**

These are just values connected by operators that crunch down to a single result.

- _Math Example:_ `2 + 2` becomes `4`.
- _String Example:_ `'Hello' + ' ' + 'World'` becomes `'Hello World'`.    
- _Note:_ When you use these with keywords like `if` or `for`, we call them **conditions**.

2. **Assignment Statements (Memory)**

This is how we store data. We calculate a value and stash it in a variable so we can use it later in the program.

3. **Flow Control (The Logic)**

This decides where the program goes next.

- **Keywords:** `if`, `for`, `break`.
- **Function:** They let us skip code, loop through it, or break out of loops entirely.
- **Function Calls:** These also change the flow by jumping execution to a specific set of instructions inside a function.

![Image of flowchart diagram logic](https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcT7LXmGgdqHb0AkLjegLNKvPROs4dkdPoTT-1cbz8NTUlaQVIfEOJfKkSI94R-JfOV7oNRg4XEiIyE3UMsIPAGRc66bTZnru8wdV3cLhFsdN7Y9WRU)

4. **I/O (Input / Output)**

This is how the program talks to the outside world.

- **Output:** `print()` sends text to the screen.
- **Input:** `input()` grabs text from the keyboard.
- **Technical Term:** We call this **I/O** (pronounced "eye-oh").

![Image of basic computer input output diagram](https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQ6BpGUIL8oqjVmjchbXfofwRMC42JZfC0PW-QMRfpc2vtKGivsmJrmJl8vwWJMQlraR0SC9-mXBDj52vakDlq5rrGR-D81VAXMFlijfdufWc7YAz4)

**The Bottom Line:**

That’s it—just those four things. Obviously, it gets deeper later on with complex data types, mouse/graphics I/O, and language-specific libraries but these are the foundational mechanics.

##### SOURCE CODES

> [!example]- Short Snippet
> 
> ```python
> # Example: Expressions, Assignment, Flow Control, I/O
> print("What is your name?")
> name = input()
> print("Hello, " + name)
> ```

> [!code]- Full Source Code — Guess the Number
> 
> ```python
> import random
> 
> guessesTaken = 0
> 
> print('Hello! What is your name?')
> myName = input()
> 
> number = random.randint(1, 20)
> print('Well, ' + myName + ', I am thinking of a number between 1 and 20.')
> 
> while guessesTaken < 6:
>     print('Take a guess.')
>     guess = input()
>     guess = int(guess)
>     
>     guessesTaken = guessesTaken + 1
>     
>     if guess < number:
>         print('Your guess is too low.')
>     
>     if guess > number:
>         print('Your guess is too high.')
>     
>     if guess == number:
>         break
> 
> if guess == number:
>     guessesTaken = str(guessesTaken)
>     print('Good job, ' + myName + '! You guessed my number in ' + guessesTaken + ' guesses!')
> 
> if guess != number:
>     number = str(number)
>     print('Nope. The number I was thinking of was ' + number)
> ```

---
#### **Chapter 4**: Joke Telling Program

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=73&selection=31,0,76,1&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.44]]
> > This chapter explores the different ways you can use the print() function. Escape characters are used for characters that are difficult to type into the code with the keyboard. 
> > 
> > If you want to use special characters in a string, you must use a backslash escape character, \, followed by another letter for the special character. 
> > 
> > For example, \n would be a newline. If your special character is a backslash itself, you use \\. 
> > 
> > The print() function automatically appends a newline character to the end of a string. Most of the time, this is a helpful shortcut. 
> > 
> > But sometimes you don’t want a newline character. To change this, you can pass a blank string as the keyword argument for print()’s end keyword parameter. For example, to print spam to the screen without a newline character, you would call print('spam', end='')
##### Advanced Print & Escape Characters

> [!NOTE] Overview
> The `print()` function handles more than just basic text. We use **escape characters** for special formatting and the `end` parameter to control line breaks.

### 1. Escape Characters (`\`)
These are used to insert characters that are "illegal" in a string or physically difficult to type. The backslash `\` acts as a signal to Python: *"Treat the very next character as a special command, not text."*

| Sequence | Meaning      | Usage                                                    |
| :------- | :----------- | :------------------------------------------------------- |
| `\n`     | Newline      | Moves the cursor to the start of the next line.          |
| `\\`     | Backslash    | Prints a literal `\` character (escapes itself).         |
| `\'`     | Single Quote | Allows a quote symbol inside a string defined by quotes. |
### 2. Controlling Output (`end` parameter)
By default, Python's `print()` automatically appends a newline character (`\n`) to the end of every string. This is why multiple print statements usually stack vertically.

**The Override:**
To keep output on the same line, pass a blank string to the `end` keyword argument.

```python
# Standard (Automatic Newline)
print('Spam') 
# Output: Spam\n

# Modified (No Newline)
print('Spam', end='')
# Output: Spam (cursor remains at the end of 'm')
````

##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> print("Knock Knock!")
> print("Who's there?")
> ```

> [!code]- Full Source Code — Joke Program
> 
> ```python
> print('What do you get when you cross a snowman with a vampire?')
> input()
> print('Frostbite!')
> print()
> print('Press Enter for another joke...')
> input()
> 
> print('What do dentists call an astronaut\'s cavity?')
> input()
> print('A black hole!')
> print()
> print('Press Enter for another joke...')
> input()
> 
> print('Knock knock.')
> input()
> print("Who\'s there?")
> input()
> print('Interrupting cow.')
> input()
> print('Interrupting cow wh', end='')
> print('-MOO!')
> ```

---
#### **Chapter 5**: Dragon Realm

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=90&selection=142,0,149,76&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.61]]
> > 
> > In the Dragon Realm game, you created your own functions. A function is a mini-program within your program. 
> > 
> > The code inside the function runs when the function is called. By breaking up your code into functions, you can organize your code into shorter and easier-to-understand sections. 
> > 
> > Arguments are values copied to the function’s parameters when the function is called. The function call itself evaluates to the return value.
> 
##### Functions & Scopes

This chapter moves beyond using built-in functions (like `print()`) to defining our own using the `def` keyword.

1. **Mini-Programs:** Functions allow us to reuse code. Instead of copy-pasting logic, we write it once and call it multiple times.
2. **Parameters vs. Arguments:**
    
    - **Parameters:** The variable names inside the function definition (e.g., `def greet(name):`).
    - **Arguments:** The actual value passed when calling the function (e.g., `greet('Alice')`).

3. **Variable Scope (The "Container" Rule):**
    
    - **Global Scope:** Variables created outside functions. They exist as long as the program runs.
    - **Local Scope:** Variables created _inside_ a function. They are created when the function starts and **destroyed** when it returns.
    - _Crucial Rule:_ Code in the global scope cannot use any local variables.

##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> def displayIntro():
>     print('You are in a land of dragons...')
> ```

> [!code]- Full Source Code — Dragon Realm
> 
> ```python
> import random
> import time
> 
> def displayIntro():
>     print('You are in a land full of dragons. In front of you,')
>     print('you see two caves. In one cave, the dragon is friendly')
>     print('and will share his treasure with you. The other dragon')
>     print('is greedy and hungry, and will eat you on sight.')
>     print()
> 
> def chooseCave():
>     cave = ''
>     while cave != '1' and cave != '2':
>         print('Which cave will you go into? (1 or 2)')
>         cave = input()
>     return cave
> 
> def checkCave(chosenCave):
>     print('You approach the cave...')
>     time.sleep(2)
>     print('It is dark and spooky...')
>     time.sleep(2)
>     print('A large dragon jumps out!')
>     time.sleep(2)
> 
>     friendlyCave = random.randint(1, 2)
> 
>     if chosenCave == str(friendlyCave):
>         print('He shares his treasure with you!')
>     else:
>         print('He gobbles you down in one bite!')
> 
> playAgain = 'yes'
> while playAgain == 'yes' or playAgain == 'y':
>     displayIntro()
>     caveNumber = chooseCave()
>     checkCave(caveNumber)
>     
>     print('Do you want to play again? (yes or no)')
>     playAgain = input().lower()
> ```

---

#### **Chapter 6**: Using the Debugger

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=104&selection=62,0,69,19&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.75]]
> > 
> > Writing programs is only the first part of programming. The next part is making sure the code you wrote actually works. Debuggers let you step through the code one line at a time. 
> > 
> > You can examine which lines execute in what order and what values the variables contain. When stepping through line by line is too slow, you can set breakpoints to stop the debugger only at the lines you want.

>[!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=104&selection=70,0,72,51&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.75]]
> > 
> > Using the debugger is a great way to understand what a program is doing. While this book provides explanations of all the game code we use, the debugger can help you find out more on your own
> 

##### The 3 Types of Bugs

Coding isn't just about writing; it's about fixing. There are three specific ways a program can fail:

|**Type**|**Description**|**Difficulty to Fix**|
|---|---|---|
|**Syntax Errors**|Grammar mistakes (e.g., missing a parenthesis or colon). Python catches these before running.|Easy|
|**Runtime Errors**|The code is grammatically correct but tries to do something illegal while running (e.g., dividing by zero). The program crashes.|Medium|
|**Semantic Errors**|The scariest type. The program runs perfectly without crashing, but it does the _wrong thing_ because the logic is flawed.|Hard|
##### The Debugger Tool

Instead of just guessing, we use the Debugger (in IDLE) to run code line-by-line.

- **Stepping:** Executing one instruction at a time.
- **Globals/Locals:** Watching variables change value in real-time.
##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> number1 = random.randint(1,10)
> number2 = random.randint(1,10)
> ```

> [!code]- Full Source Code — Debugging Example
> 
> ```python
> import random
> 
> number1 = random.randint(1, 10)
> number2 = random.randint(1, 10)
> 
> print('What is ' + str(number1) + ' + ' + str(number2) + '?')
> answer = input()
> 
> if int(answer) == number1 + number2:
>     print('Correct!')
> else:
>     print('Nope. The correct answer is ' + str(number1 + number2))
> ```

---

#### **Chapter 7**: Designing Hangman with Flowcharts

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=115&selection=4,0,19,33&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.86]]
> > 
> > It may seem like a lot of work to sketch out a flowchart about the program first. After all, people want to play games, not look at flowcharts! 
> > 
> > But it is much easier to make changes and identify problems by thinking about how the program works before writing the code for it. If you jump in to write the code first, you may discover problems that require you to change the code you’ve already written, wasting time and effort. 
> > 
> > And every time you change your code, you risk creating new bugs by changing too little or too much. It is much more efficient to know what you want to build before you build it. 
> > 
> > Now that we have a flowchart, let’s create the Hangman program in Chapter 8!
> 

##### Logic Visualization & ASCII Art

Before writing code for complex games like Hangman, we need a map.

1. Flowcharts:
    
    A diagram that represents the logic flow.
    
    - **Terminator (Oval):** Start or End.
    - **Process (Rectangle):** An action (e.g., "Pick a random word").
    - **Decision (Diamond):** A branch (e.g., "Is the letter in the word?").
        
2. ASCII Art:
    
    Using text characters to create graphics. In Hangman, we use characters like |, -, and O to draw the gallows and the victim.
    
##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> HANGMAN_PICS = ['''
>   +---+
>       |
> ''']
> ```

> [!code]- Full Source Code — Hangman
> 
> ```python
> import random
> 
> HANGMAN_PICS = ['''
>   +---+
>       |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>   |   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  /    |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  / \  |
>      ===''']
> 
> words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard mole monkey mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
> 
> def getRandomWord(wordList):
>     wordIndex = random.randint(0, len(wordList) - 1)
>     return wordList[wordIndex]
> 
> def displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord):
>     print(HANGMAN_PICS[len(missedLetters)])
>     print()
> 
>     print('Missed letters:', end=' ')
>     for letter in missedLetters:
>         print(letter, end=' ')
>     print()
> 
>     blanks = '_' * len(secretWord)
> 
>     for i in range(len(secretWord)):
>         if secretWord[i] in correctLetters:
>             blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
> 
>     for letter in blanks:
>         print(letter, end=' ')
>     print()
> 
> def getGuess(alreadyGuessed):
>     while True:
>         print('Guess a letter.')
>         guess = input().lower()
>         if len(guess) != 1:
>             print('Please enter a single letter.')
>         elif guess in alreadyGuessed:
>             print('You have already guessed that letter. Choose again.')
>         elif guess not in 'abcdefghijklmnopqrstuvwxyz':
>             print('Please enter a LETTER.')
>         else:
>             return guess
> 
> def playAgain():
>     print('Do you want to play again? (yes or no)')
>     return input().lower().startswith('y')
> 
> print('H A N G M A N')
> missedLetters = ''
> correctLetters = ''
> secretWord = getRandomWord(words)
> gameIsDone = False
> 
> while True:
>     displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord)
> 
>     guess = getGuess(missedLetters + correctLetters)
> 
>     if guess in secretWord:
>         correctLetters = correctLetters + guess
> 
>         foundAllLetters = True
>         for i in range(len(secretWord)):
>             if secretWord[i] not in correctLetters:
>                 foundAllLetters = False
>                 break
>         if foundAllLetters:
>             print('Yes! The secret word is "' + secretWord + '"! You win!')
>             gameIsDone = True
>     else:
>         missedLetters = missedLetters + guess
> 
>         if len(missedLetters) == len(HANGMAN_PICS) - 1:
>             displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord)
>             print('You have run out of guesses!')
>             print('The word was "' + secretWord + '"')
>             gameIsDone = True
> 
>     if gameIsDone:
>         if playAgain():
>             missedLetters = ''
>             correctLetters = ''
>             gameIsDone = False
>             secretWord = getRandomWord(words)
>         else:
>             break
> ```

---

#### **Chapter 8**: Writing the Hangman Code

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=138&selection=41,0,75,11&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.109]]
> > 
> > Lists are values that can contain other values. Methods are functions attached to a value. Lists have an append() method. Strings have lower(), upper(), split(), startswith(), and endswith() methods. You’ll learn about many more data types and methods in the rest of this book. The elif statement lets you add an “or else-if” clause to the middle of your if-else statements.
> 
##### Lists & Methods

This is a heavy coding chapter introducing data structures.

1. Lists ([]):
    A variable that holds multiple values. It is ordered.
    
    - `animals = ['cat', 'bat', 'rat']`        
    - We access items using an **index**: `animals[0]` is 'cat'.
    - **Slicing:** Getting a subsection of a list: `animals[1:3]`.
        
2. Methods:
    
    These are functions that belong to a specific data type.
    
    - **List Methods:** `.append()` (add item), `.reverse()` (flip order).
    - **String Methods:** `.split()` (turn string into list), `.upper()` (convert to uppercase).
        
3. The in Operator:
    Checks if a value exists inside a list or string. Returns True or False.

##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> HANGMAN_PICS = ['''
>   +---+
>       |
> ''']
> ```

> [!code]- Full Source Code — Hangman
> 
> ```python
> import random
> 
> HANGMAN_PICS = ['''
>   +---+
>       |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>   |   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  /    |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  / \  |
>      ===''']
> 
> words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard mole monkey mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
> 
> def getRandomWord(wordList):
>     wordIndex = random.randint(0, len(wordList) - 1)
>     return wordList[wordIndex]
> 
> def displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord):
>     print(HANGMAN_PICS[len(missedLetters)])
>     print()
> 
>     print('Missed letters:', end=' ')
>     for letter in missedLetters:
>         print(letter, end=' ')
>     print()
> 
>     blanks = '_' * len(secretWord)
> 
>     for i in range(len(secretWord)):
>         if secretWord[i] in correctLetters:
>             blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
> 
>     for letter in blanks:
>         print(letter, end=' ')
>     print()
> 
> def getGuess(alreadyGuessed):
>     while True:
>         print('Guess a letter.')
>         guess = input().lower()
>         if len(guess) != 1:
>             print('Please enter a single letter.')
>         elif guess in alreadyGuessed:
>             print('You have already guessed that letter. Choose again.')
>         elif guess not in 'abcdefghijklmnopqrstuvwxyz':
>             print('Please enter a LETTER.')
>         else:
>             return guess
> 
> def playAgain():
>     print('Do you want to play again? (yes or no)')
>     return input().lower().startswith('y')
> 
> print('H A N G M A N')
> missedLetters = ''
> correctLetters = ''
> secretWord = getRandomWord(words)
> gameIsDone = False
> 
> while True:
>     displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord)
> 
>     guess = getGuess(missedLetters + correctLetters)
> 
>     if guess in secretWord:
>         correctLetters = correctLetters + guess
> 
>         foundAllLetters = True
>         for i in range(len(secretWord)):
>             if secretWord[i] not in correctLetters:
>                 foundAllLetters = False
>                 break
>         if foundAllLetters:
>             print('Yes! The secret word is "' + secretWord + '"! You win!')
>             gameIsDone = True
>     else:
>         missedLetters = missedLetters + guess
> 
>         if len(missedLetters) == len(HANGMAN_PICS) - 1:
>             displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord)
>             print('You have run out of guesses!')
>             print('The word was "' + secretWord + '"')
>             gameIsDone = True
> 
>     if gameIsDone:
>         if playAgain():
>             missedLetters = ''
>             correctLetters = ''
>             gameIsDone = False
>             secretWord = getRandomWord(words)
>         else:
>             break
> ```

---

#### **Chapter 9**: Extending Hangman

> [!PDF|note] SUMMARY
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=149&selection=16,0,21,17&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.120]]
> 
> > Dictionaries are similar to lists except that they can use any type of value for an index, not just integers. The indexes in dictionaries are called keys. Multiple assignment is a shortcut to assign multiple variables the values in a list. 5

##### Dictionaries (`{}`)

Dictionaries are like Lists, but instead of using numbered indexes (0, 1, 2), they use **Keys** (which can be strings).

- **Structure:** `Key : Value` pairs.
- **Example:** `my_pet = {'size': 'fat', 'color': 'gray', 'disposition': 'loud'}`
- **Access:** `my_pet['color']` returns `'gray'`.

This chapter also introduced Multiple Assignment, a Python shortcut:

apples, bananas = 10, 5 (Assigns 10 to apples and 5 to bananas in one line).

##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> words = {'Colors': ['red','blue']}
> ```

> [!code]- Full Source Code — Category Hangman
> 
> ```python
> import random
> 
> HANGMAN_PICS = ['''
>   +---+
>       |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>       |
>       |
>      ===''', '''
>   +---+
>   O   |
>   |   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|   |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>       |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  /    |
>      ===''', '''
>   +---+
>   O   |
>  /|\  |
>  / \  |
>      ===''']
> 
> words = {
>     'Colors': 'red orange yellow green blue indigo violet'.split(),
>     'Shapes': 'square triangle rectangle circle ellipse'.split(),
>     'Fruits': 'apple orange lemon lime pear watermelon grape'.split(),
>     'Animals': 'bat bear beaver cat cougar crab deer'.split()
> }
> 
> def getRandomWord(wordDict):
>     wordKey = random.choice(list(wordDict.keys()))
>     wordIndex = random.randint(0, len(wordDict[wordKey]) - 1)
>     return [wordDict[wordKey][wordIndex], wordKey]
> 
> def displayBoard(HANGMAN_PICS, missedLetters, correctLetters, secretWord):
>     print(HANGMAN_PICS[len(missedLetters)])
>     print()
>     
>     print('Missed letters:', end=' ')
>     for letter in missedLetters:
>         print(letter, end=' ')
>     print()
>     
>     blanks = '_' * len(secretWord)
>     
>     for i in range(len(secretWord)):
>         if secretWord[i] in correctLetters:
>             blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
>     
>     for letter in blanks:
>         print(letter, end=' ')
>     print()
> ```

---
#### **Chapter 10**: Tic-Tac-Toe

> [!PDF|note] SUMMARY 
> 
> [[Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library).pdf#page=177&selection=108,0,122,11&color=note|Invent Your Own Computer Games with Python, 4th Edition (Al Sweigart) (Z-Library), p.148]]
> > 
> > Creating a program with AI comes down to carefully considering all the possible situations the AI can encounter and how it should respond in each of those situations. 
> > 
> > The Tic-Tac-Toe AI is simple because not as many moves are possible in Tic-Tac-Toe as in a game like chess or checkers. Our computer AI checks for any possible winning moves. Otherwise, it checks whether it must block the player’s move. Then the AI simply chooses any available corner space, then the center space, then the side spaces. 
> > 
> > This is a simple algorithm for the computer to follow. The key to implementing our AI is to make copies of the board data and simulate moves on the copy. That way, the AI code can see whether a move results in a win or loss. Then the AI can make that move on the real board. 
> > 
> > This type of simulation is effective at predicting what is or isn’t a good move.
> 

##### Artificial Intelligence (AI) & Logic

This isn't "machine learning"; it's **rule-based AI**. We teach the computer a strategy by giving it a checklist of priorities to follow:

1. **Check for a win:** Can I win on this move? If yes, take it.
2. **Block the player:** Can the player win on their next move? If yes, block them.
3. **Take Corners:** Corners are the most valuable spots in Tic-Tac-Toe.
4. **Take Center.**
5. **Take Sides.**

##### Short-Circuit Evaluation

Python is lazy (efficient).

- **OR:** If the first part of an `or` statement is `True`, Python skips checking the second part (because the whole thing is already True).
    
- **AND:** If the first part of an `and` statement is `False`, Python skips the second part.
    

This is useful for preventing errors (like checking if a list is empty before trying to access an item inside it).

##### SOURCE CODE

> [!example]- Short Snippet
> 
> ```python
> # Example of checking a winning move
> def isWinner(board, letter):
>     return (
>         (board[7] == letter and board[8] == letter and board[9] == letter) or
>         (board[4] == letter and board[5] == letter and board[6] == letter)
>     )
> ```

> [!code]- Full Source Code — Tic-Tac-Toe
> 
> ```python
> import random
> 
> def drawBoard(board):
>     print('   |   |')
>     print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
>     print('   |   |')
>     print('-----------')
>     print('   |   |')
>     print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
>     print('   |   |')
>     print('-----------')
>     print('   |   |')
>     print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
>     print('   |   |')
> 
> def inputPlayerLetter():
>     letter = ''
>     while not (letter == 'X' or letter == 'O'):
>         print('Do you want to be X or O?')
>         letter = input().upper()
>     if letter == 'X':
>         return ['X', 'O']
>     else:
>         return ['O', 'X']
> 
> def whoGoesFirst():
>     return 'computer' if random.randint(0, 1) == 0 else 'player'
> 
> def playAgain():
>     print('Play again? (yes or no)')
>     return input().lower().startswith('y')
> 
> def makeMove(board, letter, move):
>     board[move] = letter
> 
> def isWinner(board, le):
>     return ((board[7] == le and board[8] == le and board[9] == le) or
>             (board[4] == le and board[5] == le and board[6] == le) or
>             (board[1] == le and board[2] == le and board[3] == le) or
>             (board[7] == le and board[4] == le and board[1] == le) or
>             (board[8] == le and board[5] == le and board[2] == le) or
>             (board[9] == le and board[6] == le and board[3] == le) or
>             (board[7] == le and board[5] == le and board[3] == le) or
>             (board[9] == le and board[5] == le and board[1] == le))
> 
> def getBoardCopy(board):
>     return board.copy()
> 
> def isSpaceFree(board, move):
>     return board[move] == ' '
> 
> def getPlayerMove(board):
>     move = ' '
>     while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
>         print('Your next move? (1-9)')
>         move = input()
>     return int(move)
> 
> def chooseRandomMoveFromList(board, movesList):
>     possibleMoves = [move for move in movesList if isSpaceFree(board, move)]
>     return random.choice(possibleMoves) if possibleMoves else None
> 
> def getComputerMove(board, computerLetter):
>     playerLetter = 'O' if computerLetter == 'X' else 'X'
> 
>     # 1 — Win if possible
>     for i in range(1, 10):
>         copy = getBoardCopy(board)
>         if isSpaceFree(copy, i):
>             makeMove(copy, computerLetter, i)
>             if isWinner(copy, computerLetter):
>                 return i
> 
>     # 2 — Block player
>     for i in range(1, 10):
>         copy = getBoardCopy(board)
>         if isSpaceFree(copy, i):
>             makeMove(copy, playerLetter, i)
>             if isWinner(copy, playerLetter):
>                 return i
> 
>     # 3 — Take corner
>     move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
>     if move:
>         return move
> 
>     # 4 — Take center
>     if isSpaceFree(board, 5):
>         return 5
> 
>     # 5 — Take sides
>     return chooseRandomMoveFromList(board, [2, 4, 6, 8])
> 
> def isBoardFull(board):
>     return all(board[i] != ' ' for i in range(1, 10))
> 
> print('Tic-Tac-Toe')
> 
> while True:
>     theBoard = [' '] * 10
>     playerLetter, computerLetter = inputPlayerLetter()
>     turn = whoGoesFirst()
>     print('The ' + turn + ' will go first.')
>     gameIsPlaying = True
> 
>     while gameIsPlaying:
>         if turn == 'player':
>             drawBoard(theBoard)
>             move = getPlayerMove(theBoard)
>             makeMove(theBoard, playerLetter, move)
> 
>             if isWinner(theBoard, playerLetter):
>                 drawBoard(theBoard)
>                 print('You won!')
>                 gameIsPlaying = False
>             else:
>                 if isBoardFull(theBoard):
>                     drawBoard(theBoard)
>                     print('The game is a tie!')
>                     break
>                 else:
>                     turn = 'computer'
> 
>         else:
>             move = getComputerMove(theBoard, computerLetter)
>             makeMove(theBoard, computerLetter, move)
> 
>             if isWinner(theBoard, computerLetter):
>                 drawBoard(theBoard)
>                 print('The computer wins!')
>                 gameIsPlaying = False
>             else:
>                 if isBoardFull(theBoard):
>                     drawBoard(theBoard)
>                     print('The game is a tie!')
>                     break
>                 else:
>                     turn = 'player'
> 
>     if not playAgain():
>         break
> ```

---
# 📘 Unified Summary: Chapters 1–10

Chapters 1 to 10 of *Invent Your Own Computer Games with Python* built a complete foundation for my understanding of how programming works. Instead of dry theory, I used simple games as the main learning method. Each chapter expanded my skills and showed me how real programs are structured—from basic input/output to full game loops, decision-making, and simple AI.

> [!SUMMARY] Core Takeaway
> The biggest strength of these chapters is how they connect fundamental Python concepts to actual game mechanics. This made the learning process practical and memorable for me.

---

## 🌟 What I Learned (Chapters 1–10)

### 1. Python Basics & Interaction
I started by learning how the Python interpreter works, how expressions evaluate, and how variables store values. I used the interactive shell to experiment.
* **Key Lesson:** Computers only do *exactly* what I tell them. My instructions must be precise.

### 2. Input, Output, and Strings
I learned how programs communicate with the user. This forms the foundation of all interactive programs I write.
* `input()`: For receiving text from the player.
* `print()`: For displaying output to the screen.
* **Escape characters:** Using `\n`, `\\`, and `\'` for text formatting.

### 3. Flow Control & Program Logic
I learned how to make my program make decisions and control the flow. This allowed me to build my first real game: **Guess the Number**.
* **Conditionals:** `if`, `elif`, `else`.
* **Loops:** `while` loops.
* **Boolean Logic:** Handling `true`/`false` expressions.

### 4. Functions & Code Organization
I learned to break large programs into smaller, reusable pieces using `def`. This drastically improved the organization and readability of my code.
* Parameters & arguments.
* Return values.
* **Scope:** Understanding local vs. global variables.

### 5. Randomness & Game Elements
Using Python’s `random` module, I implemented unpredictability to keep games engaging.
* *Examples:* Generating random secret numbers or determining if a dragon is friendly or hostile.
* **Takeaway:** This taught me how games simulate chance.

### 6. Debugging Skills
I learned to identify the three categories of bugs. I began thinking like a developer—observing behavior, tracing execution, and inspecting variables.
1.  **Syntax errors:** Typos or grammar mistakes.
2.  **Runtime errors:** Crashes during execution.
3.  **Semantic errors:** Logic mistakes (the hardest to find).

### 7. Lists, Slicing & Data Management
I learned how to store multiple items using lists `[]`. These skills were heavily used in the **Hangman** project to manage missed letters and ASCII art.
* Indexing and Slicing.
* Appending items.

### 8. Dictionaries & Categorized Data
Dictionaries introduced a more powerful structure using **key–value pairs**.
* *Example:* `{'Colors': ['red', 'blue'], 'Animals': ['cat', 'bear']}`
* **Takeaway:** This taught me how to group related data, preparing me for complex real-world applications.

### 9. Game Loop Structure
I realized that all games I build follow the same key structure. This is critical for my future work with Pygame.
1.  **Setup:** Initialize variables.
2.  **Main Loop:** Handle player turns and check game state.
3.  **Win/Lose Detection:** Check if the game is over.
4.  **Restart:** Option to play again.

### 10. Simple AI & Strategy (Tic-Tac-Toe)
I implemented a rule-based AI that follows logical steps. It wasn't machine learning, but it taught me how to translate strategy into code.
* **The Logic:**
    1.  Can I win? -> Take the winning move.
    2.  Can the player win? -> Block them.
    3.  Take a corner -> Center -> Sides.

---

## ⭐ Why These Chapters Matter
* **Practicality:** I learned programming through real games, not boring theory.
* **Progression:** Concepts built on each other steadily.
* **State Management:** I now understand how to track the "state" of a game.
* **Debugging:** I gained the ability to trace and fix my own errors.
* **Organization:** I have experience structuring code, which prepares me for larger projects.
* **Data Structures:** I saw how lists and dictionaries affect game design in real scenarios.
* **Confidence:** I built full, working games entirely in Python.

---

## 🎯 How This Prepares Me for Pygame
Everything I learned here—logic, flow control, game loops, input handling, state tracking, and simple AI—translates directly to Pygame.

> [!INFO] Transition to GUI
> The only big difference in Pygame is **graphical rendering**. The core logic stays the same.

**I now have the foundation to:**

* [x] Build interactive systems.
* [x] Manage game states.
* [x] Handle user input.
* [x] Organize large programs.
* [x] Write basic AI.
* [x] Debug effectively.

---

