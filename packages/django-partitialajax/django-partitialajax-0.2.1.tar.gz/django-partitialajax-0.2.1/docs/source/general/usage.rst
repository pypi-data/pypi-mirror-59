===========
How to use
===========


two ways of use
 * use mix of templatetag and automatic js
 * use manual js only

================================
Template Tag (with automated js)
================================

Different Template Tags:
 * Direct Partitial
 * Lazy Partitial

Direct Partitial Recives content direct on Initial main page load
Lazy Partitial Requests its own content only by trigger

Both Partititals have the following Features:
 * Define Reload Button
 * Define


==========
Js Manual
==========


Initialize PartitialAjax Object.
This object recives one option dict

.. code-block:: js
   :linenos:

   // PartitialAjax(<options>)

The options dict:
   url: "",
   element: "",
   onlyChildReplace: true,
   interval: 5000,
   allowedElements: "all",
   textEventCallback: "console.info",
   restrictRemoteConfiguration: true,
   configFromElement: true

Options
#######

url
***
Remote Partitial URL
**default**: Current URL