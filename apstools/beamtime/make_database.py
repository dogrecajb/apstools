#!/usr/bin/env python

"""
Create the EPICS database
"""

import os
import sys

#name	RTYP	length

raw_data = """
esaf:cycle	stringout	
esaf:description	waveform	4096
esaf:endDate	stringout	
esaf:id	stringout	
esaf:status	stringout	
esaf:sector	stringout	
esaf:startDate	stringout	
esaf:title	waveform	1024
esaf:userBadges	waveform	1024
esaf:users	waveform	1024
esaf:user1:badgeNumber	stringout	
esaf:user1:email	stringout	
esaf:user1:firstName	stringout	
esaf:user1:lastName	stringout	
esaf:user2:badgeNumber	stringout	
esaf:user2:email	stringout	
esaf:user2:firstName	stringout	
esaf:user2:lastName	stringout	
esaf:user3:badgeNumber	stringout	
esaf:user3:email	stringout	
esaf:user3:firstName	stringout	
esaf:user3:lastName	stringout	
esaf:user4:badgeNumber	stringout	
esaf:user4:email	stringout	
esaf:user4:firstName	stringout	
esaf:user4:lastName	stringout	
esaf:user5:badgeNumber	stringout	
esaf:user5:email	stringout	
esaf:user5:firstName	stringout	
esaf:user5:lastName	stringout	
esaf:user6:badgeNumber	stringout	
esaf:user6:email	stringout	
esaf:user6:firstName	stringout	
esaf:user6:lastName	stringout	
esaf:user7:badgeNumber	stringout	
esaf:user7:email	stringout	
esaf:user7:firstName	stringout	
esaf:user7:lastName	stringout	
esaf:user8:badgeNumber	stringout	
esaf:user8:email	stringout	
esaf:user8:firstName	stringout	
esaf:user8:lastName	stringout	
esaf:user9:badgeNumber	stringout	
esaf:user9:email	stringout	
esaf:user9:firstName	stringout	
esaf:user9:lastName	stringout	
proposal:beamline	stringout	
proposal:mailInFlag	bo	
proposal:id	stringout	
proposal:proprietaryFlag	bo	
proposal:submittedDate	stringout	
proposal:title	waveform	1024
proposal:userBadges	waveform	1024
proposal:users	waveform	1024
proposal:user1:badgeNumber	stringout	
proposal:user1:email	stringout	
proposal:user1:firstName	stringout	
proposal:user1:institution	waveform	1024
proposal:user1:instId	stringout	
proposal:user1:lastName	stringout	
proposal:user1:piFlag	bo	
proposal:user1:userId	stringout	
proposal:user2:badgeNumber	stringout	
proposal:user2:email	stringout	
proposal:user2:firstName	stringout	
proposal:user2:institution	waveform	1024
proposal:user2:instId	stringout	
proposal:user2:lastName	stringout	
proposal:user2:piFlag	bo	
proposal:user2:userId	stringout	
proposal:user3:badgeNumber	stringout	
proposal:user3:email	stringout	
proposal:user3:firstName	stringout	
proposal:user3:institution	waveform	1024
proposal:user3:instId	stringout	
proposal:user3:lastName	stringout	
proposal:user3:piFlag	bo	
proposal:user3:userId	stringout	
proposal:user4:badgeNumber	stringout	
proposal:user4:email	stringout	
proposal:user4:firstName	stringout	
proposal:user4:institution	waveform	1024
proposal:user4:instId	stringout	
proposal:user4:lastName	stringout	
proposal:user4:piFlag	bo	
proposal:user4:userId	stringout	
proposal:user5:badgeNumber	stringout	
proposal:user5:email	stringout	
proposal:user5:firstName	stringout	
proposal:user5:institution	waveform	1024
proposal:user5:instId	stringout	
proposal:user5:lastName	stringout	
proposal:user5:piFlag	bo	
proposal:user5:userId	stringout	
proposal:user6:badgeNumber	stringout	
proposal:user6:email	stringout	
proposal:user6:firstName	stringout	
proposal:user6:institution	waveform	1024
proposal:user6:instId	stringout	
proposal:user6:lastName	stringout	
proposal:user6:piFlag	bo	
proposal:user6:userId	stringout	
proposal:user7:badgeNumber	stringout	
proposal:user7:email	stringout	
proposal:user7:firstName	stringout	
proposal:user7:institution	waveform	1024
proposal:user7:instId	stringout	
proposal:user7:lastName	stringout	
proposal:user7:piFlag	bo	
proposal:user7:userId	stringout	
proposal:user8:badgeNumber	stringout	
proposal:user8:email	stringout	
proposal:user8:firstName	stringout	
proposal:user8:institution	waveform	1024
proposal:user8:instId	stringout	
proposal:user8:lastName	stringout	
proposal:user8:piFlag	bo	
proposal:user8:userId	stringout	
proposal:user9:badgeNumber	stringout	
proposal:user9:email	stringout	
proposal:user9:firstName	stringout	
proposal:user9:institution	waveform	1024
proposal:user9:instId	stringout	
proposal:user9:lastName	stringout	
proposal:user9:piFlag	bo	
proposal:user9:userId	stringout	
""".strip().splitlines()

for row in raw_data:
    parts = row.split()
    pvname, rtyp = parts[:2]
    head = f'record({rtyp}, "$(P){pvname}")'
    fields = []
    if rtyp == "waveform" and len(parts) == 3:
        length = parts[-1]
        fields.append(f'field(FTVL, "CHAR")')
        fields.append(f'field(NELM, {length})')
    elif rtyp == "bo":
        fields.append(f'field(ZNAM, "OFF")')
        fields.append(f'field(ONAM, "ON")')
    record = head
    newline = "\n"
    if len(fields) > 0:
        field_specs = "\n".join([f"    {field}" for field in fields])
        record += " {\n" + f"{field_specs}" + "\n}"
    print(record + "\n")
