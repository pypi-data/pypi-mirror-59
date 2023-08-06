import setuptools
#import versioneer
new_version='0.1.5'

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['matplotlib','numpy','pandas'],
     python_requires='>=3',
     name='imagesc',
     version=new_version,
#     version=versioneer.get_version(),    # VERSION CONTROL
#     cmdclass=versioneer.get_cmdclass(),  # VERSION CONTROL
     author="Erdogan Taskesen",
     author_email="erdogant@gmail.com",
     description="imagesc is an python package to create heatmaps using multiple methods.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/erdogant/imagesc",
	 download_url = 'https://github.com/erdogant/imagesc/archive/'+new_version+'.tar.gz',
     packages=setuptools.find_packages(), # Searches throughout all dirs for files to include
     include_package_data=True, # Must be true to include files depicted in MANIFEST.in
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
