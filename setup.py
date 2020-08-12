import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_txt = os.path.join(here, 'cowechatapi/version.txt')
VERSION = open(version_txt, encoding='utf-8').read().strip()
# VERSION = "0.1.1"

REQUIRES = ['requests']

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cowechatapi',
    version=VERSION,
    author="Niko Zhang",
    author_email="334743423@qq.com",
    description="A tools for send message to company wechat.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="wechat cowechat",
    url="https://github.com/nikozhangwj/CoropWechatSendMsgAPI",
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'cowechat = cowechatapi.cowechat:main',
        ],
    },
)
