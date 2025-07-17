from guppylang import guppy
from guppylang.std.builtins import comptime
from guppylang.std.quantum import qubit, measure_array
from guppylang.std.builtins import array, exit
from typing import Callable

n_state_qubits = guppy.nat_var('n_state_qubits')
n_prep_qubits = guppy.nat_var('n_prep_qubits')

@guppy
def power_block_encoding(power:int, block_encoding: Callable[[array[qubit, n_prep_qubits], array[qubit, n_state_qubits]], None], state_qreg: array[qubit,n_state_qubits]) -> None:

    for i in range(power):

        prep_qreg = array(qubit() for _ in range(comptime(n_prep_qubits)))
        block_encoding(prep_qreg, state_qreg)
        
        outcome = measure_array(prep_qreg)
        # result("c", measure_array(prep_qubits))
        for b in outcome: 
            if b:
                exit("circuit failed",1)