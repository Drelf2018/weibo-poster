from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setup(
    name="weibo-poster",
    version="0.0.5",
    license="MIT",
    author="Drelf2018",
    author_email="drelf2018@outlook.com",
    description="对应 weibo-webhook 的提交器",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requires.splitlines(),
    keywords=['python', 'weibo', 'webhook'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        "": ["requirements.txt"]
    },
    url="https://github.com/Drelf2018/weibo-poster",
    python_requires=">=3.8",
)