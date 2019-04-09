from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='django-logger',
      version='0.1.0',  # version.feature.patch (rc)release-candidate 1
      url='https://github.com/NiranjanSingh/django-logger',
      license='MIT',
      author='Niranjan Singh',
      author_email='niranjan32331@gmail.com',
      description='Logging package to log formatted logs so that its readable via kibana.',
      dependency_links=['https://pypi.deploy.loansingh.com/', ],
      packages=find_packages('.', exclude='logger_test'),
      install_requires=[
          'Django>=1.8,<2',
          'arrow>=0.12.1',
          'pytz>=2017.3',
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)  # As there is only one package `django_logger` zipping it won't effect much.
