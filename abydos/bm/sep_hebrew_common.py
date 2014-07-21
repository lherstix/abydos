# -*- coding: utf-8 -*-
"""abydos.distance

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

This file is derived from PHP code by Alexander Beider and Stephen P. Morse that
is part of the Beider-Morse Phonetic Matching (BMPM) System, available at
http://stevemorse.org/phonetics/bmpm.htm.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""
             
             ('E','','',''),#finalFrench'e':onlyinSephardic
             
             ('ts','','','C'),#fornotconfusionGutes[=guts]andGuts[=guc]
             ('tS','','','C'),#samereason
             ('S','','','s'),
             ('p','','','f'),
             ('b','^','','b'),
             ('b','','','(b|v)'),
             
             ('ja','','','i'),
             ('je','','','i'),
             ('aj','','','i'),
             ('j','','','i'),
             
             ('a','^','','1'),
             ('e','^','','1'),
             ('a','','$','1'),
             ('e','','$','1'),
             
             ('a','','',''),
             ('e','','',''),
             
             ('oj','^','','(u|vi)'),
             ('uj','^','','(u|vi)'),
             
             ('oj','','','u'),
             ('uj','','','u'),
             
             ('ou','^','','(u|v|1)'),
             ('o','^','','(u|v|1)'),
             ('u','^','','(u|v|1)'),
             
             ('o','','$','(u|1)'),
             ('u','','$','(u|1)'),
             
             ('ou','','','u'),
             ('o','','','u'),
             
             ('VV','','','u'),#alef/ayin+vovfromruleshebrew
             ('L','^','','1'),#alef/ayinfromruleshebrew
             ('L','','$','1'),#alef/ayinfromruleshebrew
             ('L','','',''),#alef/ayinfromruleshebrew
             ('WW','^','','(vi|u)'),#vav-yodfromruleshebrew
             ('WW','','','u'),#vav-yodfromruleshebrew
             ('W','^','','(u|v)'),#vavfromruleshebrew
             ('W','','','u'),#vavfromruleshebrew
             
             #('g','','','(g|Z)'),
             #('z','','','(z|Z)'),
             #('d','','','(d|dZ)'),
             
             ('T','','','t'),#tetfromruleshebrew
             
             #('k','','','(k|x)'),
             #('x','','','(k|x)'),
             ('K','','','k'),#kofandinitialkaffromruleshebrew
             ('X','','','x'),#khetandfinalkaffromruleshebrew
             
             #specialforSpanishinitialB/V
             ('B','','','v'),
             ('V','','','b'),
             
             ('H','^','','(x|1)'),
             ('H','','$','(x|1)'),
             ('H','','','(x|)'),
             ('h','^','','1'),
             ('h','','',''),
             
             ('exactapproxcommonplushebrewcommon')