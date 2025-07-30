from hugr.qsystem.result import QsysResult
from selene_sim import build, Quest
from pytket.passes import AutoRebase
from pytket import OpType
from pytket.passes import DecomposeBoxes
import numpy as np
from wallcheb.qtmlib.circuits.lcu import LCUMultiplexorBox
from guppylang import guppy

def get_state_vector(compiled_hugr, n_qubits, n_shots=25000, ):
    runner = build(compiled_hugr)
    shots = QsysResult(
        runner.run_shots(
            Quest(), n_qubits=n_qubits, n_shots=n_shots
        )
    )
    for shot in shots.results:
        if 'exit' not in shot.entries[0][0]:
            state = Quest.extract_states_dict(shot.entries)
            vec = state['gs'].get_single_state()
            return vec
    return None

def compute_expectation(sv, hamiltonian):
    array_vec = np.array([sv]).T.conj()
    return array_vec.conj().T @ hamiltonian @ array_vec


def build_multiplexor_lcu(ham, n_state_qubits, ind):
    multiplexor_lcu = LCUMultiplexorBox(ham, n_state_qubits)
    

    circ = multiplexor_lcu.get_circuit()
    DecomposeBoxes().apply(circ)
    rebase = AutoRebase({OpType.CX, OpType.Rz, OpType.H, OpType.CCX})
    rebase.apply(circ)


    qlibs_multiplexor_lcu = guppy.load_pytket(f"qlibs_multiplexor_lcu_{ind}", circ)
    return qlibs_multiplexor_lcu