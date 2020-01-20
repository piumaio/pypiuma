from setuptools import setup, find_packages

setup(
    name='pypiuma',
    version='1.0.2',
    url='',
    install_requires=[],
    description="Piuma Python library with Django support",
    long_description=open('README.rst', 'r').read(),
    license="MIT",
    author="Lotrèk",
    author_email="dimmitutto@lotrek.it",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
