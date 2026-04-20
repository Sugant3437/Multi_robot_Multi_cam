from setuptools import setup

package_name = 'amr_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sugant',
    description='AMR Navigation',
    entry_points={
        'console_scripts': [
            'apriltag_node = amr_nav.apriltag_node:main',
            'pose_bridge = amr_nav.pose_bridge_node:main',
        ],
    },
)