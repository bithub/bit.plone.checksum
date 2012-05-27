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
        for res in results:
            if not res.checksum:
                continue
            if not res.checksum in csums:
                csums[res.checksum] = []
            csums[res.checksum].append(res)
        content = {}
        for result in results:
            item = self.get_item(result)
            item['checksum'] = result.checksum or None
            item['dupes'] = []
            if result.checksum and len(csums[result.checksum]) > 1:
                for dupe in csums[result.checksum]:
                    if not dupe == result:
                        item['dupes'].append(dupe.getURL())                    
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
                    'type': 'list',
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
