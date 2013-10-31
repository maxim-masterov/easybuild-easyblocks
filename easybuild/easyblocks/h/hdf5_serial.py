##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing HDF5, implemented as an easyblock

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
"""

import os

import easybuild.tools.environment as env
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.modules import get_software_root


class EB_HDF5_serial(ConfigureMake):
    """Support for building/installing HDF5"""

    def configure_step(self):
        """Configure build: set require config and make options, and run configure script."""

        # Szip configure option -> --with-szlib
        szip_root = get_software_root("Szip")
        if szip_root:
            self.cfg.update('configopts', '--with-szlib=%s' % (szip_root))
        else:
            self.log.error("Dependency module Szip not loaded.")

        # zlib configure option -> --with-zlib
        zlib_root = get_software_root("zlib")
        if zlib_root:
            self.cfg.update('configopts', '--with-zlib=%s' % (zlib_root))
        else:
            self.log.error("Dependency module zlib not loaded.")


        fcomp = 'FC="%s"' % os.getenv('F90')

        self.cfg.update('configopts', "--with-pic --with-pthread --enable-shared")
        self.cfg.update('configopts', "--enable-cxx --enable-fortran %s" % fcomp)

        # C++ support enabled (MPI as well) requires --enable-unsupported, because this is untested by HDF5
        self.cfg.update('configopts', "--enable-unsupported")

        # make options
        self.cfg.update('makeopts', fcomp)

        super(EB_HDF5_serial, self).configure_step()

    # default make and make install are ok

    def sanity_check_step(self):
        """
        Custom sanity check for HDF5
        """

        extra_binaries = ["bin/%s" % x for x in ["h5cc", "h5fc"]]

        custom_paths = {
                        'files': ["bin/h5%s" % x for x in ["2gif", "c++", "copy", "debug", "diff",
                                                           "dump", "import", "jam","ls", "mkgrp",
                                                           "perf_serial", "redeploy", "repack",
                                                           "repart", "stat", "unjam"]] +
                                 ["bin/gif2h5"] + extra_binaries +
                                 ["lib/libhdf5%s.so" % x for x in ["_cpp", "_fortran", "_hl_cpp",
                                                                   "_hl", "hl_fortran", ""]],
                        'dirs': ['include']
                       }

        super(EB_HDF5_serial, self).sanity_check_step(custom_paths=custom_paths)
