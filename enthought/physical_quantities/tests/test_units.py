import math

from unittest import TestCase

from enthought.physical_quantities.dimensions import Dimensions, Dim

from enthought.physical_quantities.units import Unit, MultiplicativeUnit, \
    NamedUnit, BaseUnit
    
class UnitClassTest(TestCase):
    def setUp(self):
        self.length = Dimensions({"length": 1.0})
        self.mass = Dimensions({"mass": 1.0})
        self.time = Dimensions({"time": 1.0})
        self.temperature = Dimensions({"temperature": 1.0})
        self.force = self.mass*self.length/self.time**2
        self.power = self.force*self.length
        
        self.newton = Unit(symbol="N", expression="N", latex="\mathrm{N}",
                      dimensions=self.force)
        
        self.watt = Unit(symbol="W", expression="W", latex="\mathrm{W}",
                         dimensions=self.power)
        self.milliwatt = Unit(symbol="mW", expression="mW", latex="\mathrm{mW}",
                         scale=1000.0, dimensions=self.power)
        self.decibel = Unit(symbol="dB", expression="decibel",
                            latex="\mathrm{dB}", dimensions=self.power,
                            logarithmic=True, scale=10.0, offset=-3.0)
        self.neper = Unit(symbol="np", expression="neper",
                            latex="\mathrm{np}", dimensions=self.power,
                            logarithmic=True, scale=0.5, offset=-math.log(1000),
                            log_base=math.exp(1.0))
        
        self.kelvin = Unit(symbol="K", expression="K", latex="\mathrm{K}",
                      dimensions=self.temperature)
        self.kelvin_named = NamedUnit(symbol="K", expression="K", latex="\mathrm{K}",
                      dimensions=self.temperature)
        self.kelvin_base = BaseUnit(symbol="K", expression="K", latex="\mathrm{K}",
                      dimensions=self.temperature)
        self.rankine = Unit(symbol="R", expression="R", latex="\mathrm{R}",
                      dimensions=self.temperature, scale=9.0/5.0)
        self.rankine_named = NamedUnit(symbol="R", expression="R", latex="\mathrm{R}",
                      dimensions=self.temperature, scale=9.0/5.0)
        self.degree_C = Unit(symbol=u"\u00B0C", expression="degree_C",
                       latex="\,^{\circ}\mathrm{C}", dimensions=self.temperature,
                       offset=273.15)
        self.degree_F = Unit(symbol=u"\u00B0F", expression="degree_F",
                       latex="\,^{\circ}\mathrm{F}", dimensions=self.temperature,
                       scale=9.0/5.0, offset=459.67*5.0/9.0)
    
    # Test convert_to_base method
    def test_convert_to_base_trivial(self):
        assert self.kelvin.convert_to_base(273.15) == 273.15
        assert self.kelvin.convert_to_base(0.0) == 0.0
        assert self.kelvin.convert_to_base(373.15) == 373.15
        assert self.kelvin.convert_to_base(255.37222222222221) == 255.37222222222221

    def test_convert_to_base_scale(self):
        self.assertAlmostEqual(self.rankine.convert_to_base(491.67), 273.15)
        self.assertAlmostEqual(self.rankine.convert_to_base(0.0), 0.0)
        self.assertAlmostEqual(self.rankine.convert_to_base(491.67+180), 373.15)
        self.assertAlmostEqual(self.rankine.convert_to_base(459.67), 255.37222222222221)
    
    def test_convert_to_base_offset(self):
        assert self.degree_C.convert_to_base(0.0) == 273.15
        assert self.degree_C.convert_to_base(-273.15) == 0.0
        assert self.degree_C.convert_to_base(100.0) == 373.15
        assert self.degree_C.convert_to_base(-17.777777777777779) == 255.37222222222221
    
    def test_convert_to_base_scale_offset(self):
        self.assertAlmostEqual(self.degree_F.convert_to_base(32.0), 273.15)
        self.assertAlmostEqual(self.degree_F.convert_to_base(-459.67), 0.0)
        self.assertAlmostEqual(self.degree_F.convert_to_base(212.0), 373.15)
        self.assertAlmostEqual(self.degree_F.convert_to_base(0.0), 255.37222222222221)
        
    def test_convert_to_base_logarithmic(self):
        self.assertAlmostEqual(self.decibel.convert_to_base(30.0), 1.0)
        self.assertAlmostEqual(self.decibel.convert_to_base(0.0), 0.001)
        
    def test_convert_to_base_logarithmic_natural(self):
        self.assertAlmostEqual(self.neper.convert_to_base(3.4538776394910684), 1.0)
        self.assertAlmostEqual(self.neper.convert_to_base(0.0), 0.001)
    
    # Test convert_from_base method
    def test_convert_from_base_trivial(self):
        assert self.kelvin.convert_from_base(273.15) == 273.15
        assert self.kelvin.convert_from_base(0.0) == 0.0
        assert self.kelvin.convert_from_base(373.15) == 373.15
        assert self.kelvin.convert_from_base(255.37222222222221) == 255.37222222222221

    def test_convert_from_base_scale(self):
        self.assertAlmostEqual(self.rankine.convert_from_base(273.15), 491.67)
        self.assertAlmostEqual(self.rankine.convert_from_base(0.0), 0.0)
        self.assertAlmostEqual(self.rankine.convert_from_base(373.15), 491.67+180)
        self.assertAlmostEqual(self.rankine.convert_from_base(255.37222222222221), 459.67)
    
    def test_convert_from_base_offset(self):
        assert self.degree_C.convert_from_base(0.0) == -273.15
        assert self.degree_C.convert_from_base(273.15) == 0.0
        assert self.degree_C.convert_from_base(373.15) == 100.0
        self.assertAlmostEqual(self.degree_C.convert_from_base(255.37222222222221), -17.777777777777779)
    
    def test_convert_from_base_scale_offset(self):
        self.assertAlmostEqual(self.degree_F.convert_from_base(273.15), 32.0)
        self.assertAlmostEqual(self.degree_F.convert_from_base(0.0), -459.67)
        self.assertAlmostEqual(self.degree_F.convert_from_base(373.15), 212.0)
        self.assertAlmostEqual(self.degree_F.convert_from_base(255.37222222222221), 0.0)
        
    # Test convert_to_unit method
    def test_convert_to_unit_trivial(self):
        assert self.kelvin.convert_to_unit(273.15, self.kelvin) == 273.15
        assert self.kelvin.convert_to_unit(0.0, self.kelvin) == 0.0
        assert self.kelvin.convert_to_unit(373.15, self.kelvin) == 373.15
        assert self.kelvin.convert_to_unit(255.37222222222221, self.kelvin) == 255.37222222222221

    def test_convert_to_unit_scale_trivial(self):
        self.assertAlmostEqual(self.rankine.convert_to_unit(491.67, self.kelvin), 273.15)
        self.assertAlmostEqual(self.rankine.convert_to_unit(0.0, self.kelvin), 0.0)
        self.assertAlmostEqual(self.rankine.convert_to_unit(491.67+180, self.kelvin), 373.15)
        self.assertAlmostEqual(self.rankine.convert_to_unit(459.67, self.kelvin), 255.37222222222221)
    
    def test_convert_to_unit_offset_trivial(self):
        assert self.degree_C.convert_to_unit(0.0, self.kelvin) == 273.15
        assert self.degree_C.convert_to_unit(-273.15, self.kelvin) == 0.0
        assert self.degree_C.convert_to_unit(100.0, self.kelvin) == 373.15
        assert self.degree_C.convert_to_unit(-17.777777777777779, self.kelvin) == 255.37222222222221
    
    def test_convert_to_unit_scale_offset_trivial(self):
        self.assertAlmostEqual(self.degree_F.convert_to_unit(32.0, self.kelvin), 273.15)
        self.assertAlmostEqual(self.degree_F.convert_to_unit(-459.67, self.kelvin), 0.0)
        self.assertAlmostEqual(self.degree_F.convert_to_unit(212.0, self.kelvin), 373.15)
        self.assertAlmostEqual(self.degree_F.convert_to_unit(0.0, self.kelvin), 255.37222222222221)

    # Automatically generated test cases to cover all cases of non-logarithmic
    # conversions
    #    Generated by the following code:
    """

def values(T):
    return {
        "degree_C": repr(T),
        "kelvin": repr(T+273.15),
        "kelvin_base": repr(T+273.15),
        "kelvin_named": repr(T+273.15),
        "degree_F": repr(T*9.0/5.0 + 32),
        "rankine": repr((T+273.15)*9.0/5.0),
        "rankine_named": repr((T+273.15)*9.0/5.0),
    }

def write_base_converter_test(unit, rows):
    func_code = "    def test_convert_to_base_%s(self):\n" % unit
    for row in rows:
        func_code += "        self.assertAlmostEqual(self.%s.convert_to_base(%s), %s)\n" % \
                     (unit, row[unit], row["kelvin"])
        func_code += "\n"
    func_code += "    def test_convert_from_base_%s(self):\n" % unit
    for row in rows:
        func_code += "        self.assertAlmostEqual(self.%s.convert_from_base(%s), %s)\n" % \
                     (unit, row["kelvin"], row[unit])
        func_code += "\n"
    return func_code
       

def write_complex_convert_test(from_unit, to_unit, rows):
    func_code = "    def test_convert_to_unit_%s_to_%s(self):\n" % \
                (from_unit, to_unit)
    for row in rows:
        func_code += "        self.assertAlmostEqual(self.%s.convert_to_unit(%s, self.%s), %s)\n" % \
                     (from_unit, row[from_unit], to_unit, row[to_unit])

    func_code += "\n"
    func_code = "    def test_convert_from_unit_%s_from_%s(self):\n" % \
                (from_unit, to_unit)
    for row in rows:
        func_code += "        self.assertAlmostEqual(self.%s.convert_from_unit(%s, self.%s), %s)\n" % \
                     (to_unit, row[from_unit], from_unit, row[to_unit])

    func_code += "\n"
    func_code = "    def test_make_converter_%s_from_%s(self):\n" % \
                (from_unit, to_unit)
    func_code += "        converter = self.%s.make_converter(self.%s)\n" % \
                 (from_unit, to_unit)
    for row in rows:
        func_code += "        self.assertAlmostEqual(converter(%s), %s)\n" % \
                     (row[from_unit], row[to_unit])

    func_code += "\n"
    return func_code

rows = [values(T) for T in [-273.15, -17.777777777777779, 0.0, 100.0]]
units = rows[0].keys()

for unit in units:
    print write_base_converter_test(unit, rows)

for from_unit in units:
    for to_unit in units:
        print write_complex_convert_test(from_unit, to_unit, rows)
    
    """
    
    def test_convert_to_base_kelvin_base(self):
        self.assertAlmostEqual(self.kelvin_base.convert_to_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin_base.convert_to_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin_base.convert_to_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin_base.convert_to_base(373.14999999999998), 373.14999999999998)

    def test_convert_from_base_kelvin_base(self):
        self.assertAlmostEqual(self.kelvin_base.convert_from_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin_base.convert_from_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin_base.convert_from_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin_base.convert_from_base(373.14999999999998), 373.14999999999998)


    def test_convert_to_base_rankine(self):
        self.assertAlmostEqual(self.rankine.convert_to_base(0.0), 0.0)

        self.assertAlmostEqual(self.rankine.convert_to_base(459.66999999999996), 255.37222222222221)

        self.assertAlmostEqual(self.rankine.convert_to_base(491.66999999999996), 273.14999999999998)

        self.assertAlmostEqual(self.rankine.convert_to_base(671.66999999999996), 373.14999999999998)

    def test_convert_from_base_rankine(self):
        self.assertAlmostEqual(self.rankine.convert_from_base(0.0), 0.0)

        self.assertAlmostEqual(self.rankine.convert_from_base(255.37222222222221), 459.66999999999996)

        self.assertAlmostEqual(self.rankine.convert_from_base(273.14999999999998), 491.66999999999996)

        self.assertAlmostEqual(self.rankine.convert_from_base(373.14999999999998), 671.66999999999996)


    def test_convert_to_base_kelvin(self):
        self.assertAlmostEqual(self.kelvin.convert_to_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin.convert_to_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin.convert_to_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin.convert_to_base(373.14999999999998), 373.14999999999998)

    def test_convert_from_base_kelvin(self):
        self.assertAlmostEqual(self.kelvin.convert_from_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin.convert_from_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin.convert_from_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin.convert_from_base(373.14999999999998), 373.14999999999998)


    def test_convert_to_base_degree_F(self):
        self.assertAlmostEqual(self.degree_F.convert_to_base(-459.66999999999996), 0.0)

        self.assertAlmostEqual(self.degree_F.convert_to_base(0.0), 255.37222222222221)

        self.assertAlmostEqual(self.degree_F.convert_to_base(32.0), 273.14999999999998)

        self.assertAlmostEqual(self.degree_F.convert_to_base(212.0), 373.14999999999998)

    def test_convert_from_base_degree_F(self):
        self.assertAlmostEqual(self.degree_F.convert_from_base(0.0), -459.66999999999996)

        self.assertAlmostEqual(self.degree_F.convert_from_base(255.37222222222221), 0.0)

        self.assertAlmostEqual(self.degree_F.convert_from_base(273.14999999999998), 32.0)

        self.assertAlmostEqual(self.degree_F.convert_from_base(373.14999999999998), 212.0)


    def test_convert_to_base_degree_C(self):
        self.assertAlmostEqual(self.degree_C.convert_to_base(-273.14999999999998), 0.0)

        self.assertAlmostEqual(self.degree_C.convert_to_base(-17.777777777777779), 255.37222222222221)

        self.assertAlmostEqual(self.degree_C.convert_to_base(0.0), 273.14999999999998)

        self.assertAlmostEqual(self.degree_C.convert_to_base(100.0), 373.14999999999998)

    def test_convert_from_base_degree_C(self):
        self.assertAlmostEqual(self.degree_C.convert_from_base(0.0), -273.14999999999998)

        self.assertAlmostEqual(self.degree_C.convert_from_base(255.37222222222221), -17.777777777777779)

        self.assertAlmostEqual(self.degree_C.convert_from_base(273.14999999999998), 0.0)

        self.assertAlmostEqual(self.degree_C.convert_from_base(373.14999999999998), 100.0)


    def test_convert_to_base_rankine_named(self):
        self.assertAlmostEqual(self.rankine_named.convert_to_base(0.0), 0.0)

        self.assertAlmostEqual(self.rankine_named.convert_to_base(459.66999999999996), 255.37222222222221)

        self.assertAlmostEqual(self.rankine_named.convert_to_base(491.66999999999996), 273.14999999999998)

        self.assertAlmostEqual(self.rankine_named.convert_to_base(671.66999999999996), 373.14999999999998)

    def test_convert_from_base_rankine_named(self):
        self.assertAlmostEqual(self.rankine_named.convert_from_base(0.0), 0.0)

        self.assertAlmostEqual(self.rankine_named.convert_from_base(255.37222222222221), 459.66999999999996)

        self.assertAlmostEqual(self.rankine_named.convert_from_base(273.14999999999998), 491.66999999999996)

        self.assertAlmostEqual(self.rankine_named.convert_from_base(373.14999999999998), 671.66999999999996)


    def test_convert_to_base_kelvin_named(self):
        self.assertAlmostEqual(self.kelvin_named.convert_to_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin_named.convert_to_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin_named.convert_to_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin_named.convert_to_base(373.14999999999998), 373.14999999999998)

    def test_convert_from_base_kelvin_named(self):
        self.assertAlmostEqual(self.kelvin_named.convert_from_base(0.0), 0.0)

        self.assertAlmostEqual(self.kelvin_named.convert_from_base(255.37222222222221), 255.37222222222221)

        self.assertAlmostEqual(self.kelvin_named.convert_from_base(273.14999999999998), 273.14999999999998)

        self.assertAlmostEqual(self.kelvin_named.convert_from_base(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_base_from_kelvin_base(self):
        converter = self.kelvin_base.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_base_from_rankine(self):
        converter = self.kelvin_base.make_converter(self.rankine)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_base_from_kelvin(self):
        converter = self.kelvin_base.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_base_from_degree_F(self):
        converter = self.kelvin_base.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(0.0), -459.66999999999996)
        self.assertAlmostEqual(converter(255.37222222222221), 0.0)
        self.assertAlmostEqual(converter(273.14999999999998), 32.0)
        self.assertAlmostEqual(converter(373.14999999999998), 212.0)


    def test_make_converter_kelvin_base_from_degree_C(self):
        converter = self.kelvin_base.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(0.0), -273.14999999999998)
        self.assertAlmostEqual(converter(255.37222222222221), -17.777777777777779)
        self.assertAlmostEqual(converter(273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(373.14999999999998), 100.0)


    def test_make_converter_kelvin_base_from_rankine_named(self):
        converter = self.kelvin_base.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_base_from_kelvin_named(self):
        converter = self.kelvin_base.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_rankine_from_kelvin_base(self):
        converter = self.rankine.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_rankine_from_rankine(self):
        converter = self.rankine.make_converter(self.rankine)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 459.66999999999996)
        self.assertAlmostEqual(converter(491.66999999999996), 491.66999999999996)
        self.assertAlmostEqual(converter(671.66999999999996), 671.66999999999996)


    def test_make_converter_rankine_from_kelvin(self):
        converter = self.rankine.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_rankine_from_degree_F(self):
        converter = self.rankine.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(0.0), -459.66999999999996)
        self.assertAlmostEqual(converter(459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(491.66999999999996), 32.0)
        self.assertAlmostEqual(converter(671.66999999999996), 212.0)


    def test_make_converter_rankine_from_degree_C(self):
        converter = self.rankine.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(0.0), -273.14999999999998)
        self.assertAlmostEqual(converter(459.66999999999996), -17.777777777777779)
        self.assertAlmostEqual(converter(491.66999999999996), 0.0)
        self.assertAlmostEqual(converter(671.66999999999996), 100.0)


    def test_make_converter_rankine_from_rankine_named(self):
        converter = self.rankine.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 459.66999999999996)
        self.assertAlmostEqual(converter(491.66999999999996), 491.66999999999996)
        self.assertAlmostEqual(converter(671.66999999999996), 671.66999999999996)


    def test_make_converter_rankine_from_kelvin_named(self):
        converter = self.rankine.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_kelvin_from_kelvin_base(self):
        converter = self.kelvin.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_from_rankine(self):
        converter = self.kelvin.make_converter(self.rankine)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_from_kelvin(self):
        converter = self.kelvin.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_from_degree_F(self):
        converter = self.kelvin.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(0.0), -459.66999999999996)
        self.assertAlmostEqual(converter(255.37222222222221), 0.0)
        self.assertAlmostEqual(converter(273.14999999999998), 32.0)
        self.assertAlmostEqual(converter(373.14999999999998), 212.0)


    def test_make_converter_kelvin_from_degree_C(self):
        converter = self.kelvin.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(0.0), -273.14999999999998)
        self.assertAlmostEqual(converter(255.37222222222221), -17.777777777777779)
        self.assertAlmostEqual(converter(273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(373.14999999999998), 100.0)


    def test_make_converter_kelvin_from_rankine_named(self):
        converter = self.kelvin.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_from_kelvin_named(self):
        converter = self.kelvin.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_degree_F_from_kelvin_base(self):
        converter = self.degree_F.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(-459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(0.0), 255.37222222222221)
        self.assertAlmostEqual(converter(32.0), 273.14999999999998)
        self.assertAlmostEqual(converter(212.0), 373.14999999999998)


    def test_make_converter_degree_F_from_rankine(self):
        converter = self.degree_F.make_converter(self.rankine)
        self.assertAlmostEqual(converter(-459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(0.0), 459.66999999999996)
        self.assertAlmostEqual(converter(32.0), 491.66999999999996)
        self.assertAlmostEqual(converter(212.0), 671.66999999999996)


    def test_make_converter_degree_F_from_kelvin(self):
        converter = self.degree_F.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(-459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(0.0), 255.37222222222221)
        self.assertAlmostEqual(converter(32.0), 273.14999999999998)
        self.assertAlmostEqual(converter(212.0), 373.14999999999998)


    def test_make_converter_degree_F_from_degree_F(self):
        converter = self.degree_F.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(-459.66999999999996), -459.66999999999996)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(32.0), 32.0)
        self.assertAlmostEqual(converter(212.0), 212.0)


    def test_make_converter_degree_F_from_degree_C(self):
        converter = self.degree_F.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(-459.66999999999996), -273.14999999999998)
        self.assertAlmostEqual(converter(0.0), -17.777777777777779)
        self.assertAlmostEqual(converter(32.0), 0.0)
        self.assertAlmostEqual(converter(212.0), 100.0)


    def test_make_converter_degree_F_from_rankine_named(self):
        converter = self.degree_F.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(-459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(0.0), 459.66999999999996)
        self.assertAlmostEqual(converter(32.0), 491.66999999999996)
        self.assertAlmostEqual(converter(212.0), 671.66999999999996)


    def test_make_converter_degree_F_from_kelvin_named(self):
        converter = self.degree_F.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(-459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(0.0), 255.37222222222221)
        self.assertAlmostEqual(converter(32.0), 273.14999999999998)
        self.assertAlmostEqual(converter(212.0), 373.14999999999998)


    def test_make_converter_degree_C_from_kelvin_base(self):
        converter = self.degree_C.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(-273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(-17.777777777777779), 255.37222222222221)
        self.assertAlmostEqual(converter(0.0), 273.14999999999998)
        self.assertAlmostEqual(converter(100.0), 373.14999999999998)


    def test_make_converter_degree_C_from_rankine(self):
        converter = self.degree_C.make_converter(self.rankine)
        self.assertAlmostEqual(converter(-273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(-17.777777777777779), 459.66999999999996)
        self.assertAlmostEqual(converter(0.0), 491.66999999999996)
        self.assertAlmostEqual(converter(100.0), 671.66999999999996)


    def test_make_converter_degree_C_from_kelvin(self):
        converter = self.degree_C.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(-273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(-17.777777777777779), 255.37222222222221)
        self.assertAlmostEqual(converter(0.0), 273.14999999999998)
        self.assertAlmostEqual(converter(100.0), 373.14999999999998)


    def test_make_converter_degree_C_from_degree_F(self):
        converter = self.degree_C.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(-273.14999999999998), -459.66999999999996)
        self.assertAlmostEqual(converter(-17.777777777777779), 0.0)
        self.assertAlmostEqual(converter(0.0), 32.0)
        self.assertAlmostEqual(converter(100.0), 212.0)


    def test_make_converter_degree_C_from_degree_C(self):
        converter = self.degree_C.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(-273.14999999999998), -273.14999999999998)
        self.assertAlmostEqual(converter(-17.777777777777779), -17.777777777777779)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(100.0), 100.0)


    def test_make_converter_degree_C_from_rankine_named(self):
        converter = self.degree_C.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(-273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(-17.777777777777779), 459.66999999999996)
        self.assertAlmostEqual(converter(0.0), 491.66999999999996)
        self.assertAlmostEqual(converter(100.0), 671.66999999999996)


    def test_make_converter_degree_C_from_kelvin_named(self):
        converter = self.degree_C.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(-273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(-17.777777777777779), 255.37222222222221)
        self.assertAlmostEqual(converter(0.0), 273.14999999999998)
        self.assertAlmostEqual(converter(100.0), 373.14999999999998)


    def test_make_converter_rankine_named_from_kelvin_base(self):
        converter = self.rankine_named.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_rankine_named_from_rankine(self):
        converter = self.rankine_named.make_converter(self.rankine)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 459.66999999999996)
        self.assertAlmostEqual(converter(491.66999999999996), 491.66999999999996)
        self.assertAlmostEqual(converter(671.66999999999996), 671.66999999999996)


    def test_make_converter_rankine_named_from_kelvin(self):
        converter = self.rankine_named.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_rankine_named_from_degree_F(self):
        converter = self.rankine_named.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(0.0), -459.66999999999996)
        self.assertAlmostEqual(converter(459.66999999999996), 0.0)
        self.assertAlmostEqual(converter(491.66999999999996), 32.0)
        self.assertAlmostEqual(converter(671.66999999999996), 212.0)


    def test_make_converter_rankine_named_from_degree_C(self):
        converter = self.rankine_named.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(0.0), -273.14999999999998)
        self.assertAlmostEqual(converter(459.66999999999996), -17.777777777777779)
        self.assertAlmostEqual(converter(491.66999999999996), 0.0)
        self.assertAlmostEqual(converter(671.66999999999996), 100.0)


    def test_make_converter_rankine_named_from_rankine_named(self):
        converter = self.rankine_named.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 459.66999999999996)
        self.assertAlmostEqual(converter(491.66999999999996), 491.66999999999996)
        self.assertAlmostEqual(converter(671.66999999999996), 671.66999999999996)


    def test_make_converter_rankine_named_from_kelvin_named(self):
        converter = self.rankine_named.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(459.66999999999996), 255.37222222222221)
        self.assertAlmostEqual(converter(491.66999999999996), 273.14999999999998)
        self.assertAlmostEqual(converter(671.66999999999996), 373.14999999999998)


    def test_make_converter_kelvin_named_from_kelvin_base(self):
        converter = self.kelvin_named.make_converter(self.kelvin_base)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_named_from_rankine(self):
        converter = self.kelvin_named.make_converter(self.rankine)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_named_from_kelvin(self):
        converter = self.kelvin_named.make_converter(self.kelvin)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)


    def test_make_converter_kelvin_named_from_degree_F(self):
        converter = self.kelvin_named.make_converter(self.degree_F)
        self.assertAlmostEqual(converter(0.0), -459.66999999999996)
        self.assertAlmostEqual(converter(255.37222222222221), 0.0)
        self.assertAlmostEqual(converter(273.14999999999998), 32.0)
        self.assertAlmostEqual(converter(373.14999999999998), 212.0)


    def test_make_converter_kelvin_named_from_degree_C(self):
        converter = self.kelvin_named.make_converter(self.degree_C)
        self.assertAlmostEqual(converter(0.0), -273.14999999999998)
        self.assertAlmostEqual(converter(255.37222222222221), -17.777777777777779)
        self.assertAlmostEqual(converter(273.14999999999998), 0.0)
        self.assertAlmostEqual(converter(373.14999999999998), 100.0)


    def test_make_converter_kelvin_named_from_rankine_named(self):
        converter = self.kelvin_named.make_converter(self.rankine_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 459.66999999999996)
        self.assertAlmostEqual(converter(273.14999999999998), 491.66999999999996)
        self.assertAlmostEqual(converter(373.14999999999998), 671.66999999999996)


    def test_make_converter_kelvin_named_from_kelvin_named(self):
        converter = self.kelvin_named.make_converter(self.kelvin_named)
        self.assertAlmostEqual(converter(0.0), 0.0)
        self.assertAlmostEqual(converter(255.37222222222221), 255.37222222222221)
        self.assertAlmostEqual(converter(273.14999999999998), 273.14999999999998)
        self.assertAlmostEqual(converter(373.14999999999998), 373.14999999999998)

