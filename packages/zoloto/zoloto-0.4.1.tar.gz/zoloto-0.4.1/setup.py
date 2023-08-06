from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="zoloto",
    version="0.4.1",
    url="https://github.com/RealOrangeOne/zoloto",
    author="Jake Howard",
    description="A fiducial marker system powered by OpenCV - Supports ArUco and April",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(include="zoloto*"),
    install_requires=[
        "opencv-contrib-python-headless>=4.0,<4.1",
        "cached-property>=1.5",
        "coordinates>=0.3.0",
        "fastcache>=1.1",
        "ujson>=1.35",
    ],
    entry_points={
        "console_scripts": [
            "zoloto-preview=zoloto.cli.preview:main",
            "zoloto-calibrate=zoloto.cli.calibrate:main",
        ]
    },
    python_requires=">=3.5",
    extras_require={"rpi": ["picamera[array]>=1.13"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development",
    ],
)
