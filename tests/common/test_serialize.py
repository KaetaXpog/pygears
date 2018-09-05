from nose import with_setup

from pygears import clear
from pygears.common.serialize import serialize
from pygears.cookbook.verif import directed, verif
from pygears.sim import sim
from pygears.sim.modules.drv import drv
from pygears.sim.modules.sim_socket import SimSocket
from pygears.sim.modules.verilator import SimVerilated
from pygears.typing import Array, Uint
from utils import skip_ifndef, prepare_result_dir


@with_setup(clear)
def test_pygears_sim():
    brick_size = 4
    seq_list = [1, 2, 3, 4]
    directed(
        drv(t=Array[Uint[16], brick_size],
            seq=[(i, ) * brick_size for i in seq_list]),
        f=serialize,
        ref=sorted(seq_list * brick_size))

    sim()


@with_setup(clear)
def test_socket_sim():
    skip_ifndef('SIM_SOCKET_TEST')
    brick_size = 4
    seq_list = [1, 2, 3]
    directed(
        drv(t=Array[Uint[16], brick_size],
            seq=[(i, ) * brick_size for i in seq_list]),
        f=serialize(sim_cls=SimSocket),
        ref=sorted(seq_list * brick_size))

    sim()


@with_setup(clear)
def test_verilate_sim():
    skip_ifndef('VERILATOR_ROOT')
    brick_size = 4
    seq_list = [1, 2, 3, 4]
    directed(
        drv(t=Array[Uint[16], brick_size],
            seq=[(i, ) * brick_size for i in seq_list]),
        f=serialize(sim_cls=SimVerilated),
        ref=sorted(seq_list * brick_size))

    sim(outdir=prepare_result_dir())


@with_setup(clear)
def test_socket_cosim():
    skip_ifndef('SIM_SOCKET_TEST')
    brick_size = 4
    seq_list = [1, 2, 3, 4]
    verif(
        drv(t=Array[Uint[16], brick_size],
            seq=[(i, ) * brick_size for i in seq_list]),
        f=serialize(sim_cls=SimSocket),
        ref=serialize(name='ref_model'))

    sim()