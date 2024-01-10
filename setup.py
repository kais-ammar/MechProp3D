from setuptools import setup, find_packages
from MechProp3D import __version__, __author__, __contact__, __name__
setup(
    name = __name__,
    version = __version__,
    author=__author__,
    author_email = __contact__,
    description='3D visualization of elastic properties',
    long_description='',
    license='',
    url="",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Beta',
        'Natural Language :: English',        
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
    python_requires='>=3.7',
    install_requires=['PyQt5'],
    packages=find_packages(),
    scripts=[],
    data_files=[('MechProp3D/icons/', ["MechProp3D/icons/3D_parameter.png", "MechProp3D/icons/comp.png", "MechProp3D/icons/nu.png",
                                       "MechProp3D/icons/slice.png","MechProp3D/icons/background_icon.ico","MechProp3D/icons/E.png",
                                       "MechProp3D/icons/settings-solid.svg","MechProp3D/icons/take_screen.ico","MechProp3D/icons/close.ico",
                                       "MechProp3D/icons/iso.ico","MechProp3D/icons/shear.png" ,"MechProp3D/icons/vtk.svg"])],    
    entry_points={
        'gui_scripts': ['MechProp3D = MechProp3D.MechProp3D:main'],
    },
)
