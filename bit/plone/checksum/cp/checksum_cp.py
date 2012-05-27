from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from bit.plone.cp.interfaces import IControlPanel
from bit.plone.cp.cp import ControlPanel


class ChecksumCP(ControlPanel):
    implements(IControlPanel)

    def __init__(self, context):
        self.context = context

    def get_title(self):
        return 'Checksums'

    def get_data(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(object_provides='bit.content.checksum.interfaces.IChecksummable')
        csums = {}
        [csums.__setitem__(x.checksum, x)
         for x in results
         if x.checksum]
        content = {}
        paths = [x.getPath() for x in results]
        for result in results:
            item = self.get_item(result)
            item['checksum'] = result.checksum or None
            item['dupes'] = {}
            content[result.getPath()] = item
        return content

    def get_fields(self):
        fields = super(self.__class__, self).get_fields()
        fields['fields'].update({
                'checksum': {
                    'searchable': True,
                    'sort': True,
                    'visible': True,
                    'title': 'Checksum',
                    },
                'dupes': {
                    'searchable': True,
                    'sort': True,
                    'visible': True,
                    'title': 'Dupes',
                    },
                })
        fields['index'] += [
                'checksum',
                'dupes'
                ]

        return fields

    def get_buttons(self):
        buttons = super(self.__class__, self).get_buttons()
        buttons['reindex checksum'] = 'reindex_checksum_confirm:method'
        return buttons
