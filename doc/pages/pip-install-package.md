# pip-install-package

## airflow_shopify

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pip-install-package/airflow_shopify/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/pip-install-package/airflow_shopify/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## airflow_shopify

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pip-install-package/airflow_shopify/shopify/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/pip-install-package/airflow_shopify/shopify/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## airflow_shopify

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pip-install-package/airflow_shopify/shopify/collection/__init__.py) -->
<!-- The below code snippet is automatically added from ../../python/pip-install-package/airflow_shopify/shopify/collection/__init__.py -->
```py

```
<!-- MARKDOWN-AUTO-DOCS:END -->



## setup

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pip-install-package/setup.py) -->
<!-- The below code snippet is automatically added from ../../python/pip-install-package/setup.py -->
```py
from setuptools import setup

setup(
    name='shopify_collaboration',
    version='0.1.0',    
    description='shopify airflow utility',
    author='Cherkashyn Vitalii',
    packages=['airflow_shopify.shopify',
              'airflow_shopify.shopify.collection',
              'airflow_shopify.shopify.product',
              'airflow_shopify.storage'],
    install_requires=['requests', 'apache-airflow' ],
    classifiers=[
        'Development Status :: 2 - prototype',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


