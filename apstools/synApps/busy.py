"""
Ophyd support for the EPICS busy record


Public Structures

.. autosummary::

    ~BusyRecord

"""

from ophyd import EpicsSignal
from ophyd.device import Component
from ophyd.device import Device


class BusyRecord(Device):
    """
    EPICS synApps busy record

    .. index:: Ophyd Device; synApps BusyRecord
    """

    state = Component(EpicsSignal, "", kind="hinted")
    output_link = Component(EpicsSignal, ".OUT", kind="config")
    forward_link = Component(EpicsSignal, ".FLNK", kind="config")


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     jemian@anl.gov
# :copyright: (c) 2017-2023, UChicago Argonne, LLC
#
# Distributed under the terms of the Argonne National Laboratory Open Source License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
