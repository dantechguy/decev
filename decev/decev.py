_tag = '__events'
_init_tag = '__custom_init'


class EventHandler:
    def __init__(self):
        self._events = {}  # { 'event1': { <function object>, <function object>} }
        self.m = self.method = MEventHandler(self)

    def run(self, event_name, *args, **kwargs):
        for callback in self._events.get(event_name, []):
            callback(*args, **kwargs)

    def add(self, event_name, fn):
        if event_name not in self._events:
            self._events[event_name] = set()
        self._events[event_name].add(fn)

    def __getattr__(self, event_name):  # function decorator
        def decorator(fn):
            self.add(event_name, fn)
            return fn

        return decorator


class MEventHandler:
    def __init__(self, event_handler):
        self.handler = event_handler

    def __getattr__(self, event_name):  # method decorator
        return MethodDecorator(self.handler, event_name)


class MethodDecorator:
    def __init__(self, event_handler, event_name):
        self.handler = event_handler
        self.name = event_name

    def __call__(self, fn):
        event_dict = getattr(fn, _tag, {})  # { <EventHandler object>: [ 'event1', 'EVENT_TWO' ], }
        event_dict[self.handler] = event_dict.get(self.handler, []) + [self.name]
        setattr(fn, _tag, event_dict)

        self.fn = fn

        return self  # ???

    def __set_name__(self, owner, name):
        old_init = owner.__init__

        # if __init__ is not already customised
        if not hasattr(old_init, _init_tag):

            # this is the new __init__ for the class
            def new_init(obj, *args, **kwargs):  # obj -> self
                # get all methods in object
                for method_name in dir(obj):
                    method = getattr(obj, method_name)
                    # get method's `_event` event dictionary
                    event_dict = getattr(method, _tag, {})
                    # for each handler in the dict
                    for event_handler, event_names in event_dict.items():
                        # and for each event in each handler
                        for event_name in event_names:
                            # add the method to that handler's event
                            event_handler.add(event_name, method)

                # and run the old __init__ as if nothing happened (don't replace in case they want to re-run this)
                old_init(obj, *args, **kwargs)

            # set this attribute to prevent another new_init from being added
            setattr(new_init, _init_tag, True)
            owner.__init__ = new_init

        setattr(owner, name, self.fn)



