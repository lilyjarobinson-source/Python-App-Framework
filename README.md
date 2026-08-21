# Menu framework

A lightweight tkinter based python application framework.

## General Structure

This framework uses a single main class that uses polymorphism to treat all menus the same way and allow the user to develop menu specific code seperate from the overall app function.

The Main class holds all the menus, controls which menu is currently rendered, controls the updates of runable menus and holds the root tkinter window.

Each menu is a subclass of the Menu class which gives it the basic functionality to be used by the main class.

Each menu can hold icons which are wrapper classes for tkinter widgets. Currently supported:
- Labels
- Buttons
- Entry boxes
- Option Boxes
- List boxes
- Canvas
- Images

## Usage
### Getting started

Place the framework folder into your project scope. Such as:

- project
    - framework
    - Menus
        - Menu1
        - Menu2
        - Icon file.txt
    - Application.py

Then your Application.py should read as:
```
import sys
sys.path.append("project/framework")
sys.path.append("project/Menus")
from Main import main
from Menu1 import menu1
from Menu2 import menu2

main = main("test", "800x500")

menu1 = menu1()
menu2 = menu2()

main.assignMenus([menu1, menu2])
main.assignIconFileLocation("project/Menus")
main.activate()
main.root.mainloop()
```
You first import then instantiate main and all the menus.<br>
Then you assign all the menus in main which gives it access to the classes.<br>
Now you assign the location of the icon file menu that main will read from.<br>
Finally you activate main and set it's root to loop to run the program.<br>

### Personalisation

As Main and Menu are classes it is possible to polymorphise these into your application specific versions.

### Menus

For each menu the main functions to mutate are:
- initialise - ran when the menu is loaded
- uninitialise - ran when the menu is unloaded
- assignIconFunctions - used to assign functions to icons such as button and entry boxes
- reload - used to reload the menu
- runInitialisation - ran when the menu begins running (if runable is true)
- runDeinitialisation - ran when the menu stops running (if runable is true)
- update - ran while the menu is running (if running is true)

### The icon file

The icon file is where you define your icons to be rendered in the menus.
The syntax is
```
M:{Menu name}
{Icon name}::{Icon type},,{Icon x position},,{Icon y position},,{Icon width},,{Icon Height}
```
For each icon type the syntax ranges but that is the base syntax for an icon.<br>
For each icon see:
```
M:menu1
label1::label,,1,,1,,100,,19,,label text
button1::button,,1,,21,,100,,19,,button text
entry1::entry,,1,,41,,100,,19
optionBox1::optionBox,,1,,61,,100,,19,,Default option,,Default option,,Option 1,,Option 2...
listBox1::listBox,,1,,61,,100,,19
canvas1::canvas,,1,,81,,100,,19
M:menu2
image1::image,,1,,101,,100,,19
```
An icon can also be assigned to multiple menus using:
```
M:menu1,menu2
label2::label,,101,1,100,19,,different label text
```

### Assigning icon functions

Buttons, entrys, option boxes, list boxes and canvases can be assigned functions.<br>
| icon | Function |
| ---| --- |
| button | bindFunction(fun) |
| entry | bindFunctionToKeypress(fun) |
| optionBox | bindFunctionToKeypress(fun) |
| listBox | bindFunctionToChange(fun) |
| canvas | bindFuncitonToMouseEvent(fun) |

