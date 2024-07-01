# TODO: perhaps update name of class 'AugmentedGrammarRule' to 'GrammarItem' or 'AugmentedGrammarItem' or 'ParseTableItem' or 'ParseItem'


class AugmentedGrammarRule:

    __slots__ = ("_grammar_rule",)

    def __init__(self, grammar_rule):
        self._grammar_rule = grammar_rule


if __name__ == "__main__":
    pass
