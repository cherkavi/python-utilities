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
