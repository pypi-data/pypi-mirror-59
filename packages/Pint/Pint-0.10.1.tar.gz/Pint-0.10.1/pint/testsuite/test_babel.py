import os

from pint import UnitRegistry
from pint.testsuite import BaseTestCase, helpers


class TestBabel(BaseTestCase):
    @helpers.requires_babel()
    def test_format(self):
        ureg = UnitRegistry()
        dirname = os.path.dirname(__file__)
        ureg.load_definitions(os.path.join(dirname, "../xtranslated.txt"))

        distance = 24.0 * ureg.meter
        self.assertEqual(
            distance.format_babel(locale="fr_FR", length="long"), "24.0 mètres"
        )
        time = 8.0 * ureg.second
        self.assertEqual(
            time.format_babel(locale="fr_FR", length="long"), "8.0 secondes"
        )
        self.assertEqual(time.format_babel(locale="ro", length="short"), "8.0 s")
        acceleration = distance / time ** 2
        self.assertEqual(
            acceleration.format_babel(locale="fr_FR", length="long"),
            "0.375 mètre par seconde²",
        )
        mks = ureg.get_system("mks")
        self.assertEqual(mks.format_babel(locale="fr_FR"), "métrique")

    @helpers.requires_babel()
    def test_registry_locale(self):
        ureg = UnitRegistry(fmt_locale="fr_FR")
        dirname = os.path.dirname(__file__)
        ureg.load_definitions(os.path.join(dirname, "../xtranslated.txt"))

        distance = 24.0 * ureg.meter
        self.assertEqual(distance.format_babel(length="long"), "24.0 mètres")
        time = 8.0 * ureg.second
        self.assertEqual(time.format_babel(length="long"), "8.0 secondes")
        self.assertEqual(time.format_babel(locale="ro", length="short"), "8.0 s")
        acceleration = distance / time ** 2
        self.assertEqual(
            acceleration.format_babel(length="long"), "0.375 mètre par seconde²"
        )
        mks = ureg.get_system("mks")
        self.assertEqual(mks.format_babel(locale="fr_FR"), "métrique")

    def test_nobabel(self):
        ureg = UnitRegistry()
        distance = 24.0 * ureg.meter
        self.assertRaises(
            Exception, distance.format_babel, locale="fr_FR", length="long"
        )
