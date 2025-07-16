"""init file for circuits.utils."""

from .lcu_utils import (
    block_encoded_sparse_matrix,
    int_to_bits,
    is_hermitian,
)
from .qsvt_utils import (
    measure_single_qubit_qsp,
    qsp_phase_reflection,
    scipy_qsvt,
    single_qubit_qsp_circuit,
)

from .qsp_angles import (
    ChebyshevPolynomial,
    QSPAngleOptimiser,
    BaseCompilePhases,
    CompilerPhasesNumpy,
    CompilerPhasesNumba,
)

from .block_encoding_utils import generate_diagonal_block_encoding


from .linalg import kron_list


__all__ = [
    "int_to_bits",
    "block_encoded_sparse_matrix",
    "is_hermitian",
    "scipy_qsvt",
    "qsp_phase_reflection",
    "single_qubit_qsp_circuit",
    "measure_single_qubit_qsp",
    "Rz_jkn",
    "extend_functions",
    "generate_diagonal_entries",
    "ChebyshevPolynomial",
    "QSPAngleOptimiser",
    "generate_diagonal_block_encoding",
    "BaseCompilePhases",
    "CompilerPhasesNumpy",
    "CompilerPhasesNumba",
    "phased_paulig_box",
    "kron_list",
    "FourierPolynomial",
    "GQSPAngleFinder",
]
