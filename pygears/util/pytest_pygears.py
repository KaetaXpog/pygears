import pytest
import pathlib
from functools import partial
import os


@pytest.fixture(autouse=True)
def resdir(tmp_path_factory, pytestconfig):
    if not pytestconfig.getoption('--pg'):
        return None

    from pygears import clear, reg
    from pygears.conf.custom_settings import load_rc
    clear()
    load_rc('.pygears', os.path.dirname(__file__))

    resdir = pytestconfig.getoption("--pg-resdir")

    if resdir is None:
        resdir = str(tmp_path_factory.getbasetemp())

    from pygears import reg
    reg['results-dir'] = resdir

    return resdir


def hook_after(top, args, kwds, file_lock):
    file_lock.release()
    return False


def hook_before(top, args, kwds, config):
    import filelock
    from pygears import reg
    from pygears.sim import cosim_build_dir

    inst_id = cosim_build_dir(top)
    kwds['rebuild'] = False

    if config.getoption('--pg-resdir') is None:
        kwds['outdir'] = pathlib.Path(kwds['outdir']).parent / 'sim'
    else:
        kwds['outdir'] = pathlib.Path(kwds['outdir'])

    os.makedirs(kwds['outdir'], exist_ok=True)

    lock_fn = kwds['outdir'] / f'{inst_id}.lock'
    try:
        fl = filelock.FileLock(lock_fn, timeout=0)
        fl.acquire()
        reg['sim/hook/cosim_build_after'].append(partial(hook_after, file_lock=fl))
    except filelock.Timeout:
        with filelock.FileLock(lock_fn):
            pass


def pytest_runtest_call(item):
    if item.config.getoption('--gearbox'):
        from gearbox.main import main_loop
        main_loop(str(pathlib.Path(item.module.__file__).parent), [], item.runtest, {})
        pytest.skip()
    elif item.config.getoption('--pg'):
        from pygears import reg
        if item.config.getoption('--pg-reuse'):
            reg['sim/hook/cosim_build_before'].append(partial(hook_before, config=item.config))


# If any of --pg switches is active, than --pg should be there too
def pytest_load_initial_conftests(args):
    if (any(a.startswith('--pg') for a in args) and not any(a == '--pg' for a in args)):
        args[:] = ['--pg'] + args


def pytest_addoption(parser):
    parser.addoption(
        "--gearbox",
        action="store_true",
        help="Specify the result directory. Use /tmp by default.",
    )

    parser.addoption(
        "--pg",
        action="store_true",
        help="Use pygears pytest plugin",
    )

    parser.addoption(
        "--pg-resdir",
        type=str,
        default=None,
        help="Specify the result directory. Use /tmp by default.",
    )

    parser.addoption(
        "--pg-reuse",
        action="store_true",
        help="Specify the result directory. Use /tmp by default.",
    )