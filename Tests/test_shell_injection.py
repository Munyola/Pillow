import shutil

from PIL import GifImagePlugin, Image, JpegImagePlugin

from .helper import (
    PillowTestCase,
    cjpeg_available,
    djpeg_available,
    is_win32,
    netpbm_available,
    unittest,
)

TEST_JPG = "Tests/images/hopper.jpg"
TEST_GIF = "Tests/images/hopper.gif"

test_filenames = ("temp_';", 'temp_";', "temp_'\"|", "temp_'\"||", "temp_'\"&&")


@unittest.skipIf(is_win32(), "requires Unix or macOS")
class TestShellInjection(PillowTestCase):
    def assert_save_filename_check(self, src_img, save_func):
        for filename in test_filenames:
            dest_file = self.tempfile(filename)
            save_func(src_img, 0, dest_file)
            # If file can't be opened, shell injection probably occurred
            Image.open(dest_file).load()

    @unittest.skipUnless(djpeg_available(), "djpeg not available")
    def test_load_djpeg_filename(self):
        for filename in test_filenames:
            src_file = self.tempfile(filename)
            shutil.copy(TEST_JPG, src_file)

            im = Image.open(src_file)
            im.load_djpeg()

    @unittest.skipUnless(cjpeg_available(), "cjpeg not available")
    def test_save_cjpeg_filename(self):
        im = Image.open(TEST_JPG)
        self.assert_save_filename_check(im, JpegImagePlugin._save_cjpeg)

    @unittest.skipUnless(netpbm_available(), "netpbm not available")
    def test_save_netpbm_filename_bmp_mode(self):
        im = Image.open(TEST_GIF).convert("RGB")
        self.assert_save_filename_check(im, GifImagePlugin._save_netpbm)

    @unittest.skipUnless(netpbm_available(), "netpbm not available")
    def test_save_netpbm_filename_l_mode(self):
        im = Image.open(TEST_GIF).convert("L")
        self.assert_save_filename_check(im, GifImagePlugin._save_netpbm)
