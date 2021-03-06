from __future__ import print_function

from abc import ABCMeta, abstractmethod
from datetime import datetime

try:
    import Queue as queue
except ImportError:
    import queue

from Events import FillEvent, OrderEvent

class ExecutionHandler(object):
    """
    The ExecutionHandler abstract class handles the interaction
    between a set of order objects generated by the Portfolio and
    the ultimate set of Fill objects that actually occurs in the
    market.
    The handlers can be used to subclass simulated brokerages
    or live brokerages, with identical interfaces. This allows
    strategies to be backtested in a very similar manner to a live
    trading engines
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        """
        Takes an Order event and executes it, producing
        a Fill event that gets placed onto the Events queue.
        
        Parameters:
        event - Contains an Event object with order information.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimpleSimulatedExecutionHandler(ExecutionHandler):
    """
    The simulated execution handler simply converts all order
    objects into their equivalent fill objects automatically
    without latency, slippage or fill-ratio issues.
    This allows a straightforward "first go" test of any strategy,
    before implementation with a more sophisticated execution
    handler.
    """

    def __init__(self, events):
        """
        Initialises the handler, setting the event queues
        up internally.
        
        Parameters:
        events - The Queue of Event objects.
        """
        self.events = events

    def execute_order(self, event):
        """
        Order event converted to Fill event to
        execute the order on "live" broker

        Parameters:
        event - Contains an Event object with order information.
        """
        
        if isinstance(event, OrderEvent):
            fill_event = FillEvent(datetime.utcnow(), event.symbol, "ARCA", event.quantity, event.direction, None) # ARCA used as reference e.g.
            self.events.put(fill_event)