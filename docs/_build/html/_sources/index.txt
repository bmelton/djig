Djig
====

Djig is a minimalist, Digg-like news aggregator (old Digg, not new) for letting
users submit content.  Currently in a fairly alphaish state, not recommended
for use. 

Djig includes a search_indexes.py file and a couple of example search templates 
for use with Django-Haystack.  Haystack is not a requirement, and lack of its
presence should not cause any harm, but may be used if search is needed. You 
will need to at least update_index after installing Djig.  

Installation
============

::

   pip install djig


Configuration
=============

Add ``djig`` to ``INSTALLED_APPS``

::

   INSTALLED_APPS = {
       [...],
       'djig',
   }

Add ``djig.urls`` to your root ``urls.py``.  I have mine as 'news', like this:

::

   url('^news/', include('djig.urls', namespace='news')),



.. toctree::
   :maxdepth: 2

   intro


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

