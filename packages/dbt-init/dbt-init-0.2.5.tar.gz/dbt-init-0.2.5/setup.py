from setuptools import find_packages, setup
from setuptools.command.install import install
import os
import glob

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()


package_name = "dbt-init"
VERSION = "0.2.5"
description = """Create a dbt project the way Fishtown Analytics would"""


class VerifyVersionCommand(install):
    """
    Custom command to verify that the git tag matches our version
    https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
    """

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

starter_project_files = package_files('starter-project')

setup(
    name=package_name,
    version=VERSION,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Claire Carroll",
    author_email="claire@fishtownanalytics.com",
    url="https://github.com/fishtown-analyics/dbt-init",
    packages=find_packages(),
    package_data={
        '': starter_project_files
    },
    include_package_data=True,
    test_suite="test",
    entry_points={"console_scripts": ["dbt-init = core.main:main"]},
    scripts=[],
    install_requires=["jinja2"],
    cmdclass={"verify": VerifyVersionCommand},
)
