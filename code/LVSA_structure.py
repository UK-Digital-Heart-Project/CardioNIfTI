import os
import shutil
import convert_utils as convert

# Change paths accordingly.

cur_path = os.getcwd()

cur_dir =  os.path.join(cur_path,"data")
cardiac_phase_dir = "cardiacphasedetection"
patient_folders = sorted(os.listdir(cur_dir))
os.chdir(cur_dir)

for patient in patient_folders:
          patient_dir = os.path.join(cur_dir,patient)
          os.chdir(patient_dir)
          patient_content = os.listdir(patient_dir)
          lvsa_dir = os.path.join(cur_dir,patient,"LVSA")
          if os.path.exists(lvsa_dir) is False:
                    os.mkdir(lvsa_dir)
          if "LVSA.nii.gz" in patient_content:
                    shutil.copy((os.path.join(patient_dir, "LVSA.nii.gz")), (os.path.join(lvsa_dir)))
          else:
                    print("LVSA.nii.gz ", patient)
                    pass
          
          if "LVSA_img_ED.nii.gz" in patient_content:
              try:
                  shutil.copy((os.path.join(patient_dir, "LVSA_img_ED.nii.gz")), (os.path.join(lvsa_dir)))
              except:
                    convert.cardiac_phase_detection("LVSA.nii.gz")
                    shutil.copy((os.path.join(patient_dir, "LVSA_img_ED.nii.gz")), (os.path.join(lvsa_dir)))
                    print("LVSA_img_ED.nii.gz ", patient)
              else:
                  pass
          
          if "LVSA_img_ES.nii.gz" in patient_content:
              try:
                  shutil.copy((os.path.join(patient_dir, "LVSA_img_ES.nii.gz")), (os.path.join(lvsa_dir)))
              except:
                  print("LVSA_img_ES.nii.gz ", patient)
              else:
                  pass
