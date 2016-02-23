#=============================================================================
#
# aptask Package Setup Script
#
#=============================================================================

"""
aptask Package Setup Script
===========================

Normal Installation
-------------------

    python setup.py install

Development Installation
------------------------

    python setup.py develop

Create Source Distribution
--------------------------

    python setup.py sdist

"""


from setuptools import setup


setup(
    name         = 'aptask',
    version      = '0.1.0',
    description  = 'Asynchronous Parallel Task Queue',
    url          = 'https://github.com/zhester/aptask',
    author       = 'Zac Hester',
    author_email = 'zac.hester@gmail.com',
    license      = 'BSD',
    packages     = [ 'aptask' ],
    scripts      = [ 'scripts/aptaskd.py', 'scripts/aptc.py' ],
    data_files   = [ ( 'config', 'conf/aptaskd.json' ) ],
    zip_safe     = False
)

