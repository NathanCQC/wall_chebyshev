from pytket.pauli import QubitPauliString, Pauli
from pytket.utils.operators import QubitPauliOperator
from pytket.circuit import Qubit
from openfermion import fermi_hubbard, jordan_wigner



from pytket.pauli import QubitPauliString, Pauli
from pytket.utils.operators import QubitPauliOperator
from pytket.circuit import Qubit
from openfermion import fermi_hubbard, jordan_wigner, QubitOperator
import openfermion
import numpy as np
from openfermion.linalg import get_sparse_operator

def count_set_bits(n):
    m = n
    count = 0
    while m:
        if m & 1:
            count += 1
        m = m >> 1
    return count
def count_set_even_bits(n):
    m = n
    count = 0
    while m:
        if m & 1:
            count += 1
        m = m >> 2
    return count
def check_set_bits(n, p):
    for i in p:
        if 2**i & n:
            return True
    return False
def get_a_nu_vals(E_n, S, m, alpha):
    R = alpha*(E_n - S)
    avs = []
    for v in range(1, m + 1):
        avs.append(S+(R/2)*(1-np.cos(v * np.pi/(m + 0.5))))
    return avs

def generate_hilbert_space_hamil(hmat, nqubits, nelec, nalpha, ref):
    subset = []
    for i in range(2**nqubits):
        if count_set_bits(i) == nelec and count_set_even_bits(i) == nalpha:
            subset.append(i)
            if i == ref:
                index = len(subset) - 1
    matrix  = np.zeros((len(subset), len(subset)))
    for i in range(len(subset)):
        for j in range(len(subset)):
            matrix[i,j] = hmat[subset[i], subset[j]]
    return matrix, index

pauli_gate = {'X':Pauli.X, 'Y':Pauli.Y, 'Z':Pauli.Z, 'I': Pauli.I}
def generate_pytket_hvs_hubbard(u, nsites, m=5):
    # Generate the Hubbard model operator in the pytket format
    # Imports assumed already available in the file scope.

    # Create the fermionic and qubit Hamiltonians
    fermi_ham = fermi_hubbard(1, nsites, tunneling=1, coulomb=u, periodic=False)
    qubit_ham = jordan_wigner(fermi_ham)
    nqubit = nsites * 2
    nelec = nsites
    # Reference state must be chosen appropriately;
    # Here it is hardcoded for the two-site case.
    ref = 2**0 + 2**3
    hmat = get_sparse_operator(qubit_ham, n_qubits=nqubit).todense()

    # Build Hilbert space Hamiltonian
    hmat_hilb, index = generate_hilbert_space_hamil(hmat, nqubit, nelec, int(nelec/2), ref)
    evals_h, evecs_h = np.linalg.eigh(hmat_hilb)

    # Generate modified Hamiltonians with shifts using a_nu values
    hvs = []
    avs = get_a_nu_vals(evals_h[-1], evals_h[0], m, 1)
    for a in avs:
        hvs.append(qubit_ham - a * QubitOperator(''))

    # Convert the original qubit operator to a pytket operator
    pauli_strings = {}
    for term, coeff in qubit_ham.terms.items():
        paulis = []
        qubits = []
        for gate in term:
            paulis.append(pauli_gate[gate[1]])
            qubits.append(Qubit(gate[0]))
        pauli_strings[QubitPauliString(qubits, paulis)] = coeff
    qps_h = QubitPauliOperator(pauli_strings)

    # Convert each modified Hamiltonian to its pytket equivalent
    pytket_hvs = []
    for hv in hvs:
        ps_map = {}
        for term, coeff in hv.terms.items():
            paulis = []
            qubits = []
            for gate in term:
                paulis.append(pauli_gate[gate[1]])
                qubits.append(Qubit(gate[0]))
            ps_map[QubitPauliString(qubits, paulis)] = coeff
        pytket_hvs.append(QubitPauliOperator(ps_map))
    return pytket_hvs, hmat

# Example usage