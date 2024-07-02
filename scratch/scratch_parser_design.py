from pyparse import (
    Grammar,
    Tokenizer,
    ShiftReduceParser,
    Parser,
    TransitionError
)
from .scratch_parser_automaton import ParserAutomaton
from pyparse.library import (
    PyChannels,
    PyChannel,
    PySignal,
    PySynchronyEventLoop,
    PySynchronyContext
)
from .utils import generate_id, apply_color, underline_text, bold_text, center_text


class Parser:

    __slots__ = ("_parser_id", "_event_loop")

    def __init__(self, automaton=None, parser_id=None):
        self._parser_id = parser_id or generate_id()
        self._event_loop = PySynchronyEventLoop(loop_id=self.parser_id)
        self._automaton = automaton or ParserAutomaton()
        self._automaton.set_parser(self)

    @property
    def parser_id(self):
        return self._parser_id


if __name__ == "__main__":
    pass
