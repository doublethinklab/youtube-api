import setuptools


def fix_requirement(x):
    if x.startswith('git+ssh'):
        package = x.split('.git')[0].split('/')[-1]
        return f'{package} @ {x}'
    else:
        return x


with open('version') as f:
    version = f.read().strip()
with open('requirements.txt') as f:
    required = f.read().splitlines()
    required = [fix_requirement(x) for x in required]


setuptools.setup(
    name='youtube_api',
    version=version,
    author='Tim Niven',
    author_email='tim@doublethinklab.org',
    description='Reusable module for accessing the YouTube API.',
    url=f'https://github.com/doublethinklab/youtube-api.git#{version}',
    packages=setuptools.find_packages(),
    python_requires='>=3.9.5',
    install_requires=required)
