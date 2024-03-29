# README

[![DOI](https://zenodo.org/badge/175637825.svg)](https://zenodo.org/badge/latestdoi/175637825)

## CardioNIfTI ![](https://img.shields.io/badge/beta-version-blue.svg)

Software tools for preprocessing of cardiac MR DICOM datasets and conversion to NIfTI prior to segmentation. You should make a copy of your original data before running this tool.

![](.gitbook/assets/imagej_cine.gif)

## Overview

The files in this repository are organised as follows:

[Code](https://github.com/UK-Digital-Heart-Project/CardioNIfTI/tree/0bf3dc7c91fbf8fc6894263a6000ed8f965a6bfd/code/README.md): 1\) `repeated_slices.py` \(optional\) – it identifies repeated cine slices, finds the latest repeat and deletes older versions. 2\) `auto_conversion.py` – converts multi and single frame dicoms into one NIfTI \(`LVSA.nii.gz`\). It also identifies the end-diastolic and end-systolic frames in this cine and saves these as separate files \(`LVSA_img_ED.nii.g` and `LVSA_img_ES.nii.gz`\). 3\) `LVSA_structure.py` \(optional\) – creates a new folder - `LVSA` – which contains copies of the 3 new NIfTI files.

[Data](https://github.com/UK-Digital-Heart-Project/CardioNIfTI/tree/0bf3dc7c91fbf8fc6894263a6000ed8f965a6bfd/data/README.md):

Contains sample DICOM datasets on which the functions of the code can be run. `LVSA_1` is a Philips sequence with consecutive DICOM files, while `LVSA_2` is a Siemens sequence with each slice in separate folders.

To run the [code](https://github.com/UK-Digital-Heart-Project/CardioNIfTI/tree/0bf3dc7c91fbf8fc6894263a6000ed8f965a6bfd/code/README.md) we provide a [Docker](https://www.docker.com) image with all the necessary dependencies pre-compiled.

### Installation/Usage Guide for Docker Image

A Docker image is available on dockerhub [https://hub.docker.com/r/gdoumou/auto\_conversion](https://hub.docker.com/r/gdoumou/auto_conversion). This image contains a base Ubuntu linux operating system image set up with all the libraries required to run the code.

#### Download the repo

Click the Code button, and then unzip the file to your desktop etc. In `...CardioNIfTI/data` unzip the two folders containing sample DICOM stacks.

#### Install Docker

For Windows 10 Pro first install [Docker](https://www.docker.com/docker-windows). Windows 10 Home users will require [Docker toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/).

Ensure you have the C drive selected as a [shared drive](https://docs.docker.com/docker-for-windows/) in Docker settings \(or in VirtualBox on W10 Home\).

To visualise the images download [ImageJ](https://imagej.nih.gov/) or equivalent.

#### Download Docker image

In W10 open PowerShell from the Windows search box \(Win + X then I\), in macOS navigate Finder &gt; Applications &gt; Utilities &gt; Terminal, or in Linux any terminal can be used. Then download the pre-compiled image:

```text
  docker pull gdoumou/auto_conversion:latest
```

Check the image is there

```text
  docker images
```

should show auto\_conversion on the list of images on your local system.

#### Run the Docker image

Note the path to the data folder \(containing the DICOM files\) on your desktop eg `/c/Users/Desktop/CardioNIfTI/data` and substitute `<folder-path>` within this command:

```text
docker run -it --rm -v <folder-path>:/code/data gdoumou/auto_conversion
```

At the root prompt enter:

```text
export LD_LIBRARY_PATH=/lib64
```

Navigate to /code/data and check that it has mounted your DICOM folders \(eg `LVSA_1` and `LVSA_2`\):

```text
cd data
ls
```

Then return to /code:

```text
cd ..
```

#### Run the python scripts

1\) `repeated_slices.py` \(optional\) 2\) `auto_conversion.py` 3\) `LVSA_structure.py` \(optional\)

example:

```text
python auto_conversion.py
```

when you finish type:

```text
exit
```

#### Outputs from the pipeline

Once the pipeline is finished, under the root directory of each subject, you have three NIfTI files, i.e., `LVSA.nii.gz`, `LVSA_img_ED.nii.gz` and `LVSA_img_ES.nii.gz` which can be visualised in ImageJ.

#### Acknowledgements

This code was developed by Georgia Doumou with help from Wenjia Bai and Jinming Duan - Imperial College London. Dependencies - [dcm2niix](https://github.com/rordenlab/dcm2niix)

