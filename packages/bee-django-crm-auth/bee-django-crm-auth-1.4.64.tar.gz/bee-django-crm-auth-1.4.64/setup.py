import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bee-django-crm-auth',
    version='1.4.64',
    packages=['bee_django_crm'],
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django app to conduct Web-based crm.',
    long_description=README,
    url='http://www.example.com/',
    author='zhangyue',
    author_email='zhangyue@zhenpuedu.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'bee_django_richtext>=0.0.3',
    ],
)
