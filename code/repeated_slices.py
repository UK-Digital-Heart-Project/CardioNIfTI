import dicom
import os
import shutil

cur_path = os.getcwd()

cur_dir =  os.path.join(cur_path,"data")
os.chdir(cur_dir)

patient_folders = os.listdir(cur_dir)

for patient in patient_folders:
          try:
                    p_dict = {}
                    slice_folders = sorted(os.listdir(os.path.join(cur_dir,patient)))
                    for slice_no in slice_folders:
                              os.chdir(os.path.join(cur_dir,patient,slice_no))
                              dicoms = os.listdir(os.path.join(cur_dir,patient,slice_no))
                              ds = dicom.read_file(dicoms[0])
                              slice_location = int(ds.SliceLocation)
                              try:
                                        p_dict[slice_location].append(slice_no)
                              except:
                                        p_dict[slice_location] = [slice_no]

                    for slice_location, slice_no in p_dict.items():
                              if len(slice_no) != 1:
                                        if len(slice_no) ==2:
                                                  repeated_slices = sorted(slice_no)
                                                  patient_dir = os.path.join(cur_dir,patient)
                                                  os.chdir(patient_dir)
                                                  shutil.rmtree(os.path.join(patient_dir,repeated_slices[0]))
                                                  os.rename((os.path.join(patient_dir,repeated_slices[1])),(os.path.join(patient_dir,repeated_slices[0])))
                                        else:
                                                  print (patient," has more than two repeated slices" ,slice_no)
          except:
                    pass
