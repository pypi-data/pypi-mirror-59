.. Android Strings Lib documentation master file, created by
   sphinx-quickstart on Sat Feb 17 19:48:43 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Android Strings Lib's documentation!
===============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   androidstringslib
   parser


Android Strings Lib provides support for android's strings.xml files.  These
files are used to translate strings in android apps.

Android Strings Lib is built for python 3.  Patches for adding python 2 support
are welcome, but may break at any point as I don't intend to test it.


Quick Start Guide
-----------------

.. code-block:: python
   :linenos:

   import androidstringslib
   # The two arguments are the file with original strings (here, English)
   # and the file containing the translations (here, French).
   an = androidstringslib.android('app/src/main/res/values/strings.xml',
        'app/src/main/res/values-fr/strings.xml', 'fr')
   for entry in an:
           # Automatically translate 'Logcat' to itself
           if entry.orig == 'Logcat':
                   entry.dst = 'Logcat'
   # Save the result to the destination file
   # Note that this also updated the destination file to the newer origin
   # file.
   an.save()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
