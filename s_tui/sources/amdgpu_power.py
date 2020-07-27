#!/usr/bin/env python

# Copyright (C) 2020 Christian Schärf
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
"""
Read GPU power consumption from amdgpu driver
"""

from __future__ import absolute_import

from glob import glob

from s_tui.sources.source import Source
from s_tui.helper_functions import cat


class AmdgpuPowerSource(Source):

    POWER_INPUT_GLOB = "/sys/class/drm/card*/device/hwmon/hwmon*/power1_average"
    MICRO_WATT_IN_WATT = 1e6

    def __init__(self):
        Source.__init__(self)

        self.name = 'AMDGPU Power'
        self.measurement_unit = 'W'
        self.max_power = 1

        self.sources = glob(self.POWER_INPUT_GLOB)
        self.last_measurement = [0] * len(self.sources)
        self.available_sensors = ["GPU Power"] * len(self.sources)

    def update(self):
        self.last_measurement = list(map(lambda f: float(cat(f, binary=False))/self.MICRO_WATT_IN_WATT, self.sources))

    def get_maximum(self):
        return self.max_power

    def get_top(self):
        return 1
