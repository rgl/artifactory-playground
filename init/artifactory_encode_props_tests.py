#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from io import StringIO

from artifactory_encode_props import (
    artifactory_encode_prop_value,
    artifactory_encode_props,
    main,
)


class TestArtifactoryEncodePropValue(unittest.TestCase):
    def test_basic_values(self):
        self.assertEqual(artifactory_encode_prop_value("plain_value"), "plain_value")
        self.assertEqual(artifactory_encode_prop_value(""), "")
        self.assertEqual(
            artifactory_encode_prop_value("  spaced value  "), "  spaced value  "
        )

    def test_special_characters(self):
        self.assertEqual(artifactory_encode_prop_value("back\\slash"), "back\\\\slash")
        self.assertEqual(artifactory_encode_prop_value("comma,value"), "comma\\,value")
        self.assertEqual(artifactory_encode_prop_value("semi;value"), "semi\\;value")
        self.assertEqual(artifactory_encode_prop_value("pipe|value"), "pipe\\|value")

    def test_multiple_special_chars(self):
        self.assertEqual(
            artifactory_encode_prop_value("all\\special,chars;here|now"),
            "all\\\\special\\,chars\\;here\\|now",
        )


class TestArtifactoryEncodeProps(unittest.TestCase):
    def test_single_property(self):
        self.assertEqual(artifactory_encode_props(["key=value"]), "key=value")
        self.assertEqual(artifactory_encode_props(["key=  value  "]), "key=  value  ")

    def test_multiple_values_same_key(self):
        self.assertEqual(
            artifactory_encode_props(["key=val1", "key=val2"]), "key=val1,val2"
        )

    def test_multiple_keys(self):
        self.assertEqual(artifactory_encode_props(["k1=v1", "k2=v2"]), "k1=v1;k2=v2")

    def test_complex_case(self):
        self.assertEqual(
            artifactory_encode_props(
                [
                    "key1=value1",
                    "key1=value2",
                    "key2=value1,a,  b  b  ;c",
                    "key2=value2",
                    "key3=  last-value  ",
                ]
            ),
            "key1=value1,value2;key2=value1\\,a\\,  b  b  \\;c,value2;key3=  last-value  ",
        )


class TestMainFunction(unittest.TestCase):
    @patch("sys.argv", ["script.py", "key=value"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_single_arg(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "key=value")

    @patch("sys.argv", ["script.py", "key1=val1", "key1=val2", "key2=val3"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_multiple_args(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "key1=val1,val2;key2=val3")

    @patch("sys.argv", ["script.py", "key=special\\,chars;here|now"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_special_chars(self, mock_stdout):
        main()
        self.assertEqual(
            mock_stdout.getvalue().strip(), "key=special\\\\\\,chars\\;here\\|now"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
