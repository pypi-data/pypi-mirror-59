from runtests.mpi import MPITest

@MPITest(commsize=[1, 2])
def test_mpicomm(comm):
    assert comm is not None

from runtests.mpi import MPITestFixture

comm1 = MPITestFixture(commsize=[1, 2])
def test_mpicomm(comm1):
    assert comm1 is not None

from runtests.mpi import MPIWorld
# this is deprecated
@MPIWorld(NTask=[1, 2], required=(1, 2))
def test_mpiworld(comm):
    assert comm is not None

