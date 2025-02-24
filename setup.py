import os
from pathlib import Path
from setuptools import setup, find_packages
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

device_capability = "90"  # NOTE: Pinned version for SM90

cwd = Path(os.path.dirname(os.path.abspath(__file__)))

cxx_flags = ["-O2", "-fopenmp", "-fPIC", "-Wno-strict-aliasing"]
nvcc_flags = ["-O2", "-std=c++17"]

if device_capability:
    nvcc_flags.extend([
        f"--generate-code=arch=compute_{device_capability},code=sm_{device_capability}",
        f"-DGROUPED_GEMM_DEVICE_CAPABILITY={device_capability}",
    ])

ext_modules = [
    CUDAExtension(
        "grouped_gemm_backend",
        ["csrc/ops.cu", "csrc/grouped_gemm.cu"],
        include_dirs = [
            f"{cwd}/third_party/cutlass/include/",
            f"{cwd}/csrc"
        ],
        extra_compile_args={
            "cxx": cxx_flags,
            "nvcc": nvcc_flags,
        }
    )
]

extra_deps = {}

extra_deps['dev'] = [
    'absl-py',
]

extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name="grouped_gemm",
    version="0.1.4",
    author="Trevor Gale",
    author_email="tgale@stanford.edu",
    description="Grouped GEMM",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tgale06/grouped_gemm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
    ],
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtension},
    extras_require=extra_deps,
)
