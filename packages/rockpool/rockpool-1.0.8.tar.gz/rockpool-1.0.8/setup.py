from distutils.core import setup
import setuptools

# - Read version
exec(open("rockpool/version.py").read())

setup(
    name="rockpool",
    author="aiCTX AG",
    author_email="dylan.muir@aictx.ai",
    version=__version__,
    packages=setuptools.find_packages(),
    install_requires=["numba", "numpy", "scipy"],
    extras_require={
        "all": [
            "tqdm",
            "brian2",
            "pytest",
            "torch",
            "torchvision",
            "rpyc",
            "jax",
            "jaxlib",
            "sphinx",
            "nbsphinx",
            "sphinx-autobuild",
            "sphinx-rtd-theme",
            "m2r",
        ]
    },
    description="A Python package for developing, simulating and training spiking neural networks, and deploying on neuromorphic hardware",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    keywords="spiking neural network SNN neuromorphic",
    python_requires=">=3.6",
    project_urls={"Source": "https://gitlab.com/aiCTX/rockpool"},
)
