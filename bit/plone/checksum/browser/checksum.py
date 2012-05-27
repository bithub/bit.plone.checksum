import os

from zope.annotation.interfaces import IAnnotations

from Products.Five import BrowserView as FiveView


class ReindexChecksumView(FiveView):

    def get_content(self):
        return [(x, os.path.basename(x))
                for x in self.request.get('paths') or []]

    def reindex_checksum(self):
        content = self.request.get('content')
        if not content:
            return
        total = len(content)
        i = 1
        for path in content:
            try:
                obj = self.context.restrictedTraverse(path)
                obj.reindexObject(idxs=['checksum'])
                log.warn(
                    '(%s/%s) reindexing checksum for %s' % (i, total, path))
                print '(%s/%s) reindexing checksum for %s' % (i, total, path)
            except:
                log.error(
                    '(%s/%s) FAIL: reindexing checksum for %s'\
                        % (i, total, path))
            i += 1
