from setuptools import setup

# Docs: https://setuptools.readthedocs.io/en/latest/userguide/keywords.html
setup(
    name='decorators',
    version='0.1.0',
    description='Python library with common and useful decorator functions.',
    url='https://gitlab.com/Patesz/decorators',
    author='Ricky',
    author_email='p.ricky.dev@gmail.com',
    py_modules=['asynchronous', 'convert', 'core', 'log', 'reader', 'timer', 'test'],
    install_requires=[
        'pandas', 'APScheduler'
    ],
    packages=[
        'decorators'
    ],
    package_dir={'decorators': 'src'},
    license='MIT',
    test_suite='test'
)
