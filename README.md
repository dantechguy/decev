# DECEV (*dec*orator *ev*ents) by @dantechguy

A teeny library for event handling which uses decorators for event subscription

## Overview

- Add functions to events with `@event.your_event` decorators
- Add instance methods to events with `@event.m.your_event` decorators
- Run events with `event.run('your_event')`
- Pass arguments with events with `event.run('your_event', 'bar', foo=True)`

## Installation

Either copy decev/decev.py into your directory, or run

```
pip install decev
```

then import into your file with `import decev`

## Usage

**1. Create an EventHandler object**

```python
import decev
events = decev.EventHandler()
```

**2. Add functions to events**

*A single function can have multiple events*

```python
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

*Use `@events.m.your_event` to add methods with `self` parameter*

```python
class MyClass:      
    # add myMethod to THIRD_EVENT
    @events.m.firstEvent
    @events.m.THIRD_EVENT
    def myMethod(self):
        print('myMethod')
        
    # add unbound myOtherMethod to THIRD_EVENT
    @events.THIRD_EVENT
    def myOtherMethod():
        print('myOtherMethod')

# create instance of class        
myObject = MyClass()
```

**4. Receive arguments in callbacks**

*Make sure the parameters match the arguments passed into `events.run()`*

```python
@events.ArgEvent
def myArgFunction(foo, bar=True):
    print(f'myArgFunction foo={foo} bar={bar}')
``` 

**5. Run events**

```python
events.run('firstEvent')
print()
events.run('event_two')
print()
events.run('LAST_EVENT')
print()
events.run('ArgEvent', 100, bar=False)
```

Which produces this:

```
> py main.py
myOtherFunction
myFunction

myOtherFunction

myOtherMethod
myMethod

myArgFunction foo=100 bar=False
```

## How it works

All functions added with `@events.your_event` are subscribed immediately to `events`'s callback dictionary.

As instance methods require the `self` parameter, they can only be subscribed once the class has been instantiated and `self` has a value. The alternate `@events.m.your_event` syntax instead *tags* the method, storing the event names and event handler, and inserts a code snippet into the object's `__init__` method to subscribe the events on instantiation.