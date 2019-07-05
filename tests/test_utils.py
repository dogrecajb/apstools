
"""
simple unit tests for this package
"""

from collections import OrderedDict
import os
import sys
import unittest

_path = os.path.dirname(__file__)
_path = os.path.join(_path, '..')
if _path not in sys.path:
    sys.path.insert(0, _path)

from apstools import utils as APS_utils
from apstools import __version__ as APS__version__
from common import Capture_stdout


RE = None


class Test_Utils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_cleanupText(self):
        original = "1. Some text to cleanup #25"
        received = APS_utils.cleanupText(original)
        expected = "1__Some_text_to_cleanup__25"
        self.assertEqual(received, expected)
    
    def test_device_read2table(self):
        from ophyd.sim import motor1
        table = APS_utils.device_read2table(motor1, show_ancient=True, use_datetime=True)
        # print(table)
        expected = """
=============== =====
name            value
=============== =====
motor1          0    
motor1_setpoint 0    
=============== =====
        """.strip()
        # TODO: figure out how to compare with timestamps
        received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
        self.assertEqual(received, expected)    # fails since timestamps do not match

        table = APS_utils.device_read2table(motor1, show_ancient=True, use_datetime=False)
        # expected = """ """.strip()
        received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
        self.assertEqual(received, expected)    # fails since timestamps do not match

        table = APS_utils.device_read2table(motor1, show_ancient=False, use_datetime=False)
        # expected = """ """.strip()
        received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
        self.assertEqual(received, expected)    # fails since timestamps do not match

    def test_dictionary_table(self):
        md = {
            'login_id': 'jemian:wow.aps.anl.gov', 
            'beamline_id': 'developer', 
            'proposal_id': None, 
            'pid': 19072, 
            'scan_id': 10, 
            'version': {
                'bluesky': '1.5.2', 
                'ophyd': '1.3.3', 
                'apstools': '1.1.5', 
                'epics': '3.3.3'
                }
              }
        table = APS_utils.dictionary_table(md)
        received = str(table).strip()
        expected = """
=========== =============================================================================
key         value                                                                        
=========== =============================================================================
beamline_id developer                                                                    
login_id    jemian:wow.aps.anl.gov                                                       
pid         19072                                                                        
proposal_id None                                                                         
scan_id     10                                                                           
version     {'bluesky': '1.5.2', 'ophyd': '1.3.3', 'apstools': '1.1.5', 'epics': '3.3.3'}
=========== =============================================================================
        """.strip()
        self.assertEqual(received, expected)

    def test_itemizer(self):
        items = [1.0, 1.1, 1.01, 1.001, 1.0001, 1.00001]
        received = APS_utils.itemizer("%.2f", items)
        expected = ["1.00", "1.10", "1.01", "1.00", "1.00", "1.00"]
        self.assertEqual(received, expected)

    def test_print_RE_md(self):
        global RE
        md = {}
        md["purpose"] = "testing"
        md["versions"] = dict(apstools=APS__version__)
        md["something"] = "else"

        with Capture_stdout() as received:
            APS_utils.print_RE_md(md)

        expected = [
            'RunEngine metadata dictionary:',
            '========= ================================',
            'key       value                           ',
            '========= ================================',
            'purpose   testing                         ',
            'something else                            ',
            'versions  ======== =======================',
            '          key      value                  ',
            '          ======== =======================',
            f'          apstools {APS__version__}',
            '          ======== =======================',
            '========= ================================',
            ''
            ]
        self.assertEqual(str(received), str(expected))

    def test_pairwise(self):
        items = [1.0, 1.1, 1.01, 1.001, 1.0001, 1.00001, 2]
        received = list(APS_utils.pairwise(items))
        expected = [(1.0, 1.1), (1.01, 1.001), (1.0001, 1.00001)]
        self.assertEqual(received, expected)

    def test_split_quoted_line(self):
        source = 'FlyScan 5   2   0   "empty container"'
        received = APS_utils.split_quoted_line(source)
        self.assertEqual(len(received), 5)
        expected = ['FlyScan', '5', '2', '0', 'empty container']
        self.assertEqual(received, expected)

    def test_trim_string_for_EPICS(self):
        source = "0123456789"
        self.assertLess(len(source), APS_utils.MAX_EPICS_STRINGOUT_LENGTH)
        received = APS_utils.trim_string_for_EPICS(source)
        self.assertEqual(len(source), len(received))
        expected = source
        self.assertEqual(received, expected)

        source = "0123456789"*10
        self.assertGreater(len(source), APS_utils.MAX_EPICS_STRINGOUT_LENGTH)
        received = APS_utils.trim_string_for_EPICS(source)
        self.assertGreater(len(source), len(received))
        expected = source[:APS_utils.MAX_EPICS_STRINGOUT_LENGTH-1]
        self.assertEqual(received, expected)


def suite(*args, **kw):
    test_list = [
        Test_Utils,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())