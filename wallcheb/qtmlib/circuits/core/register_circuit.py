"""Oracle Circuit for Abstract Circuit Construction."""

from wallcheb.qtmlib.circuits.core import RegisterBox
from pytket.circuit import QubitRegister, Qubit
from pytket._tket.unit_id import BitRegister, Bit
from pytket._tket.circuit import Circuit, CircBox
from dataclasses import dataclass
from copy import deepcopy
from typing import Self
from collections.abc import Sequence
from collections import Counter


QMAP_INPUT_TYPES = QubitRegister | Qubit | list[Qubit]
CMAP_INPUT_TYPES = BitRegister | Bit | list[Bit]


@dataclass
class RegisterMapElement:
    """Qubit Register Map Element.

    This class is used to map the qubit registers of an register_box to the
    qubit registers of a RegisterCircuit. The register_box qubit registers are
    the input qubit registers of the register_box. It can also map individual
    qubits and lists of qubits to RegisterCircuit.

    Args:
    ----
        box (QubitRegister | Qubit | list[Qubit]): The qubit register or qubits
            to be mapped.
        circ (QubitRegister | Qubit | list[Qubit]): The qubit register or qubits
            to be mapped to.

    Raises:
    ------
        ValueError: If the box registers/qubits and registers/qubits are not the
            same type.
        ValueError: If the box registers/qubits and registers/qubits are not the
            same size.

    """

    box: QubitRegister | Qubit | list[Qubit]
    circ: QubitRegister | Qubit | list[Qubit]

    def __post_init__(self):
        """Initialise the RegisterMapElement."""
        if isinstance(self.box, (QubitRegister | list)) and isinstance(
            self.circ, (QubitRegister | list)
        ):
            if len(self.box) != len(self.circ):
                raise ValueError(
                    f"box qreg {self.box} and circuit qreg {self.circ} are"
                    "not the same size"
                )


class QRegMap:
    """Qubit Register Maps for RegisterBoxes to RegisterCircuits.

    This class is used to map the list[QubitRegister | Qubit | list[Qubit]]) of an
    register_box to the corresponding list[QubitRegister | Qubit | list[Qubit]])
    of a RegisterCircuit. Each element of the box_qreg maps to the same index
    element in the other list. They must be the same size and type.

    Args:
    ----
        box_qregs (list[QubitRegister | Qubit | list[Qubit]]): List of
            QubitRegister objects for the register_box.
        reg_circ_qregs (list[QubitRegister | Qubit | list[Qubit]]): List of
            QubitRegister objects for the RegisterCircuit.

    Raises:
    ------
        ValueError: If the number of qubits in the register_box qubit registers and
            the RegisterCircuit qubit registers are not the same.
        ValueError: If there are duplicates in the register_box qubit registers.

    """

    def __init__(
        self,
        box_qregs: Sequence[QubitRegister | Qubit | list[Qubit]],
        reg_circ_qregs: Sequence[QubitRegister | Qubit | list[Qubit]],
    ) -> None:
        """Initialise the QRegMap."""
        self.items = [
            RegisterMapElement(box, qregcirc)
            for box, qregcirc in zip(box_qregs, reg_circ_qregs, strict=True)
        ]
        self.box_qregs = box_qregs
        self.circ_qregs = reg_circ_qregs

        self._box_qubits = self.qubit_list(box_qregs)
        self._circ_qubits = self.qubit_list(reg_circ_qregs)

    @property
    def qubit_map(self) -> dict[Qubit, Qubit]:
        """Return the qubit map."""
        return dict(zip(self.box_qubits, self.circ_qubits, strict=True))

    @property
    def box_qubits(self) -> list[Qubit]:
        """Return the qubits in the register_box."""
        return self._box_qubits

    @property
    def circ_qubits(self) -> list[Qubit]:
        """Return the qubits in the RegisterCircuit."""
        return self._circ_qubits

    def qubit_list(self, map_qreg: Sequence[QMAP_INPUT_TYPES]) -> list[Qubit]:
        """Convert the map_qreg to a set of qubits."""
        qubits: list[Qubit] = []
        for element in map_qreg:
            if isinstance(element, QubitRegister):
                qubits.extend(element.to_list())
            elif isinstance(element, list):
                qubits.extend(element)
            else:
                qubits.append(element)

        counts = Counter(qubits)
        for item, count in counts.items():
            if count > 1:
                raise ValueError(f"Qubit {item} appears more than once in the input")

        return qubits

    @classmethod
    def from_dict(cls, qreg_map_dict: dict[QMAP_INPUT_TYPES, QMAP_INPUT_TYPES]) -> Self:
        """Create a QRegMap from a dictionary.

        Args:
        ----
            qreg_map_dict (dict): Dictionary of QubitRegister objects for the
                register_box (.keys()) and RegisterCircuit (.values()).§

        """
        box_qregs = list(qreg_map_dict.keys())
        qregcirc_qregs = list(qreg_map_dict.values())
        return cls(box_qregs, qregcirc_qregs)

    @classmethod
    def from_QRegMap_list(cls, qreg_map_list: list[Self]) -> Self:
        """Create a QRegMap from a list of QRegMaps.

        Args:
        ----
            qreg_map_list (list[QRegMap]): List of QRegMap objects.

        """
        box_qubits = [qreg_map.box_qubits for qreg_map in qreg_map_list]
        circ_qubits = [qreg_map.circ_qubits for qreg_map in qreg_map_list]
        return cls(box_qubits, circ_qubits)

    def __repr__(self):
        """Return string representation of the QRegMap."""
        mapping_str = "\n"
        for item in self.items:
            if isinstance(item.box, QubitRegister) and isinstance(
                item.circ, QubitRegister
            ):
                mapping_str += f"QREG: {item.box.name} [{len(item.box)}] -> \
                    {item.circ.name} [{len(item.circ)}]\n"

            elif isinstance(item.box, Qubit) and isinstance(item.circ, Qubit):
                mapping_str += f"QUBIT: {item.box.reg_name} ({item.box.index}) -> \
                      {item.circ.reg_name} ({item.circ.index})\n"

            elif isinstance(item.box, list) and isinstance(item.circ, list):
                box_qubits_str = "".join(
                    [f"{qubit.reg_name} ({qubit.index})," for qubit in item.box]
                )
                circ_qubits_str = "".join(
                    [f"{qubit.reg_name} ({qubit.index})," for qubit in item.circ]
                )
                mapping_str += (
                    f"QUBITS: {box_qubits_str[:-1]} -> {circ_qubits_str[:-1]}\n"
                )

        return f"QRegMap (box -> circ):\n{mapping_str}"


@dataclass
class BitRegisterMapElement:
    """Bit Register Map Element.

    This class is used to map the bit registers of an register_box to the
    qubit registers of a RegisterCircuit. The register_box bit registers are
    the input qubit registers of the register_box. It can also map individual
    qubits and lists of qubits to RegisterCircuit.

    Args:
    ----
        box (BitRegister | Bit | list[Bit]): The qubit register or qubits
            to be mapped.
        circ (BitRegister | Bit | list[Bit]): The qubit register or qubits
            to be mapped to.

    Raises:
    ------
        ValueError: If the box registers/qubits and registers/qubits are not the
            same type.
        ValueError: If the box registers/qubits and registers/qubits are not the
            same size.

    """

    box: BitRegister | Bit | list[Bit]
    circ: BitRegister | Bit | list[Bit]

    def __post_init__(self):
        """Initialise the RegisterMapElement."""
        if isinstance(self.box, (BitRegister | list)) and isinstance(
            self.circ, (BitRegister | list)
        ):
            if len(self.box) != len(self.circ):
                raise ValueError(
                    f"box creg {self.box} and circuit creg {self.circ} are"
                    "not the same size"
                )


class CRegMap:
    """Bit Register Maps for RegisterBoxes to RegisterCircuits.

    This class is used to map the list[BitRegister | Bit | list[Bit]]) of an
    register_box to the corresponding list[BitRegister | Bit | list[Bit]])
    of a RegisterCircuit. Each element of the box_qreg maps to the same index
    element in the other list. They must be the same size and type.

    Args:
    ----
        box_cregs (list[BitRegister | Bit | list[Bit]]): List of
            BitRegister objects for the register_box.
        reg_circ_cregs (list[BitRegister | Bit | list[Bit]]): List of
            BitRegister objects for the RegisterCircuit.

    Raises:
    ------
        ValueError: If the number of bits in the register_box bit registers and
            the RegisterCircuit bit registers are not the same.
        ValueError: If there are duplicates in the register_box bit registers.

    """

    def __init__(
        self,
        box_cregs: Sequence[BitRegister | Bit | list[Bit]],
        reg_circ_cregs: Sequence[BitRegister | Bit | list[Bit]],
    ) -> None:
        """Initialise the CRegMap."""
        self.items = [
            BitRegisterMapElement(box, cregcirc)
            for box, cregcirc in zip(box_cregs, reg_circ_cregs, strict=True)
        ]
        self.box_cregs = box_cregs
        self.circ_cregs = reg_circ_cregs

        self._box_bits = self.bit_list(box_cregs)
        self._circ_bits = self.bit_list(reg_circ_cregs)

    @property
    def bit_map(self) -> dict[Bit, Bit]:
        """Return the bit map."""
        return dict(zip(self.box_bits, self.circ_bits, strict=True))

    @property
    def box_bits(self) -> list[Bit]:
        """Return the bits in the register_box."""
        return self._box_bits

    @property
    def circ_bits(self) -> list[Bit]:
        """Return the qubits in the RegisterCircuit."""
        return self._circ_bits

    def bit_list(self, map_creg: Sequence[CMAP_INPUT_TYPES]) -> list[Bit]:
        """Convert the map_creg to a set of qubits."""
        bits: list[Bit] = []
        for element in map_creg:
            if isinstance(element, BitRegister):
                bits.extend(element.to_list())
            elif isinstance(element, list):
                bits.extend(element)
            else:
                bits.append(element)

        counts = Counter(bits)
        for item, count in counts.items():
            if count > 1:
                raise ValueError(f"Bit {item} appears more than once in the input")

        return bits

    @classmethod
    def from_dict(cls, creg_map_dict: dict[CMAP_INPUT_TYPES, CMAP_INPUT_TYPES]) -> Self:
        """Create a CRegMap from a dictionary.

        Args:
        ----
            creg_map_dict (dict): Dictionary of BitRegister objects for the
                register_box (.keys()) and RegisterCircuit (.values()).§

        """
        box_cregs = list(creg_map_dict.keys())
        cregcirc_cregs = list(creg_map_dict.values())
        return cls(box_cregs, cregcirc_cregs)

    @classmethod
    def from_QRegMap_list(cls, creg_map_list: list[Self]) -> Self:
        """Create a CRegMap from a list of CRegMaps.

        Args:
        ----
            creg_map_list (list[CRegMap]): List of CRegMap objects.

        """
        box_bits = [creg_map.box_bits for creg_map in creg_map_list]
        circ_bits = [creg_map.circ_bits for creg_map in creg_map_list]
        return cls(box_bits, circ_bits)

    def __repr__(self):
        """Return string representation of the QRegMap."""
        mapping_str = "\n"
        for item in self.items:
            if isinstance(item.box, BitRegister) and isinstance(item.circ, BitRegister):
                mapping_str += f"QREG: {item.box.name} [{len(item.box)}] -> \
                    {item.circ.name} [{len(item.circ)}]\n"

            elif isinstance(item.box, Bit) and isinstance(item.circ, Bit):
                mapping_str += f"BIT: {item.box.reg_name} ({item.box.index}) -> \
                      {item.circ.reg_name} ({item.circ.index})\n"

            elif isinstance(item.box, list) and isinstance(item.circ, list):
                box_bits_str = "".join(
                    [f"{bit.reg_name} ({bit.index})," for bit in item.box]
                )
                circ_bits_str = "".join(
                    [f"{bit.reg_name} ({bit.index})," for bit in item.circ]
                )
                mapping_str += f"BITS: {box_bits_str[:-1]} -> {circ_bits_str[:-1]}\n"

        return f"CRegMap (box -> circ):\n{mapping_str}"


class RegisterCircuit(Circuit):
    """OracleCircuit for Abstract Circuit Construction.

    This class inherits from Circuit. It is used to construct the circuit
    but add the abililty to add an register_box to the circuit using a QRegMap.
    Which maps the registers of the register_box to the registers of the
    RegisterCircuit. Register Circuits have all the functionality of pytket.Circuit
    and can be used in the same way. With individual gates and qubits. But the
    main purpose is to add an register_box to the circuit just use register maps.
    """

    def add_registerbox(
        self,
        register_box: RegisterBox,
        qreg_map: QRegMap | None = None,
        creg_map: CRegMap | None = None,
    ) -> Self:
        """Add an register_box to the RegisterCircuit.

        Adds an register_box to the RegisterCircuit using a QRegMap to map the
        register_box qubit registers to the RegisterCircuit qubit registers.
        If no QRegMap is provided, the register_box qubit registers will be
        mapped to the RegisterCircuit qubit registers automatically if they
        match in name and size.

        Args:
        ----
            register_box (register_box): The register_box to be added to the circuit.
            qreg_map (QRegMap, optional): The QRegMap to map the register_box
                qubit registers to the RegisterCircuit qubit registers.
                Defaults to None. Box registers matching circuit names of the
                 same size will be mapped automatically, if None is passed.
            creg_map (CRegMap, optional): The CRegMap to map the register_box
                bit registers to the RegisterCircuit bit registers.
                Defaults to None. Box registers matching circuit names of the
                 same size will be mapped automatically, if None is passed.

        Raises:
        ------
            ValueError: If the register_box qubit registers are not a subset of the
                RegisterCircuit qubit registers (When no QregMap is provided).
            ValueError: If the QRegMap RegisterCircuit qubit registers are not a
            subset of the register_box qubit registers.

        Returns:
        -------
            RegisterCircuit: The RegisterCircuit with the register_box added.

        """
        if qreg_map is None:
            # if not set(register_box.q_registers).issubset(set(self.q_registers)):
            #     raise ValueError(
            #         "register_box QubitRegisters are not a subset of "
            #         "circuit QubitRegisters of the same size"
            #     )
            if not set(register_box.qubits).issubset(set(self.qubits)):
                raise ValueError(
                    "register_box qubits are not a subset of circuit qubits"
                )
            qubits = register_box.qubits

        else:
            if not set(qreg_map.box_qubits).issubset(set(register_box.qubits)):
                raise ValueError("qreg map box qubits are not a subset of box qubits")

            if not set(qreg_map.circ_qubits).issubset(set(self.qubits)):
                raise ValueError("qreg map circ qubits are not a subset of circ qubits")

            # Orders the map in the same order as the box qregs
            # Then form the qubit input list

            qubits = [qreg_map.qubit_map[q_regbox] for q_regbox in register_box.qubits]

        if creg_map is None:
            if not set(register_box.bits).issubset(set(self.bits)):
                raise ValueError("register_box bits are not a subset of circuit bits")
            bits = register_box.bits

        else:
            if not set(creg_map.box_bits).issubset(set(register_box.bits)):
                raise ValueError("creg map box bits are not a subset of box bits")

            if not set(creg_map.circ_bits).issubset(set(self.bits)):
                raise ValueError("creg map circ bits are not a subset of circ bits")

            # Orders the map in the same order as the box cregs
            # Then form the bit input list

            bits = [creg_map.bit_map[c_regbox] for c_regbox in register_box.bits]

        circ = register_box.get_circuit().copy()
        circ.flatten_registers()

        self.add_gate(CircBox(circ), qubits + bits)

        return self

    def copy(self) -> Self:
        """Return a copy of the RegisterCircuit."""
        return deepcopy(self)
