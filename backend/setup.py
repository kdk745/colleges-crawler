import platform

requirements = [
    # other dependencies
]

if platform.system() == "Windows":
    requirements.append('twisted-iocpsupport')

setup(
    # other setup parameters
    install_requires=requirements,
)
