from compilation_utils.tokens import LexicalTokens
from abc import abstractmethod


class State(object):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass


class KeywordState(State):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass


class OperatorState(State):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass


class IdentifierState(State):
    def __init__(self):
        super(IdentifierState, self).__init__()


class LiteralState(State):
    def __init__(self):
        super(LiteralState, self).__init__()


class StringLiteralState(State):
    def __init__(self):
        super(StringLiteralState, self).__init__()


class Transition(object):
    def __init__(self, to_state):
        self.to_state = to_state

    def execute(self):
        pass


class StateMachine(object):
    def __init__(self, logic_stack):
        self.logic_stack = logic_stack
        self.states = {}
        self.transitions = {}
        self.curr_state = None
        self.curr_trans = None

    def set_state(self, state_name: str):
        self.curr_state = self.states[state_name]

    def transition(self, trans_name):
        self.curr_trans = self.transitions[trans_name]

    def execute(self):
        if self.curr_trans:
            self.curr_trans.execute()
            self.set_state(self.curr_trans.to_state)
            self.curr_trans = None
        self.curr_state.execute()


class StackStateMachine(object):
    def __init__(self):
        self.state_machine = StateMachine(self)
        self.type_stack = []


if __name__ == "__main__":
    stack_machine = StackStateMachine()

    stack_machine.state_machine.states[LexicalTokens.KEYWORD] = KeywordState()
