from zope.interface import Interface as I

from plone.indexer.decorator import indexer

from bit.content.checksum.interfaces import IChecksummable, IChecksum


@indexer(I)
def getChecksum(obj):
    """Make sure we index icon relative to portal"""
    if IChecksummable.providedBy(obj):
        return IChecksum(obj).checksum
    return 0
