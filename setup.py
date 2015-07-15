from setuptools import setup, find_packages


setup(
    name='simphony_network',
    version='0.1',
    author='SimPhoNy FP7 European Project',
    description='SimPhoNy network layer',
    packages=find_packages(),
    install_requires=['simphony',
                      'gevent>=1.0',
                      'pyzmq>=13.1.0',
                      'msgpack-python>=0.4.6',
                      'msgpack-numpy>=0.3.6',
                      'zerorpc>=0.5.1',
                      'fabric>=1.10.2',
                      'blinker>=1.3'],
    dependency_links = ['git+https://github.com/simphony/simphony-common.git#egg=simphony'],
    entry_points = {
        'console_scripts': [
            'simphony = simphony_network.server:run_server',
             ],
        'simphony.engine': [
            'proxy = simphony_network.proxy'
             ],
        },
)
