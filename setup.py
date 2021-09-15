import setuptools


with open('version') as f:
    version = f.read().strip()
with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name='youtube_api',
    version=version,
    author='Tim Niven',
    author_email='tim@doublethinklab.org',
    description="Simple wrapper around YouTube's API",
    url=f'https://github.com/doublethinklab/youtube-api.git#{version}',
    packages=setuptools.find_packages(),
    python_requires='>=3.9.5',
    install_requires=required)
