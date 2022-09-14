from . import NACABase, NACA4Digit, NACA5DigitStandard, NACA5DigitReflex

if __name__ == '__main__':
    ns = NACABase.factory("23112", chord_length=4, cs=True)
    ni = NACABase.factory(23112, chord_length=4, cs=True)
    print(ni.n)
    print(ni.__class__.__name__)

    NACA0012 = NACABase.factory("2412", cs=True)
    # print(NACA0012.dat_file())
    print(NACA0012.__class__.__name__)
    NACA0012.plot()

    assert ns.n == ni.n
    assert ns.__class__.__name__ == ni.__class__.__name__
    assert ns.max_camber == ni.max_camber == 0.2
    assert ns.max_camber_position == ni.max_camber_position == 0.15
    assert ns.thickness == ni.thickness == 0.12
    print(ns.design_cl)
    assert ns.design_cl == ni.design_cl == 0.3
    print(ns.camber_line)
    print(ns.camber_gradient)
    n4s = NACABase.factory("2312", chord_length=4)
    n4i = NACABase.factory(2312, chord_length=4)
    print(n4s.n)
    print(n4s.__class__.__name__)
    assert n4s.n == n4i.n == "2312"
    assert n4s.__class__.__name__ == n4i.__class__.__name__ == "NACA4Digit"
    print(n4s.max_camber)
    assert n4s.max_camber == n4i.max_camber == 0.02
    assert n4s.max_camber_position == n4i.max_camber_position == 0.3
    assert n4s.thickness == n4i.thickness == 0.12
