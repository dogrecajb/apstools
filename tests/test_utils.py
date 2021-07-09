"""
simple unit tests for this package
"""


from apstools import __version__ as APS__version__
from apstools import utils as APS_utils
import databroker
import numpy as np
import ophyd.sim
import os
import pytest
import sys
import time


CATALOG = "usaxs_test"
COUNT = "555a604"  # <-- uid,  scan_id: 2
RE = None


@pytest.fixture(scope="function")
def cat():
    cat = databroker.catalog[CATALOG]
    return cat


def test_utils_cleanupText():
    original = "1. Some text to cleanup #25"
    received = APS_utils.cleanupText(original)
    expected = "1__Some_text_to_cleanup__25"
    assert received == expected


def test_utils_listdevice():
    motor1 = ophyd.sim.hw().motor1
    table = APS_utils.listdevice(motor1, show_ancient=True, use_datetime=True)
    expected = (
        "=============== =====\n"
        "name            value\n"
        "=============== =====\n"
        "motor1          0    \n"
        "motor1_setpoint 0    \n"
        "=============== ====="
    )
    received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
    assert received == expected

    table = APS_utils.listdevice(motor1, show_ancient=True, use_datetime=False)
    # expected = """ """.strip()
    received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
    assert received == expected

    table = APS_utils.listdevice(motor1, show_ancient=False, use_datetime=False)
    # expected = """ """.strip()
    received = "\n".join([v[:21] for v in str(table).strip().splitlines()])
    assert received == expected


def test_utils_dictionary_table():
    md = {
        "login_id": "jemian:wow.aps.anl.gov",
        "beamline_id": "developer",
        "proposal_id": None,
        "pid": 19072,
        "scan_id": 10,
        "version": {
            "bluesky": "1.5.2",
            "ophyd": "1.3.3",
            "apstools": "1.1.5",
            "epics": "3.3.3",
        },
    }
    table = APS_utils.dictionary_table(md)
    received = str(table).strip()
    expected = (
        "=========== =============================================================================\n"
        "key         value                                                                        \n"
        "=========== =============================================================================\n"
        "beamline_id developer                                                                    \n"
        "login_id    jemian:wow.aps.anl.gov                                                       \n"
        "pid         19072                                                                        \n"
        "proposal_id None                                                                         \n"
        "scan_id     10                                                                           \n"
        "version     {'bluesky': '1.5.2', 'ophyd': '1.3.3', 'apstools': '1.1.5', 'epics': '3.3.3'}\n"
        "=========== ============================================================================="
    )
    assert received == expected


def test_utils_itemizer():
    items = [1.0, 1.1, 1.01, 1.001, 1.0001, 1.00001]
    received = APS_utils.itemizer("%.2f", items)
    expected = ["1.00", "1.10", "1.01", "1.00", "1.00", "1.00"]
    assert received == expected


def test_utils_print_RE_md(capsys):
    global RE
    md = {}
    md["purpose"] = "testing"
    md["versions"] = dict(apstools=APS__version__)
    md["something"] = "else"

    APS_utils.print_RE_md(md)
    out, err = capsys.readouterr()
    received = out.splitlines()

    expected = [
        "RunEngine metadata dictionary:",
        "========= ===============================",
        "key       value                          ",
        "========= ===============================",
        "purpose   testing                        ",
        "something else                           ",
        "versions  ======== ======================",
        "          key      value                 ",
        "          ======== ======================",
        f"          apstools {APS__version__}",
        "          ======== ======================",
        "========= ===============================",
        "",
    ]
    assert len(received) == len(expected)
    assert received[4].strip() == expected[4].strip()
    assert received[5].strip() == expected[5].strip()
    assert received[9].strip() == expected[9].strip()


def test_utils_pairwise():
    items = [1.0, 1.1, 1.01, 1.001, 1.0001, 1.00001, 2]
    received = list(APS_utils.pairwise(items))
    expected = [(1.0, 1.1), (1.01, 1.001), (1.0001, 1.00001)]
    assert received == expected


@pytest.mark.parametrize(
    "given, expected",
    [
        ["simple", "simple"],
        ["sim_ple", "sim_ple"],
        ["hy-phen", "hy_phen"],
        ["white space", "white_space"],
        ["1world", "_1world"],
        ["end9", "end9"],
        ["$tree", "_tree"],
        ["#!bang", "__bang"],
        ["0 is not a good name", "_0_is_not_a_good_name"],
        ["! is even worse!", "__is_even_worse_"],
        ["double.dotted.name", "double_dotted_name"],
    ],
)
def test_utils_safe_ophyd_name(given, expected):
    received = APS_utils.safe_ophyd_name(given)
    assert received == expected


def test_utils_split_quoted_line():
    source = 'FlyScan 5   2   0   "empty container"'
    received = APS_utils.split_quoted_line(source)
    assert len(received) == 5
    expected = ["FlyScan", "5", "2", "0", "empty container"]
    assert received == expected


def test_utils_trim_string_for_EPICS():
    source = "0123456789"
    assert len(source) < APS_utils.MAX_EPICS_STRINGOUT_LENGTH
    received = APS_utils.trim_string_for_EPICS(source)
    assert len(source) == len(received)
    expected = source
    assert received == expected

    source = "0123456789" * 10
    assert len(source) > APS_utils.MAX_EPICS_STRINGOUT_LENGTH
    received = APS_utils.trim_string_for_EPICS(source)
    assert len(source) > len(received)
    expected = source[: APS_utils.MAX_EPICS_STRINGOUT_LENGTH - 1]
    assert received == expected


def test_utils_listobjects():
    sims = ophyd.sim.hw().__dict__
    wont_show = (
        "flyer1",
        "flyer2",
        "new_trivial_flyer",
        "trivial_flyer",
    )
    num = len(sims) - len(wont_show)
    kk = sorted(sims.keys())

    table = APS_utils.listobjects(symbols=sims, printing=False)
    assert 4 == len(table.labels)
    rr = [r[0] for r in table.rows]
    for k in kk:
        if k not in wont_show:
            assert k in rr
    assert num == len(table.rows)


def test_utils_unix():
    cmd = 'echo "hello"'
    out, err = APS_utils.unix(cmd)
    assert out == b"hello\n"
    assert err == b""

    cmd = "sleep 0.8 | echo hello"
    t0 = time.time()
    out, err = APS_utils.unix(cmd)
    dt = time.time() - t0
    assert dt >= 0.8
    assert out == b"hello\n"
    assert err == b""


def test_utils_with_database_listruns(cat):
    assert len(list(cat.v1[COUNT].documents())[:1]) == 1
    df = APS_utils.listruns(cat=cat, printing=False, num=10)
    assert df is not None
    assert len(df.columns) == 4

    assert "time" in df
    assert df.columns[1] == "time"
    ts = df["time"]
    assert len(ts) == 10
    assert (ts == np.sort(ts)[::-1]).all()


def test_utils_with_database_listruns_v1_4(cat):
    assert len(list(cat.v1[COUNT].documents())[:1]) == 1
    table = APS_utils.listruns_v1_4(db=cat, show_command=True, printing=False, num=10,)
    assert table is not None
    assert len(table.labels) == 3 + 2  # requested 2 extra columns
    assert len(table.rows) == 10
    assert len(table.rows[1][4]) <= 40

    assert table.labels[1] == "date/time"  # "second column is ISO8601 date/time"
    ts = [row[1] for row in table.rows]
    assert ts == sorted(ts, reverse=True)


def test_utils_with_database_replay(cat):
    replies = []

    def cb1(key, doc):
        replies.append((key, len(doc)))

    APS_utils.replay(cat.v1[COUNT], callback=cb1)
    assert len(replies) > 0
    keys = set([v[0] for v in replies])
    # doc_types = "start stop event descriptor datum resource".split()
    doc_types = "start stop event descriptor".split()
    for item in doc_types:
        assert item in keys

    def cb2(key, doc):
        if key == "start":
            replies.append(doc["time"])

    replies = []
    APS_utils.replay(cat.v1[-1], callback=cb2)
    assert len(replies) == 1  # last run

    replies = []
    APS_utils.replay(cat.v1[-3:], callback=cb2)
    assert len(replies) == 3  # last 3 runs

    replies = []
    APS_utils.replay(cat.v1[COUNT], callback=cb2)
    previous = 0
    for i, v in enumerate(replies):
        assert v - previous > 0
        previous = v

    replies = []
    APS_utils.replay(cat.v1[-1], callback=cb2, sort=False)
    previous = replies[0] + 1
    for i, v in enumerate(replies):
        assert v - previous < 0
        previous = v


@pytest.mark.parametrize(
    "scan_id, stream, total_keys, key, m3, m_default, m_strict, m_lower",
    [
        (103, "primary", 7, "PD_USAXS", 1, 1, 1, 0),
        (103, None, 7, "PD_USAXS", 1, 1, 1, 0),
        (2, "primary", 5, "scaler0", 2, 2, 2, 2),
        (2, None, 5, "scaler0", 2, 2, 2, 2),
    ],
)
def test_utils_listRunKeys(
    scan_id, stream, total_keys, key, m3, m_default, m_strict, m_lower, cat
):
    assert len(APS_utils.listRunKeys(scan_id, db=cat, stream=stream)) == total_keys

    result = APS_utils.listRunKeys(
        scan_id, key_fragment=key[0:3], db=cat, stream=stream
    )
    assert len(result) == m3

    result = APS_utils.listRunKeys(scan_id, key_fragment=key, db=cat, stream=stream)
    assert len(result) == m_default

    result = APS_utils.listRunKeys(
        scan_id, key_fragment=key, db=cat, stream=stream, strict=True
    )
    assert len(result) == m_strict

    result = APS_utils.listRunKeys(
        scan_id, key_fragment=key.lower(), db=cat, stream=stream, strict=True
    )
    assert len(result) == m_lower


# fmt: off
@pytest.mark.parametrize(
    "scan_id, stream",
    [
        (110, None),
        (110, "primary"),
        (103, "mca"),
    ],
)
def test_utils_listRunKeys_no_such_stream(scan_id, stream, cat):
    with pytest.raises(AttributeError) as exc:
        APS_utils.listRunKeys(scan_id, db=cat, stream=stream)
    assert str(exc.value).startswith("No such stream ")
# fmt: on


@pytest.mark.parametrize(
    "scan_id, stream, nkeys",
    [
        (2, None, 5),
        (2, "primary", 5),
        (103, "primary", 7),
        (103, "baseline", 268),  # very slow test!
    ],
)
def test_utils_getRunData(scan_id, stream, nkeys, cat):
    table = APS_utils.getRunData(scan_id, db=cat, stream=stream)
    assert table is not None
    assert len(table.keys()) == nkeys


@pytest.mark.parametrize(
    "scan_id, stream, key, idx, expected, prec",
    [
        (2, "baseline", "undulator_downstream_version", None, "4.21", 0),
        (2, "primary", "I0_USAXS", -1, 3729, 0),
        (2, "primary", "I0_USAXS", "-1", 3729, 0),
        (2, "primary", "I0_USAXS", "all", [3729.0, ], 0),
        (2, "primary", "I0_USAXS", None, 3729, 0),
        (2, None, "I0_USAXS", "all", [3729.0, ], 0),
        (103, "baseline", "undulator_downstream_version", None, "4.21", 0),
        (103, "primary", "a_stage_r", -1, 8.88197, 5),
        (103, "primary", "a_stage_r", "mean", 8.88397, 5),
        (103, "primary", "a_stage_r", 0, 8.88597, 5),
        (103, "primary", "a_stage_r", None, 8.88197, 5),
        (110, "baseline", "terms_SAXS_UsaxsSaxsMode", None, "blank", 0),
        (110, "baseline", "user_data_sample_thickness", None, 0.0, 1),
        (110, "baseline", "user_data_scan_macro", None, "FlyScan", 0),
    ],
)
def test_utils_getRunDataValue(scan_id, stream, key, idx, expected, prec, cat):
    value = APS_utils.getRunDataValue(scan_id, key, db=cat, stream=stream, idx=idx)
    if isinstance(value, str):
        assert value == expected
    elif isinstance(value, float):
        assert round(value, prec) == expected
    elif isinstance(value, np.ndarray):
        assert len(value) == len(expected)
        for v, e in zip(value, expected):
            assert round(v, prec) == e


# fmt: off
@pytest.mark.parametrize(
    "scan_id, stream, key, idx, expected, prec",
    [
        (110, "mca", "struck_mca3_elapsed_real_time", None, 93.72, 2),
    ],
)
def test_utils_getRunDataValue_MemoryError(
    scan_id, stream, key, idx, expected, prec, cat
):
    with pytest.raises(np.core._exceptions._ArrayMemoryError) as exc:
        APS_utils.getRunDataValue(
            scan_id, key, db=cat, stream=stream, idx=idx
        )
    assert str(exc.value).startswith("Unable to allocate ")
# fmt: on
