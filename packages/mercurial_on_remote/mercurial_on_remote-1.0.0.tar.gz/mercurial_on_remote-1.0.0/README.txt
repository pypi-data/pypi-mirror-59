.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

====================================
Mercurial OnRemote extension
====================================

Execute some Mercurial command on remote repository (ssh/local repositories only).

.. contents::
   :local:
   :depth: 2

.. sectnum::

Example
=====================

My two main use cases:

- update remote directory after pushing::

    hg push staging
    hg onremote staging update -r tip 

- check status and possibly commit in remote directory::

    hg onremote rhdevel status
    hg onremote rhdevel commit -m 'Forgotten typo'

In those examples ``staging`` and ``rhdevel`` are remote paths, mapped
to urls like ``ssh://some.machine.net/repos/myrepo`` (local paths work
too). 

Explicit path works too, but is much less handy::

    hg onremote ssh://euler.mydev.net/repos/myrepo   status

Arguments
======================

General command syntax::

    hg onremote «remote» «command» «arguments»

where ``«remote»`` is remote repository alias or path, and remaining arguments
constitute normal mercurial command.

Option ``--ssh`` can be used just like with push or pull::
 
    hg onremote --ssh /custom/ssh staging status


How does it work
=================================================

The extension simply resolves the specified path, and:

- if it maps to local directory, executes ``hg --cwd that/directory «command» «arguments»``

- if it maps to ssh path, executes ``ssh that/machine hg --cwd that/directory «command» «arguments»``

- elsewhere (``http`` or other remote) it refuses to work.

There is nothing particularly magical, the extension is intended to
save some keystrokes and avoid flow interruption (I wrote it mainly
to stop writing various *push and update* shell scripts).

.. caution::

   You need true ssh access to have it working. Remote repositories,
   from ``bitbucket`` to ``mercurial-server`` installations will usually
   reject attempts to run commands (as one could expect).


Configuration
=================================================

There is currently no dedicated configuration. 

Standard mercurial settings are used to decide how to call
``ssh`` and which remote command to call to spawn Mercurial (see
``ssh`` and ``remotecmd`` settings in ``[ui]`` section). 
This way ``onremote`` uses the same ``ssh`` command
which is used by ``hg push`` and ``hg pull``, and the same
mercurial name.


Problems and limitations
=================================================

Interactive commands may fail to work properly due to lack
of fully working console. 
I recommend avoiding commands which trigger interactive prompts
or editor spawns. If you try ``hg onremote commit`` add ``-m "Some message"``.

.. note::

   At the moment OnRemote doesn't initialize full terminal support
   (technically, doesn't add ``ssh -t`` or similar). It may
   change in the future.

Installation
=================================================

Mercurial ≥ 3.4 is required (attempts to run on older version will
result in crashes) and Mercurial ≥ 4.5 is strongly recommended
(versions 3.4-4.4 involve some hacks which may fail for more
complicated arguments).

Linux/Unix (from PyPI)
~~~~~~~~~~~~~~~~~~~~~~

If you have working ``pip`` or ``easy_install``::

    pip install --user mercurial_on_remote

or maybe::

    sudo pip install mercurial_on_remote

(or use ``easy_install`` instead of ``pip``). Then activate by::

    [extensions]
    mercurial_on_remote =

To upgrade, repeat the same command with ``--upgrade`` option, for
example::

    pip install --user --upgrade mercurial_on_remote

Linux/Unix (from source)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't have ``pip``, or wish to follow development more closely:

- clone both this repository and `mercurial_extension_utils`_ and put
  them in the same directory, for example::

    cd ~/sources
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-on_remote/

- update to newest tags,

- activate by::

    [extensions]
    mercurial_on_remote = ~/sources/mercurial-on_remote/mercurial_on_remote.py

To upgrade, pull and update.

See `mercurial_extension_utils`_ for longer description of this kind
of installation.

Windows
~~~~~~~~~~~~~~~~~~~~~~~

If you have any Python installed, you may install with ``pip``::

    pip install mercurial_on_remote

Still, as Mercurial (whether taken from TortoiseHg_, or own package)
uses it's own bundled Python, you must activate by specifying the path::

    [extensions]
    mercurial_on_remote = C:/Python27/Lib/site-packages/mercurial_on_remote.py
    ;; Or wherever pip installed it

To upgrade to new version::

    pip --upgrade mercurial_on_remote

If you don't have any Python, clone repositories::

    cd c:\hgplugins
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-on_remote/

update to tagged versions and activate by path::

    [extensions]
    mercurial_on_remote = C:/hgplugins/mercurial-on_remote/mercurial_on_remote.py
    ;; Or wherever you cloned

See `mercurial_extension_utils`_ documentation for more details on
Windows installation. 



Related extensions
==================================================

There are a few extensions which support operations on repository
groups - `Subrepos Extension`_, `OnSub Extension`_, `Forest
Extension`_. They all require using parent repository, which defines
the project structure. So, to pull all repos below ``~/src`` you
must ``hg init src``, create file like ``.hgsub`` there, etc.

All Dirs does not require such a parent repo. It just works on
whatever is found on the disk. You decided to keep some repositories
below ``~/src``? Fine, you can ``hg alld status`` them all.

Command syntax also matters. I strongly prefer typing::

     hg alld pull --update

to typing::

     hg onsub "hg pull --update"

At the same time, All Dirs does not support any kind of declaration
that some repositories are related, group cloning, version
relationship etc. If you are interested in such features, consider
`Subrepos Extension`_.

History
==================================================

See `HISTORY.txt`_

Development, bug reports, enhancement suggestions
===================================================

Development is tracked on BitBucket, see 
http://bitbucket.org/Mekk/mercurial-on_remote/

Use BitBucket issue tracker for bug reports and enhancement
suggestions.

Additional notes
================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/AllDirsExtension

Check also `other Mercurial extensions I wrote`_.

.. _other Mercurial extensions I wrote: http://mekk.bitbucket.io/mercurial.html

.. _Mercurial: http://mercurial.selenic.com
.. _HISTORY.txt: http://bitbucket.org/Mekk/mercurial-all-dirs/src/tip/HISTORY.txt
.. _mercurial_extension_utils: https://bitbucket.org/Mekk/mercurial-extension_utils/
.. _dynamic_username: http://bitbucket.org/Mekk/mercurial-dynamic_username/

.. _TortoiseHg: http://tortoisehg.bitbucket.org/

.. _OnSub Extension: https://www.mercurial-scm.org/wiki/OnsubExtension
.. _Subrepos Extension: https://www.mercurial-scm.org/wiki/Subrepository
.. _Forest Extension: https://www.mercurial-scm.org/wiki/ForestExtension

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mercurial-on_remote/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mercurial-on_remote/latest
     :align: middle
