"""

__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        S ---> aA
        A ---> b


    AUGMENTED TEST GRAMMAR:
        S ---> .S
        S ---> .aA
        A ---> .b


        I0:
            S ---> .S
            S ---> .aA
            A ---> .b

        I1:
            S ---> S.

        I2:
            S ---> a.A
            A ---> .b

        I3:
            A ---> b.


        EXAMPLE INPUT ---> ab

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


        EXAMPLE INPUT 2 ---> abbA

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (2, a), (3, A)]

                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> 0
        B ---> 1
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        S ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .0
        B ---> .1
        B ---> .(E)


        I0:
            KERNEL
                S ---> .E
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
                B ---> .0
                B ---> .1
                B ---> .(E)
            TRANSITIONS
                GOTO(0, E) = 1
                GOTO(0, B) = 4


        I1:
            KERNEL
                S ---> E.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(I1, S) = ACCEPT

        I2:
            KERNEL
                E ---> E .* B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I3:
            KERNEL
                E ---> E .+ B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I4:
            KERNEL:
                E ---> B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(4, E)

        I5:
            KERNEL
                B ---> 0.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I6:
            KERNEL
                B ---> 1.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I7:
            KERNEL
                B ---> (.E)
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
            TRANSITIONS
                NONE
            ACTION(S)

        I8:
            KERNEL
                E ---> E * .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(7, B) = 9
            ACTION(S)


        I9:
            KERNEL
                E ---> E + .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(8, B) = 10
            ACTION(S)


        I10:
            KERNEL
                E ---> E * B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I11:
            KERNEL
                E ---> E + B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)



    INIT:

        • Parser initializes, adding initial state/accept symbol to the stack

    PARSE

        • Parser 



__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> number
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        E ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .NUMBER
        B ---> .(E)


         I0:
            E ---> .E (augmented grammar start symbol)
            E ---> .E * B
            E ---> .E + B
            E ---> .B
            B ---> .NUMBER
            B ---> .(E)

                TRANSITIONS (from I0)
                    GOTO(0, E) = 1
                    GOTO(0, B) = 4
                    GOTO(0, NUMBER) = 


        I1:
            E ---> E.
                
                ACTION: ACCEPT


        I2:
            E ---> E .* B

"""

from .grammar_rule import GrammarRule
from .grammar_designing import Grammar


def grammar_factory():
    return Grammar(grammar_id="[GRAMMAR_AS_OF_2024_06_13]")


def init_grammar(grammar):
    # (NOTE: augmented each instance of a 'GrammarRule' in order to prepare
    #        for parse table construction)

    # (NOTE: check docstring at top of this module for the test grammar
    #        definition, just below the end line, where states "TEST GRAMMAR")


    # Augmented initial/starting production
    _initial_item = GrammarRule("$", ["S"])
    _initial_item.augment()
    grammar.add_rule(_initial_item)

    # Actual first grammar rule
    _S_rule = GrammarRule("S", ["a", "A"])
    _S_rule.augment()
    grammar.add_rule(_S_rule)

    # Final grammar rule for test grammar
    _A_rule = GrammarRule("A", ["b"])
    _A_rule.augment()
    grammar.add_rule(_A_rule)


if __name__ == "__main__":
    pass
