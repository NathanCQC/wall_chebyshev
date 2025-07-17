from guppylang import guppy
from guppylang.std.builtins import comptime
from guppylang.std.quantum import qubit, measure_array
from guppylang.std.builtins import array, exit
from typing import Callable

n_state_qubits = guppy.nat_var('n_state_qubits')
n_prep_qubits = guppy.nat_var('n_prep_qubits')
n_product_terms = guppy.nat_var('n_product_terms')

@guppy
def product_block_encoding(prod_block_encoding: array[Callable[[array[qubit, n_prep_qubits], array[qubit, n_state_qubits]], None], n_product_terms], state_qreg: array[qubit, n_state_qubits]) -> None:
    
    for prod_block in prod_block_encoding.copy():

        prep_qreg = array(qubit() for _ in range(comptime(n_prep_qubits)))
        prod_block(prep_qreg, state_qreg)

        outcome = measure_array(prep_qreg)
        # result("c", measure_array(prep_qubits))
        for b in outcome: 
            if b:
                exit("circuit failed",1)