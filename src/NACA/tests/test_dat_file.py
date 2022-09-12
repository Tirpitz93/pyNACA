from numpy import isclose

from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestAirfoilToolsDatFile():
    def testAirfoilToolsDatFile(self):
        filename = "src/NACA/tests/data/airfoiltools/NACA0012.dat"
        a = AirfoilToolsDatFile(filename)
        assert a.filename == filename
        assert  all(isclose(a.df["top"],a.df["bottom"]*-1))
        assert a.data["x"][a.turning_point] == 0
