## 0.1.1

- Initial decorator syntax
- Used `events.subscribe_tagged_methods()` method for classes 
- Didn't allow any arguments

## 1.0.0

- Replaced `events.subscribe_tagged_methods()` with the `events.cls` class decorator
- Simplified internal code

## 1.1.0

- Removed the `events.cls` class decorator
- Allowed classes to subscribe to different `EventHandlers`'s events
- Allowed events to pass arguments
- (And therefore) require users to add methods with `@events.m.EVENT_NAME` syntax

## 1.2.0

- Added `decev.cls` class decorator
- Simplified internal code