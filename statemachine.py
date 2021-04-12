# -------------------------------------------------------------------------------
# Name:         statemachine
# Purpose:      Class that creates and operates a general state machine
# Author:       Tony
# Created:      16/10/2015
# Copyright:    (c) Tony 2015
# Licence:      Free to use
# -------------------------------------------------------------------------------

# ! /usr/bin/env python

""" Implements a state machine
    Dependencies : None
"""


class StateMachine:
    """ Class to execute a FSM """
    __slots__ = ['entity', 'states', 'transitions', 'start_state', 'end_states',
                 'current_state', 'previous_state', 'state_class', 'triggers',
                 'global_class', 'global_triggers', 'finished']

    def __init__(self, entity):

        self.entity = entity  # owner of FSM

        self.states = {}  # dictionary holding details of states
        self.transitions = {}  # dictionary holding details of transitions

        self.start_state = None  # start FSM here
        self.end_states = []

        self.current_state = None  # present state (name)
        self.previous_state = None  # previous state (name)
        self.state_class = None  # current state class
        self.triggers = None  # list of triggers to leave state

        self.global_class = None  # Global state polled continually
        self.global_triggers = None  # Triggers for global state

        self.finished = False   # Finished flag set when end state reached

    def add_state(self, name, handler, transitions):
        """ add_state(Name of state, state class, list of exit triggers)
            Each transition listed must have an entry in the transition dictionary
            add state to dictionary as - name is key: [class name, list of transitions] """
        name = name.upper()
        transitions = [x.upper() for x in transitions]
        self.states[name] = [handler]
        self.states[name].append(transitions)

    def add_transition(self, name, trigger, state):
        """ add_transition(Name of transition, boolean test function, destination state)
            Must be a transition entry for each named transition in state transition lists
            add transition to dictionary as - name is key: [trigger function, list of destination state] """
        name = name.upper()
        state = state.upper()
        self.transitions[name] = [trigger]
        self.transitions[name].append(state)

    def set_start(self, name):
        """ set start state for FSM """
        self.start_state = name.upper()

    def set_end(self, names):
        """ set start state for FSM """
        for name in names:
            self.end_states.append(name.upper())

    def run(self):
        """ start FSM running """
        try:
            _ = self.states[self.start_state]
        except KeyError:
            raise ValueError("must call .set_start() before .run()")
        self.global_class = self.states.get("GLOBAL")

        self.current_state = self.start_state
        self._get_state_details()
        self.state_class.enter()
        if self.global_class is not None:
            self._get_global_details()

    def update(self):
        """ update FSM by checking all triggers for current state
            if global state specified this is always executed first """
        if self.global_class is not None:
            self.global_class.execute(self.current_state)
            (reason, trigger, newstate) = self._check_triggers(self.global_triggers)
            if reason is not None:
                self._change_state(newstate, reason)
        self.state_class.execute()
        (reason, trigger, newstate) = self._check_triggers(self.triggers)
        if reason is not None:
            self._change_state(newstate, reason)
        if self.current_state in self.end_states:
            self.finished = True

    def _get_state_details(self):
        """ get state details from dictionary and initialise class """
        (self.state_class, self.triggers) = self.states[self.current_state]
        self.state_class = self.state_class(self.entity)

    def _get_global_details(self):
        """ activate global class """
        (self.global_class, self.global_triggers) = self.states["GLOBAL"]
        self.global_class = self.global_class(self.entity)

    def _check_triggers(self, trig):
        """ check all triggers: returns t as None if none triggered """
        (t, trigger, state) = (None, None, None)
        if trig:
            for t in trig:
                (trigger, state) = self.transitions[t]
                if trigger():
                    break
                else:
                    t = None
        return t, trigger, state

    def _change_state(self, newstate, trigger):
        """ change to new state """
        print(self.current_state, "->", newstate)
        self.state_class.exit(trigger)
        if newstate == "RETURN":
            newstate = self.previous_state
        self.previous_state = self.current_state
        self.current_state = newstate
        self._get_state_details()
        self.state_class.enter()
