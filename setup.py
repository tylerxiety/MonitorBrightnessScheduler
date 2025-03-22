#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="monitor_brightness_scheduler",
    version="0.1.0",
    description="Automatically adjust external monitor brightness based on time",
    author="User",
    packages=find_packages(),
    scripts=["monitor_brightness_control.py"],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "monitor-brightness=monitor_brightness_control:main",
        ],
    },
) 