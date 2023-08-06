
==========
KubeDR CLI
==========

``kubedrctl`` is a command line tool to exercise some functionality of
the `KubeDR`_ project.

Installation
============

Here is one way of installing using a virtual environment:
::

    # Create a virtual environment
    $ python3 -m venv $HOME/venv/kubedrctl

    # Install the library
    $ $HOME/venv/kubedrctl/bin/pip install kubedrctl

    $ export PATH=$PATH:$HOME/venv/kubedrctl/bin

Usage
=====

Listing Backups
---------------

.. code-block:: bash

  $ kubedrctl list backups --accesskey <ACCESSKEY> \
        --secretkey <SECRETKEY> --repopwd <REPO_PASSWORD> \
        --endpoint <S3-ENDPOINT> --bucket <BUCKET>

Restoring from backups
----------------------

.. code-block:: bash

  $ kubedrctl restore --accesskey <ACCESSKEY> \
        --secretkey <SECRETKEY> --repopwd <REPO_PASSWORD> \
        --endpoint <S3-ENDPOINT> --bucket <BUCKET> \
        --targetdir <RESTORE_TARGET_DIR> <SNAPSHOT-ID>


.. _KubeDR: https://github.com/catalogicsoftware/kubedr
