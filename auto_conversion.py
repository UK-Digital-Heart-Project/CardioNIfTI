# Author: Georgia Doumou (g.doumou@lms.mrc.ac.uk)
# Date: 03/08/2018

import os
from os import rename
import shutil
import numpy as np
import nibabel as nib
import dicom
import csv
import operator
import convert_utils as convert
import glob

# Set current working directory
#cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = os.getcwd()

# Set paths
dcm2nii_dir =os.path.join(cur_path,"dcm2niix")
cardiac_phase_dir = "cardiacphasedetection"
cur_dir = os.path.join(cur_path,"data")


## Work on the 'data' directory
os.chdir(cur_dir)
patient_folders = sorted(os.listdir(cur_dir))

for patient in patient_folders:
          patient_path = os.path.join(cur_dir,patient)
          os.chdir(patient_path)
          subfolders = sorted(os.listdir(patient_path))
          subfolders_count = len(subfolders)
          if subfolders_count!=0:
                    if subfolders_count == 1:
                              sub = sorted(os.listdir(os.path.join(patient_path,subfolders[0])))
                              sub_count = len(sub)
                              os.chdir(os.path.join(patient_path,subfolders[0]))
                              if sub_count>20:
                                        ds1 = dicom.read_file(sub[0])
                                        try:
                                                  sl1 = ds1.SliceLocation
                                        except:
                                                  sl1 = ds1[0x20, 0x1041].value

                                        ds2 = dicom.read_file(sub[1])
                                        try:
                                                  sl2 = ds2.SliceLocation
                                        except:
                                                  ds1[0x20, 0x1041].value
                                                  
                                        if sl1 == sl2:
                                                  try:
                                                            phasenum = int(convert.loadonefolder(os.path.join(patient_path,subfolders[0])))
                                                            convert.all_in_one_folder_sorted(os.path.join(patient_path,subfolders[0]), phasenum)
                                                            convert.multiple_folders_2(patient,os.path.join(patient_path,subfolders[0]))
                                                            convert.cardiac_phase_detection("LVSA.nii.gz")

                                                  except:
                                                            convert.all_in_one_folder(patient_path,os.path.join(patient_path,subfolders[0]))
                                                            lvsa = "LVSA.nii.gz"
                                                            if os.path.exists(os.path.join(patient_path,lvsa)):
                                                                      convert.cardiac_phase_detection("LVSA.nii.gz")
                                                            
                                                  else:
                                                            pass
                                        else:
                                                  convert.all_in_one_folder(patient_path,os.path.join(patient_path,subfolders[0]))
                                                  lvsa = "LVSA.nii.gz"
                                                  if os.path.exists(os.path.join(patient_path,lvsa)):
                                                            convert.cardiac_phase_detection("LVSA.nii.gz")
                                                  
                              else:
                                        convert.multiple_folders_2(patient,os.path.join(patient_path,subfolders[0]))
                                        convert.cardiac_phase_detection("LVSA.nii.gz")
                                        
                    elif subfolders_count > 20:
                              sub = sorted(os.listdir(patient_path))
                              sub_count = len(sub)
                              os.chdir(os.path.join(patient_path))
                              ds1 = dicom.read_file(sub[0])
                              try:
                                        sl1 = ds1.SliceLocation
                              except:
                                        sl1 = ds1[0x20, 0x1041].value

                              ds2 = dicom.read_file(sub[1])
                              try:
                                        sl2 = ds2.SliceLocation
                              except:
                                        ds1[0x20, 0x1041].value
                                        
                              if sl1 == sl2:
                                        try:
                                                  phasenum = int(convert.loadonefolder(subfolders))
                                                  convert.all_in_one_folder_sorted(patient_path, phasenum)
                                                  convert.multiple_folders_2(patient,patient_path)
                                                  convert.cardiac_phase_detection("LVSA.nii.gz")
                                                  
                                        except:
                                                  convert.all_in_one_folder(patient_path,os.path.join(patient_path))
                                                  lvsa = "LVSA.nii.gz"
                                                  if os.path.exists(os.path.join(patient_path,lvsa)):
                                                            convert.cardiac_phase_detection("LVSA.nii.gz")

                                        else:
                                                  pass
                              else:
                                        convert.all_in_one_folder(patient_path)
                                        lvsa = "LVSA.nii.gz"
                                        if os.path.exists(os.path.join(patient_path,lvsa)):
                                                  convert.cardiac_phase_detection("LVSA.nii.gz")
                    else:
                              try:
                                        convert.multiple_folders_2(patient,patient_path)
                                        convert.cardiac_phase_detection("LVSA.nii.gz")

                              except:
                                        pass
          else:
                    pass
                    print(patient +" is empty")

                    
          os.chdir(patient_path)
          if os.path.exists(os.path.join(patient_path,"LVSA_img_ED.nii.gz")) is False:
                    convert.cardiac_phase_detection("LVSA.nii.gz")
          else:
              pass
