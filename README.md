# DECEV (**dec**orator **ev**ents) by @dantechguy

A teeny library for event handling which uses decorators for event subscription

## Installation

Either copy decev/decev.py into your directory, or run

```
pip install decev
```

then import into your file with `import decev`

## Usage

**1. Create an EventHandler object and events**

```py
import decev
# pass list of event names
events = decev.EventHandler(['firstEvent', 'event_two', 'LAST_EVENT'])
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
class MyClass:
    def __init__(self):
        # this must be run for methods to be subscribed
        events.subscribe_tagged_methods(self)
        
    # add myMethod to LAST_EVENT
    @events.LAST_EVENT
    def myMethod(self):
        print('myMethod')

# create instance of class        
myObject = MyClass()
```

**4. Run events**

```py
events.run('firstEvent')
print()
events.run('event_two')
print()
events.run('LAST_EVENT')
```

Which produces this:

```
> py main.py
myOtherFunction
myFunction

myOtherFunction

myMethod
```

## How it works

Any functions added with **zero** arguments are assumed to be regular functions, and are subscribed immediately to the event.

<br>

Any functions added with **one** argument are assumed to be methods (the argument being `self`), and are *tagged* with the corresponding event. Later, when `subscribe_tagged_methods` is called, all tagged methods are then subscribed to the event.

The reason we tag *then* subscribe for methods is because when the function would *usually* be subscribed, there is no value for `self` (there isn't an instance), so the method is *unbound*. Only once an instance has been created, we run `subscribe_tagged_methods` in its `__init__` to successfully subscribe all methods now that there is a value for `self`.
