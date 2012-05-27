import unittest
import doctest
from plone.testing import layered
from plone.app.testing import ploneSite
from zope.site.hooks import setHooks
from zope.site.hooks import setSite
from Testing.ZopeTestCase import FunctionalDocFileSuite

OPTION_FLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

from bit.plone.checksum.testing import CHECKSUM_FUNCTIONAL_TESTING


def setUp(self):
    with ploneSite() as portal:

        setHooks()
        setSite(portal)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
            layered(
                FunctionalDocFileSuite(
                    '../README.rst', optionflags=OPTION_FLAGS),
                layer=CHECKSUM_FUNCTIONAL_TESTING),
            ])
    return suite
