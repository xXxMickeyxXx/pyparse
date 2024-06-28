def generate_item_sets(grammar, start_symbol="$") -> None:
    # TODO: create 'GOTO' table - after generating item sets/states,
    #       iterate through them, performing the searches 

    # TODO: be wary of how the below logic (as well as the lib logic
    #       in general) handles concurrency/parallelism

    # TODO: ?? possibly create a stack implementation (possibly
    #       optimized for this lib, perhaps implement in the c
    #       programming language) ??

    # TODO: ?? create a buffer design (possibly optimized for this
    #       lib, perhaps implement in the c programming language) ??

    # TODO: fix goto logic as current implementation is missing some of the
    #       goto transitions for certain state/symbol combinations

    # TODO: add small runtime optimizations (like aliases for methods to reduce
    #       lookup times)



    result_buffer = CircularBuffer(1)
    TABLE_CHANNEL.emit(TableConstructionEvent.INIT_I0, grammar, result_buffer, start_symbol=start_symbol)


    _current_state, _init_i0_items = result_buffer.dequeue(default=(0, []))
    _item_states = {_current_state: _init_i0_items}
    TABLE_CHANNEL.emit(TableConstructionEvent.UPDATE_STATES, _current_state, _item_states[_current_state], result_buffer=None)


    _new_state_added = True
    while _new_state_added:
        _new_state_added = False

        for _state, _items in list(_item_states.items()):
            _next_states = [(i.next_symbol(default=None), i) for i in _items if not i.at_end]
            for _next_symbol, _next_item_rule in _next_states:
                _goto_result = goto(_state, _next_item_rule)
                if _goto_result is None:
                    continue

                _new_state, _new_item_group = _goto_result
                if _new_state not in _item_states:
                    _item_states[_new_state] = _new_item_group
                    GOTO_MAPPING[(_state, _next_symbol)] = _new_state
                    _new_state_added = True
                else:
                    GOTO_MAPPING[(_state, _next_symbol)] = _new_state