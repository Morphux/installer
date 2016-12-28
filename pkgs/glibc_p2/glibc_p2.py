################################### LICENSE ####################################
#                            Copyright 2016 Morphux                            #
#                                                                              #
#        Licensed under the Apache License, Version 2.0 (the "License");       #
#        you may not use this file except in compliance with the License.      #
#                  You may obtain a copy of the License at                     #
#                                                                              #
#                 http://www.apache.org/licenses/LICENSE-2.0                   #
#                                                                              #
#      Unless required by applicable law or agreed to in writing, software     #
#       distributed under the License is distributed on an "AS IS" BASIS,      #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#        See the License for the specific language governing permissions and   #
#                       limitations under the License.                         #
################################################################################

##
# glibc_p2.py
# Created: 13/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Glibc_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "glibc", # Name of the package
            "version": "2.24", # Version of the package
            "size": 1400, # Size of the installed package (MB)
            "archive": "glibc-2.24.tar.xz", # Archive name
            "SBU": 17, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "toolchain", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/glibc-2.24.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["patch", "-Np1", "-i", "../glibc-2.24-fhs-1.patch"], ignore=True)
        res = self.e(["mkdir", "-vp", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        return self.e(["../configure",
                "--prefix=/usr",
                "--enable-kernel=2.6.32",
                "--enable-obsolete-rpc"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["touch", "/etc/ld"])
        return self.e(["make", "install"])

    def     after(self):
        locales = [
            ("cs_CZ", "UTF-8", "cs_CZ.UTF-8"),
            ("de_DE", "ISO-8859-1", "de_DE"),
            ("de_DE@euro", "ISO-8859-15", "de_DE@euro"),
            ("de_DE", "UTF-8", "de_DE.UTF-8"),
            ("en_GB", "UTF-8", "en_GB.UTF-8"),
            ("en_HK", "ISO-8859-1", "en_HK"),
            ("en_PH", "IOS-8859-1", "en_PH"),
            ("en_US", "IOS-8859-1", "en_US"),
            ("en_US", "UTF-8", "en_US.UTF-8"),
            ("ex_MX", "ISO-8859-1", "es_MX"),
            ("fa_IR", "UTF-8", "fa_IR"),
            ("fr_FR", "ISO-8859-1", "fr_FR"),
            ("fr_FR@euro", "ISO-8859-15", "fr_FR@euro"),
            ("fr_FR", "UTF-8", "fr_FR.UTF-8"),
            ("it_IT", "ISO-8859-1", "it_IT"),
            ("it_IT", "UTF-8", "it_IT.UTF-8"),
            ("jp_JP", "EUC-JP", "ja_JP"),
            ("ru_RU", "KOI8-R", "ru_RU.KOI8-R"),
            ("ru_RU", "UTF-8", "ru_RU.UTF-8"),
            ("tr_TR", "UTF-8", "tr_TR.UTF-8"),
            ("zh_CN", "GB18030", "zh_CN.GB18030")
        ]
        zoneinfo="/usr/share/zoneinfo"
        locale_base = "America/New_York"

        self.e(["cp", "-v", "../nscd/nscd.conf", "/etc/nscd.conf"])
        self.e(["mkdir", "-pv", "/var/cache/nscd"])
        self.e(["mkdir", "-pv", "/usr/lib/locale"])

        for l in locales:
            self.e(["localedef", "-i", l[0], "-f", l[1], l[2]])

        self.e(["tar", "xf", "../../tzdata2016f.tar.gz"])
        self.e(["mkdir", "-pv", zoneinfo + "/{posix,right}"], shell=True)

        self.e(["for tz in etcetera southamerica northamerica europe africa antarctica \
                    asia australasia backward pacificnew systemv; do \
                zic -L /dev/null \
                -d", zoneinfo,
                "-y 'sh yearistype.sh' ${tz} \
                zic -L /dev/null \
                -d", zoneinfo, "/posix -y 'sh yearistype.sh' ${tz} \
                zic -L leapseconds -d ", zoneinfo,"/right -y 'sh yearistype.sh' ${tz} \
            done"
            ], shell=True)
        self.e(["cp", "-v", "zone.tab", "zone1970.tab", "iso3166.tab", zoneinfo])
        self.e(["zic", "-d", zoneinfo, "-p", "America/New_York"])
        self.e(["mkdir", "-pv", "/etc/ld.so.conf.d"])
        return self.e(["cp", "-v", "/usr/share/zoneinfo/" + locale_base, "/etc/localtime"])
