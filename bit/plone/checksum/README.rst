==================
bit.plone.checksum
==================

Let's log in

  >>> from plone.app.testing import login, setRoles
  >>> from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
  >>> setRoles(layer['portal'], TEST_USER_ID, ['Member', 'Manager'])
  >>> login(layer['portal'], TEST_USER_NAME)

Lets add a folder

  >>> content_folder = layer['portal'][layer['portal'].invokeFactory('Folder', 'content')]

The folder is not checksummable

  >>> from bit.content.checksum.interfaces import IChecksummable
  >>> IChecksummable.providedBy(content_folder)
  False


Image checksum
--------------

Lets add an image to the folder

  >>> test_image = content_folder[content_folder.invokeFactory('Image', 'test_image')]

The image is checksummable

  >>> IChecksummable.providedBy(test_image)
  True

Lets get the checksum for the test_image

  >>> from bit.content.checksum.interfaces import IChecksum
  >>> checker = IChecksum(test_image)
  >>> csum = checker.checksum

And check it is empty

  >>> import hashlib
  >>> hashed = hashlib.md5()
  >>> hashed.update('')
  >>> hashed.hexdigest() == csum
  True


Now lets add an image

  >>> import os
  >>> TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')
  >>> test_image.setImage(open('%s/test.png' % TEST_DIR, 'r'))

The checksum hasnt been updated

  >>> IChecksum(test_image).checksum == csum
  True

But the checksum no longer verifies

  >>> IChecksum(test_image).verify()
  False

So lets update it, this returns the new checksum
  
  >>> new_csum = IChecksum(test_image).update()

And now the checksum verifies

  >>> IChecksum(test_image).verify()
  True

And returns the correct checksum

  >>> IChecksum(test_image).checksum == new_csum
  True

And this is the same as directly checksumming the file

  >>> m = hashlib.md5()
  >>> m.update(open('%s/test.png' % TEST_DIR, 'r').read())
  >>> m.hexdigest() == new_csum
  True

Lets create another image, and this time initialize

  >>> test_image2 = content_folder[content_folder.invokeFactory('Image', 'test_image2')]
  >>> initial_csum = IChecksum(test_image2).checksum
  >>> test_image2.setImage(open('%s/test.png' % TEST_DIR, 'r'))
  >>> import zope.event
  >>> from Products.Archetypes.event import ObjectInitializedEvent
  >>> zope.event.notify(ObjectInitializedEvent(test_image2))

The checksum is automatically updated when the image was initialized

  >>> IChecksum(test_image2).verify()
  True

  >>> IChecksum(test_image2).checksum == initial_csum
  False

We can compare that the objects are the same

  >>> IChecksum(test_image).compare(test_image2)
  True
  >>> IChecksum(test_image).checksum == IChecksum(test_image2).checksum
  True

Lets change the image

  >>> test_image2.setImage(open('%s/test-2.png' % TEST_DIR, 'r'))

The checksum no longer verifies

  >>> IChecksum(test_image2).verify()
  False

And appears to still equal the other object

  >>> IChecksum(test_image2).compare(test_image)
  True

So lets notify that the object has changed

  >>> from zope.lifecycleevent import ObjectModifiedEvent
  >>> zope.event.notify(ObjectModifiedEvent(test_image2))

And now the checksum should verify and comparison should work correctly

  >>> IChecksum(test_image2).verify()
  True
  >>> IChecksum(test_image2).compare(test_image)
  False

We can get the checksum from the catalog record

  >>> test_image2.reindexObject()
  >>> from Products.CMFCore.utils import getToolByName
  >>> portal_catalog = getToolByName(test_image2, 'portal_catalog')
  >>> result = portal_catalog.searchResults(
  ...        path='/'.join(test_image2.getPhysicalPath()))[0]
  >>> result.checksum == IChecksum(test_image2).checksum
  True
