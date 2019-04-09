from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='easy-django-logger',
      version='0.1.1',  # version.feature.patch (rc)release-candidate 1
      url='https://github.com/NiranjanSingh/django-logger',
      license='MIT',
      author='Niranjan Singh',
      author_email='niranjan32331@gmail.com',
      description='Django logger to log formatted logs parsable via elastic search and visualize via kibana.',
      packages=find_packages('.', exclude='logger_test'),
      install_requires=[
          'Django>=1.8,<2',
          'arrow>=0.12.1',
          'pytz>=2017.3',
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)  # As there is only one package `django_logger` zipping it won't effect much.
