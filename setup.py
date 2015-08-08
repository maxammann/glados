from setuptools import setup, find_packages

setup(
    name='glados',
    version='0.1',
    packages=find_packages(),
    url='',
    license='',
    author='max',
    author_email='',
    description='',
    install_requires=['PyAudio',
                      'pyjulius',
                      'gTTS',
                      'pyvona',
                      'protobuf',
                      'langdetect',
                      'python-mpd2'],
    scripts=['scripts/glados-run'],
    include_package_data=True,
)
