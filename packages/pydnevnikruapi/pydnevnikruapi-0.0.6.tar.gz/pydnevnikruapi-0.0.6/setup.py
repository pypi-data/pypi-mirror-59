from setuptools import setup, find_packages
import pydnevnikruapi


setup(
    name="pydnevnikruapi",
    version=pydnevnikruapi.__version__,
    url="https://github.com/kesha1225/DnevnikRuAPI",
    author="kesha1225",
    packages=find_packages(),
    description="simple wrapper for dnevnik.ru API",
    install_requires=["requests", "aiohttp"],
    long_description="https://kesha1225.github.io/DnevnikRuAPI/"
)
