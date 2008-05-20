# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2008 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Test string formatting operations.
"""

import unittest
import os
import linkcheck.strformat


class TestStrFormat (unittest.TestCase):
    """
    Test string formatting routines.
    """

    def test_unquote (self):
        """
        Test quote stripping.
        """
        u = linkcheck.strformat.unquote
        self.assertEquals(u(""), "")
        self.assertEquals(u(None), None)
        self.assertEquals(u("'"), "'")
        self.assertEquals(u("\""), "\"")
        self.assertEquals(u("\"\""), "")
        self.assertEquals(u("''"), "")
        self.assertEquals(u("'a'"), "a")
        self.assertEquals(u("'a\"'"), "a\"")
        self.assertEquals(u("'\"a'"), "\"a")
        self.assertEquals(u('"a\'"'), 'a\'')
        self.assertEquals(u('"\'a"'), '\'a')
        self.assertEquals(u("'a'", matching=True), "a")
        self.assertEquals(u('"a"', matching=True), "a")
        # even mis-matching quotes should be removed...
        self.assertEquals(u("'a\""), "a")
        self.assertEquals(u("\"a'"), "a")
        # ...but not when matching is True
        self.assertEquals(u("'a\"", matching=True), "'a\"")
        self.assertEquals(u("\"a'", matching=True), "\"a'")

    def test_wrap (self):
        """
        Test line wrapping.
        """
        wrap = linkcheck.strformat.wrap
        s = "11%(sep)s22%(sep)s33%(sep)s44%(sep)s55" % {'sep': os.linesep}
        # testing width <= 0
        self.assertEquals(wrap(s, -1), s)
        self.assertEquals(wrap(s, 0), s)
        l = len(os.linesep)
        gap = " "*l
        s2 = "11%(gap)s22%(sep)s33%(gap)s44%(sep)s55" % \
             {'sep': os.linesep, 'gap': gap}
        # splitting lines
        self.assertEquals(wrap(s2, 2), s)
        # combining lines
        self.assertEquals(wrap(s, 4+l), s2)
        # misc
        self.assertEquals(wrap(s, -1), s)
        self.assertEquals(wrap(s, 0), s)
        self.assertEquals(wrap(None, 10), None)
        self.assertFalse(linkcheck.strformat.get_paragraphs(None))


    def test_remove_markup (self):
        """
        Test markup removing.
        """
        self.assertEquals(linkcheck.strformat.remove_markup("<a>"), "")
        self.assertEquals(linkcheck.strformat.remove_markup("<>"), "")
        self.assertEquals(linkcheck.strformat.remove_markup("<<>"), "")
        self.assertEquals(linkcheck.strformat.remove_markup("a < b"), "a < b")

    def test_strsize (self):
        """
        Test byte size strings.
        """
        self.assertRaises(ValueError, linkcheck.strformat.strsize, -1)
        self.assertEquals(linkcheck.strformat.strsize(0), "0B")
        self.assertEquals(linkcheck.strformat.strsize(1), "1B")
        self.assertEquals(linkcheck.strformat.strsize(2), "2B")
        self.assertEquals(linkcheck.strformat.strsize(1023), "1023B")
        self.assertEquals(linkcheck.strformat.strsize(1024), "1KB")
        self.assertEquals(linkcheck.strformat.strsize(1024*25), "25.00KB")
        self.assertEquals(linkcheck.strformat.strsize(1024*1024), "1.00MB")
        self.assertEquals(linkcheck.strformat.strsize(1024*1024*11), "11.0MB")
        self.assertEquals(linkcheck.strformat.strsize(1024*1024*1024),
            "1.00GB")
        self.assertEquals(linkcheck.strformat.strsize(1024*1024*1024*14),
            "14.0GB")

    def test_is_ascii (self):
        self.assert_(linkcheck.strformat.is_ascii("abcd./"))
        self.assert_(not linkcheck.strformat.is_ascii("�"))
        self.assert_(not linkcheck.strformat.is_ascii(u"�"))

    def test_indent (self):
        s = "bla"
        self.assertEqual(linkcheck.strformat.indent(s, ""), s)
        self.assertEqual(linkcheck.strformat.indent(s, " "), " "+s)

    def test_stripall (self):
        self.assertEqual(linkcheck.strformat.stripall("a\tb"), "ab")
        self.assertEqual(linkcheck.strformat.stripall(" a\t b"), "ab")
        self.assertEqual(linkcheck.strformat.stripall(" \r\na\t \nb\r"), "ab")
        self.assertEqual(linkcheck.strformat.stripall(None), None)

    def test_limit (self):
        self.assertEqual(linkcheck.strformat.limit("", 0), "")
        self.assertEqual(linkcheck.strformat.limit("a", 0), "")
        self.assertEqual(linkcheck.strformat.limit("1", 1), "1")
        self.assertEqual(linkcheck.strformat.limit("11", 1), "1...")

    def test_strtime (self):
        zone = linkcheck.strformat.strtimezone()
        t = linkcheck.strformat.strtime(0)
        self.assertEqual(t, "1970-01-01 01:00:00"+zone)

    def test_duration (self):
        duration = linkcheck.strformat.strduration
        self.assertEqual(duration(-0.5), "-00:01")
        self.assertEqual(duration(0), "00:00")
        self.assertEqual(duration(0.9), "00:01")
        self.assertEqual(duration(1), "00:01")
        self.assertEqual(duration(2), "00:02")
        self.assertEqual(duration(60), "01:00")
        self.assertEqual(duration(120), "02:00")
        self.assertEqual(duration(60*60), "01:00:00")
        self.assertEqual(duration(60*60*24), "24:00:00")

    def test_duration_long (self):
        duration = linkcheck.strformat.strduration_long
        self.assertEqual(duration(-0.5), "-0.50 seconds")
        self.assertEqual(duration(0), "0.00 seconds")
        self.assertEqual(duration(0.9), "0.90 seconds")
        self.assertEqual(duration(1), "1 second")
        self.assertEqual(duration(2), "2 seconds")
        self.assertEqual(duration(60), "1 minute")
        self.assertEqual(duration(120), "2 minutes")
        self.assertEqual(duration(60*60), "1 hour")
        self.assertEqual(duration(60*60*24), "1 day")
        self.assertEqual(duration(60*60*24*365), "1 year")
        self.assertEqual(duration(60*60*24*365 + 60*60*24 + 2),
                         "1 year, 1 day")

    def test_linenumber (self):
        get_line_number = linkcheck.strformat.get_line_number
        self.assertEqual(get_line_number("a", -5), 0)
        self.assertEqual(get_line_number("a", 0), 1)
        self.assertEqual(get_line_number("a\nb", 2), 2)

    def test_encoding (self):
        is_encoding = linkcheck.strformat.is_encoding
        self.assert_(is_encoding('ascii'))
        self.assertFalse(is_encoding('hulla'))

    def test_unicode_safe (self):
        unicode_safe = linkcheck.strformat.unicode_safe
        self.assertEqual(unicode_safe("a"), u"a")
        self.assertEqual(unicode_safe(u"a"), u"a")

    def test_ascii_safe (self):
        ascii_safe = linkcheck.strformat.ascii_safe
        self.assertEqual(ascii_safe("a"), "a")
        self.assertEqual(ascii_safe(u"a"), "a")
        self.assertEqual(ascii_safe(u"�"), "")


def test_suite ():
    """
    Build and return a TestSuite.
    """
    return unittest.makeSuite(TestStrFormat)


if __name__ == '__main__':
    unittest.main()