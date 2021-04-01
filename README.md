# DECEV (*dec*orator *ev*ents) by @dantechguy

A teeny library for event handling which uses decorators for event subscription

## Installation

Either copy decev/decev.py into your directory, or run

```
pip install decev
```

then import into your file with `import decev`

## Usage

**1. Create an EventHandler object**

```py
import decev
# pass list of event names
events = decev.EventHandler()
```

**2. Add functions to events**

*Event functions cannot have any arguments*

```py
# add myFunction to firstEvent
@events.firstEvent
def myFunction():
    print('myFunction')
    
# add myOtherFunction to firstEvent and event_two
@events.firstEvent
@events.event_two
def myOtherFunction():
    print('myOtherFunction')
```

**3. Add methods to events**

*Methods can only have the `self` argument*

```py
# class decorator is required for methods to work
@events.cls
class MyClass:
    def __init__(self):
        print('initialised!')
        
    # add myMethod to LAST_EVENT
    @events.LAST_EVENT
    def myMethod(self):
        print('myMethod')
        
    # and unbound methods work too
    @events.LAST_EVENT
    def myOtherMethod():
        print('myOtherMethod')

# create instance of class        
myObject = MyClass()
```

**4. Run events**

```py
print()
events.run('firstEvent')
print()
events.run('event_two')
print()
events.run('LAST_EVENT')
```

Which produces this:

```
> py main.py
initialised!

myOtherFunction
myFunction

myOtherFunction

myMethod
myOtherMethod
```

## How it works

Any functions added with **zero** arguments are assumed to be regular functions, and are subscribed immediately to the event.

<br>

Any functions added with **one** argument are assumed to be methods (the argument being `self`), and are *tagged* with the events. The class decorator inserts some code into the class' `__init__` method to automatically subscribe these tagged methods once an instance has been created. 

The reason methods cannot be subscribed immediately, is that at the time of decorator execution no instance has been created, so the `self` parameter has not been filled, so the method is **unbound** and will not run properly. Therefore, the method can only be subscribed after instantiation.
