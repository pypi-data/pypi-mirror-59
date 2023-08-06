from psyneulink.core.components.functions.transferfunctions import Linear
from psyneulink.core.components.mechanisms.processing.objectivemechanism import ObjectiveMechanism
from psyneulink.core.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.core.components.process import Process
from psyneulink.core.components.system import System
from psyneulink.core.globals.keywords import ALL, ENABLED
from psyneulink.library.components.mechanisms.modulatory.control.agt.lccontrolmechanism import LCControlMechanism

class TestSimpleSystems:

    def test_process(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        p = Process(name="p",
                    pathway=[a, b])
        s = System(name="s",
                   processes=[p])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label

    def test_diverging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        p = Process(name="p",
                    pathway=[a, b])
        p2 = Process(name="p2",
                    pathway=[a, c])
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label

    def test_converging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        p = Process(name="p",
                    pathway=[a, c])
        p2 = Process(name="p2",
                    pathway=[b, c])
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label

class TestLearning:

    def test_process(self):
        a = TransferMechanism(name="a-sg",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b-sg")
        p = Process(name="p",
                    pathway=[a, b],
                    learning=ENABLED)
        s = System(name="s",
                   processes=[p])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label

    def test_diverging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        p = Process(name="p",
                    pathway=[a, b],
                    learning=ENABLED)
        p2 = Process(name="p2",
                    pathway=[a, c],
                     learning=ENABLED)
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label

    def test_converging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        p = Process(name="p",
                    pathway=[a, c],
                    learning=ENABLED)
        p2 = Process(name="p2",
                    pathway=[b, c],
                     learning=ENABLED)
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label

class TestControl:

    def test_process(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        LC = LCControlMechanism(modulated_mechanisms=[a,b],
                                objective_mechanism=ObjectiveMechanism(function=Linear,
                                                                       monitor=[b],
                                                                       name='lc_om'),
                                name="lc"
                                )
        p = Process(name="p",
                    pathway=[a, b])
        s = System(name="s",
                   processes=[p])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label

    def test_diverging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        LC = LCControlMechanism(modulated_mechanisms=[a,b],
                                objective_mechanism=ObjectiveMechanism(function=Linear,
                                                                       monitor=[b],
                                                                       name='lc_om'),
                                name="lc"
                                )
        p = Process(name="p",
                    pathway=[a, b])
        p2 = Process(name="p2",
                    pathway=[a, c])
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label

    def test_converging_pathways(self):
        a = TransferMechanism(name="a",
                              default_variable=[0, 0, 0])
        b = TransferMechanism(name="b")
        c = TransferMechanism(name="c",
                              default_variable=[0, 0, 0, 0, 0])
        LC = LCControlMechanism(modulated_mechanisms=[a,b],
                                objective_mechanism=ObjectiveMechanism(function=Linear,
                                                                       monitor=[b],
                                                                       name='lc_om'),
                                name="lc"
                                )
        p = Process(name="p",
                    pathway=[a, c])
        p2 = Process(name="p2",
                    pathway=[b, c])
        s = System(name="s",
                   processes=[p, p2])

        a_label = s._get_label(a, ALL)
        b_label = s._get_label(b, ALL)
        c_label = s._get_label(c, ALL)

        assert "out (3)" in a_label and "in (3)" in a_label
        assert "out (1)" in b_label and "in (1)" in b_label
        assert "out (5)" in c_label and "in (5)" in c_label
