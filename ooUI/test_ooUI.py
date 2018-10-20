import unittest
import os
import ooUI

from json import JSONDecodeError
from unittest import TestCase


class TestAddonsUpdater(TestCase):
    def set_up(self):
        print('setUp...')

    def tear_down(self):
        print('tearDown...')

    def test_load_config(self):
        if not os.path.exists("./请配置这里.txt"):
            with self.assertRaises(FileNotFoundError):
                ooUI.AddonUpdater()

    def test_load_saved_info(self):
        if not os.path.exists("./savedInfo.txt"):
            with self.assertRaises(FileNotFoundError):
                ooUI.AddonsUpdater()

        with open("./savedInfo.txt",'r') as f:
            if f.read() is None:
                with self.assertRaises(JSONDecodeError):
                    au.load_saved_info()

    def test_get_addon_info(self):
        au = ooUI.AddonsUpdater()

        au.retrieve_addons_info()
        with open("./请配置这里.txt", 'r') as f:
            self.assertGreaterEqual(len(f.readlines()), au.count_of_addons)

    def test_download_addon(self):
        ooUI.AddonsUpdater()

    def test_if_need_update(self):
        ooUI.AddonsUpdater()

    def test_unzip_file(self):
        ooUI.AddonsUpdater()


if __name__ == '__main__':
    unittest.main()
