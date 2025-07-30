from wallcheb.qtmlib.circuits.lcu import LCUMultiplexorBox
from guppylang import guppy
from guppylang.std.builtins import comptime, array
from guppylang.std.quantum import qubit, x, discard_array
from typing import Callable
from guppylang.std.debug import state_result
from wallcheb.operators import generate_pytket_hvs_hubbard
from wallcheb.guppy import product_block_encoding
from wallcheb.utils import compute_expectation, build_multiplexor_lcu, get_state_vector
from hugr.qsystem.result import QsysResult
import pandas as pd


def wallcheb_hubbard_circ(m: int, u: float, n_sites: int):

    product_block_encoding_qpo, _ = generate_pytket_hvs_hubbard(u, n_sites, m)
    
    n_state_qubits = 2*n_sites

    lcu_box = LCUMultiplexorBox(product_block_encoding_qpo[0], n_state_qubits)
    n_prep_qubits = lcu_box.n_prepare_qubits


    @guppy.comptime
    def guppy_prod_circs() -> array[Callable[[array[qubit, comptime(n_prep_qubits)], array[qubit, comptime(n_state_qubits)]],None], comptime(m)]:

        guppy_circuits = [build_multiplexor_lcu(qpo, n_state_qubits, i) for i, qpo in enumerate(product_block_encoding_qpo)]
        return guppy_circuits

            
    @guppy
    def main() -> None:
        """Main function to run the multiplexor LCU circuit."""
        state_qreg = array(qubit() for _ in range(comptime(n_state_qubits)))

        x(state_qreg[0])
        x(state_qreg[3])

        prods = guppy_prod_circs()

        product_block_encoding(prods, state_qreg)

        state_result("gs", state_qreg)

        # result('c',measure_array(state_qreg))
        discard_array(state_qreg)
        return

    return guppy.compile(main), n_prep_qubits + n_state_qubits


def run_wallcheb_hubbard(m, u, n_sites, hubbard_hamiltonian):
    compiled_hugr, n_qubits = wallcheb_hubbard_circ(m, u, n_sites)
    sv = get_state_vector(compiled_hugr, n_qubits, n_shots=5000000)
    # print(f"State vector: {sv}")
    expectation_value = compute_expectation(sv, hubbard_hamiltonian)
    return sv, expectation_value



u = 1.0
n_sites = 2

_ , hubbard_hamiltonian = generate_pytket_hvs_hubbard(u, n_sites, 1)

results = []

min_m = 7
max_m = 8

for m_val in range(min_m, max_m + 1):
    sv, expectation_value = run_wallcheb_hubbard(m_val, u, n_sites, hubbard_hamiltonian)
    results.append({
        'm': m_val,
        'expectation_value': expectation_value.item().real,
        'sv': sv
    })
    df = pd.DataFrame(results)
    df.to_csv('wallcheb_hubbard_results.csv', index=True)


