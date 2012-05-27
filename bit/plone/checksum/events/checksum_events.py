from bit.content.checksum.interfaces import IChecksum


def updateChecksum(obj, evt):
    IChecksum(obj).update()
