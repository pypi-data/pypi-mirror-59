import fault
from fault.random import random_bv, random_bit
import magma as m
from hwtypes import BitVector, Bit
from fault.common import get_renamed_port


def get_random_arr(name, port):
    if isinstance(port, m.BitsKind) or isinstance(port.T, m._BitKind):
        # TODO: Hack, check the name and don't twiddle config ports, we
        # should add a config type
        if "config_" in name:
            return BitVector[len(port)](0)
        else:
            return random_bv(len(port))
    else:
        if isinstance(port.T, m.ArrayKind):
            return fault.array.Array([get_random_arr(name + f"_{i}", port.T)
                                      for i in range(len(port))], len(port))
    raise NotImplementedError()  # pragma: nocover


def get_random_input(name, port):
    if isinstance(port, m.ArrayKind):
        return get_random_arr(name, port)
    elif isinstance(port, m.AsyncResetKind):
        return 0
    elif isinstance(port, m._BitKind):
        # TODO: Hack, check the name and don't twiddle config ports, we
        # should add a config type
        if "config_" in name:
            return Bit(0)
        elif "reset" in name:
            return Bit(0)
        else:
            return random_bit()
    else:
        raise NotImplementedError(name, port, type(port))  # pragma: nocover


def generate_random_test_vectors(circuit, functional_model,
                                 num_vectors=10, input_mapping=None):
    tester = fault.Tester(circuit)

    for i in range(num_vectors):
        inputs = []
        for name, port in circuit.interface.items():
            if port.isinput():
                inputs.append(get_random_input(name, port))
                tester.poke(getattr(circuit, name), inputs[-1])
        tester.eval()
        # Used to handle differences between circuit's interface and
        # functional_model interface. For example, the simple_cb interface
        # is packed for the genesis version
        if input_mapping:
            inputs = input_mapping(*inputs)
        functional_model(*inputs)
        for name, port in circuit.interface.items():
            if port.isoutput():
                # Handle renamed output ports
                fn_model_port = get_renamed_port(circuit, name)
                tester.expect(getattr(circuit, name),
                              getattr(functional_model, fn_model_port))
    return tester.test_vectors
