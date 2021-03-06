"""
Exercise the map_tools applications.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header: /glast/ScienceTools/glast/sane/python/tests/map_tools_tests.py,v 1.1.1.1 2009/09/22 19:04:19 elwinter Exp $
#

from setPaths import *
from gt_apps import count_map

def run(useWorkAround=False):
    count_map['clobber'] = 'yes'
    count_map['chatter'] = 5
    count_map['mode'] = 'h'
    count_map['infile'] = 'test_events_0000.fits'
    count_map['table'] = 'EVENTS'
    if useWorkAround:
        count_map['filter'] = 'TIME>0'
    count_map['outfile'] = 'count_map.fits'
    count_map['ra_name'] = 'RA'
    count_map['dec_name'] = 'DEC'
    count_map['npix'] = 80
    count_map['npixy'] = 80
    count_map['pixelsize'] = 0.5
    count_map['xref'] = 89.0
    count_map['yref'] = 16.0
    count_map['rot'] = 0.0
    count_map['projtype'] = 'CAR'
    count_map['uselb'] = 'no'
    count_map.run(catchError=None)

if __name__ == "__main__":
    run()
