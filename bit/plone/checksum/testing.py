from plone.testing import z2

from plone.app.testing import PLONE_FIXTURE, TEST_USER_ID
from plone.app.testing import PloneSandboxLayer, IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles, applyProfile


class BitPloneChecksumTestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bit.plone.checksum
        self.loadZCML(package=bit.plone.checksum)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bit.plone.checksum:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'bit.plone.checksum')

CHECKSUM_TEST_FIXTURE = BitPloneChecksumTestLayer()
CHECKSUM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CHECKSUM_TEST_FIXTURE,),
    name="bit.plone.checksum:integration")
CHECKSUM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CHECKSUM_TEST_FIXTURE,),
    name="bit.plone.checksum:functional")
