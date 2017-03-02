epm
===

:code:`epm` is Ergonomica's package manager.

Installation
------------

Download `epm.py` from this repository and place it in `~/.ergo/packages`.

Usage
-----

Installing Packages
~~~~~~~~~~~~~~~~~~~

To install package :code:`package` from the Ergonomica central repository, just do

.. code::

   epm install package

To remove this package, simply run

.. code::

    epm remove package

To list all installed packages, run

.. code::

   epm list

Note that this lists all packages in :code:`~/.ergo/packages`; not just those installed through epm.

Security
--------

All packages are installed in :code:`~/.ergo/packages` (not any /usr directory). Additionally, all packages must be approved by the Ergonomica github organization.
