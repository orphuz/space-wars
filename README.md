# space-wars
A small 2d game based on the turtle library for the purpose  of self education in python. This project focuses on being a platform to implement serveral development principles, python functionality and standart libraries.

### Design principles
* Object oriented programming (e.g. game, sprite and state classes)
* Class inheritage (different type of sprites)
* Modules
* Finite state machine (game states runninng, paused etc.)

### Python functionality
* Function decorators (e.g. @property)
* class methods (e.g. sprite spawning)

### Python standart libraries
* os
* sys
* time
* import
* random
* logging
* import pickle
* turtle


# Dependencies
* Python3
* Pyhton3-TK
* pip install coverage

## How to:
### Run all tests from project folder
```
python -m unittest discover -s 'tests'
```

### Calculate and report test coverage
```
coverage run -m unittest discover -s 'tests'
coverage report
coverage html
```





