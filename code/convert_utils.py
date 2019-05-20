# Author: Georgia Doumou (g.doumou@lms.mrc.ac.uk)
# Co-author: Wenjia Bai (w.bai@imperial.ac.uk); Su Boyang (su.boyang@nhcs.com.sg)
# Date: 03/08/2018
import os
from os import rename
import dicom
import glob
import shutil
import operator
import numpy as np
import nibabel as nib

# Set current working directory
cur_path = os.getcwd()

# Set paths for executables
dcm2nii_dir =os.path.join(cur_path,"dcm2niix")
#cardiac_phase_dir = os.path.join(cur_path,"cardiacphasedetection")
cardiac_phase_dir = "cardiacphasedetection"

def loadonefolder(subfolders_path):
    filenamelist = []
    os.chdir(subfolders_path)
    subfolders = sorted(glob.glob("*.dcm"))
    for dcm in subfolders:
                ds = dicom.read_file(dcm)
                tt = ds[0x18, 0x1060].value
                slice_loc = ds[0x20, 0x1041].value
                rt = ds[0x8, 0x13].value
                filenamelist.append([dcm, tt, slice_loc, rt])
    sortedmatrix = sorted(filenamelist, key=operator.itemgetter(2,1))
    slicelist = set([row[2] for row in sortedmatrix])
    phasenum = len(sortedmatrix) / len(slicelist)
    slicenum = len(slicelist)

    return phasenum

def cardiac_phase_detection(file):
    command = cardiac_phase_dir + " " + file + " LVSA_img_ED.nii.gz LVSA_img_ES.nii.gz"
    os.system(command)

def all_in_one_folder(patient_path,dcm_path):
    # Execute the dcm2niix file
    command = dcm2nii_dir + " -b n -p n -f LVSA -z y -o " + patient_path + " " + dcm_path
    os.system(command)

def all_in_one_folder_sorted(path,phasenum):
    cur_dir = path
    os.chdir(cur_dir)
    dicoms = sorted(glob.glob("*.dcm"))
    dicoms_number = len(dicoms)
    ### Change number of phases accordingly
    number_of_phases = phasenum
    slice_no = int(dicoms_number/number_of_phases)
    slices =sorted(list(range(1,slice_no+1)))

    for i in slices:
             if i in sorted(range(1,10)):
                 slice_filename = "slice_0" + str(i)
                 dest_dir = os.path.join(cur_dir,slice_filename)
                 if os.path.exists(dest_dir) is False:
                           os.mkdir(dest_dir)
             else:
                slice_filename = "slice_" + str(i)
                dest_dir = os.path.join(cur_dir,slice_filename)
                if os.path.exists(dest_dir) is False:
                    os.mkdir(dest_dir)

    for x in sorted(list(range(0,slice_no))):
              slice_dest  = x+1
              if x==0:
                        dicom_range = sorted(list(range(0,number_of_phases)))
              else:
                        dicom_range =  [n+number_of_phases for n in dicom_range] 
              for j in dicom_range:
                        dicom_to_move = dicoms[j]
                        dir_to_move = os.path.join(cur_dir,dicom_to_move)
                        if slice_dest in sorted(range(0,10)):
                            dir_to_dest = os.path.join(cur_dir, "slice_0" +str(slice_dest),dicom_to_move)
                            destination = os.path.join(cur_dir, "slice_0" +str(slice_dest))
                            if os.path.exists(dir_to_dest) is False:
                                                       shutil.move(dir_to_move,destination)
                        else:
                            dir_to_dest = os.path.join(cur_dir, "slice_" +str(slice_dest),dicom_to_move)
                            destination = os.path.join(cur_dir, "slice_" +str(slice_dest))
                            if os.path.exists(dir_to_dest) is False:
                                                       shutil.move(dir_to_move,destination)
                        

def la_folder(dcm, path):
    command = dcm2nii_dir + " -p n -f %f -z y "  +  dcm + " " + path
    os.system(command)
    

def multiple_folders(path):
    # Convert and merge the subfolders on the directory with the multiple subfolders format
    cur_dir = path
    os.chdir(cur_dir)
    patient_folders = sorted(os.listdir(cur_dir))

    # Rename subfolders and DICOM files within those subfolders
    for patient in patient_folders:
            patient_path = os.path.join(cur_dir,patient)
            os.chdir(patient_path)
            slice_folders = sorted(os.listdir(patient_path))
            slice_number = len(slice_folders)
            for slice_no in sorted(range(1,slice_number+1)):
                if slice_no in sorted(range(1,10)):
                    new_slice_name = patient + "_0" + str(slice_no) + "_SAX"
                    if os.path.exists(new_slice_name) is False:
                        rename(slice_folders[slice_no-1],new_slice_name)
                        new_slice_path = os.path.join(cur_dir,patient,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(patient_path)
                            else:
                                os.chdir(patient_path)
                    else:
                        new_slice_path = os.path.join(cur_dir,patient,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(patient_path)
                            else:
                                os.chdir(patient_path)
                else:
                    new_slice_name = patient + "_" + str(slice_no) + "_SAX"
                    if os.path.exists(new_slice_name) is False:
                        rename(slice_folders[slice_no-1],new_slice_name)
                        new_slice_path = os.path.join(cur_dir,patient,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(patient_path)
                            else:
                                os.chdir(patient_path)
                    else:
                        new_slice_path = os.path.join(cur_dir,patient,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(patient_path)
                            else:
                                os.chdir(patient_path)

            # Conversion and merging
            slice_folders = sorted(os.listdir(patient_path))
            
            dir_name = slice_folders[0]
            dicom_name = '{0}/{0}_001.dcm'.format(dir_name)
            d = dicom.read_file(dicom_name)
            X = d.Columns
            Y = d.Rows
            T = d.CardiacNumberOfImages
            dx = float(d.PixelSpacing[1])
            dy = float(d.PixelSpacing[0])
            dz = d.SpacingBetweenSlices
            Z = slice_number

            # The coordinate of the upper-left voxel
            pos_ul = np.array([float(x) for x in d.ImagePositionPatient])
            pos_ul[:2] = -pos_ul[:2]

            # Image orientation
            axis_x = np.array([float(x) for x in d.ImageOrientationPatient[:3]])
            axis_y = np.array([float(x) for x in d.ImageOrientationPatient[3:]])
            axis_x[:2] = -axis_x[:2]
            axis_y[:2] = -axis_y[:2]

            # Read the dicom file at the second time point
            dicom_name = '{0}/{0}_002.dcm'.format(dir_name)
            d2 = dicom.read_file(dicom_name)
            dt = (d2.TriggerTime - d.TriggerTime) * 1e-3

            # Read the dicom file at the second slice
            dir_name = slice_folders[1]
            dicom_name = '{0}/{0}_001.dcm'.format(dir_name)
            d2 = dicom.read_file(dicom_name)
            pos_ul2 = np.array([float(x) for x in d2.ImagePositionPatient])
            pos_ul2[:2] = -pos_ul2[:2]
            axis_z = pos_ul2 - pos_ul
            axis_z = axis_z / np.linalg.norm(axis_z)

            # Affine matrix which converts the voxel coordinate to world coordinate
            affine = np.eye(4)
            affine[:3,0] = axis_x * dx
            affine[:3,1] = axis_y * dy
            affine[:3,2] = axis_z * dz
            affine[:3,3] = pos_ul

            # The 4D volume
            volume = np.zeros((X, Y, Z, T), dtype='float32')

            z_new=-1
            # Go through each slice
            for z in range(0,slice_number-1):
                z_new=z_new+1
                # Read the images
                for t in range(0, T):
                    dir_name = slice_folders[z]
                    dicom_name = '{0}/{0}_{1:03d}.dcm'.format(dir_name, t + 1 )
                    d = dicom.read_file(dicom_name)
                    volume[:, :, z_new, t] = d.pixel_array.transpose()

            # Write the 4D volume
            filename = 'lvsa.nii.gz'
            nim = nib.Nifti1Image(volume, affine)
            nim.header['pixdim'][4] = dt
            nim.header['sform_code'] = 1
            nib.save(nim, filename)

def multiple_folders_2(case,path):
            patient = case
            view_path = path
            os.chdir(view_path)
            slice_folders = sorted(os.listdir(view_path))
            slice_number = len(slice_folders)
            for slice_no in sorted(range(1,slice_number+1)):
                if slice_no in sorted(range(1,10)):
                    new_slice_name = patient + "_0" + str(slice_no) + "_SAX"
                    if os.path.exists(new_slice_name) is False:
                        rename(slice_folders[slice_no-1],new_slice_name)
                        new_slice_path = os.path.join(view_path,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(view_path)
                            else:
                                os.chdir(view_path)
                    else:
                        new_slice_path = os.path.join(view_path,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(view_path)
                            else:
                                os.chdir(view_path)
                else:
                    new_slice_name = patient + "_" + str(slice_no) + "_SAX"
                    if os.path.exists(new_slice_name) is False:
                        rename(slice_folders[slice_no-1],new_slice_name)
                        new_slice_path = os.path.join(view_path,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(view_path)
                            else:
                                os.chdir(view_path)
                    else:
                        new_slice_path = os.path.join(view_path,new_slice_name)
                        os.chdir(new_slice_path)
                        phases_files = sorted(os.listdir(new_slice_path))
                        phases_number = len(phases_files)
                        for r in sorted(range (0, phases_number)):
                            dicom_name = '{0}_{1:03d}.dcm'.format(new_slice_name, r + 1 )
                            os.chdir(new_slice_path)
                            if os.path.exists(dicom_name) is False:
                                rename(phases_files[r-1],dicom_name)
                                os.chdir(view_path)
                            else:
                                os.chdir(view_path)

            # Conversion and merging
            slice_folders = sorted(os.listdir(view_path))
            
            dir_name = slice_folders[0]
            dicom_name = '{0}/{0}_001.dcm'.format(dir_name)
            d = dicom.read_file(dicom_name)
            X = d.Columns
            Y = d.Rows
            try:
                            T = d.CardiacNumberOfImages
            except:
                            T = phases_number
                            
            dx = float(d.PixelSpacing[1])
            dy = float(d.PixelSpacing[0])
           # dz = d.SpacingBetweenSlices
            dz = d.SliceThickness
           # try:
                            #dz = d.SpacingBetweenSlices

            #except:
                            #dz = d.SliceThickness

            Z = slice_number

            # The coordinate of the upper-left voxel
            pos_ul = np.array([float(x) for x in d.ImagePositionPatient])
            pos_ul[:2] = -pos_ul[:2]

            # Image orientation
            axis_x = np.array([float(x) for x in d.ImageOrientationPatient[:3]])
            axis_y = np.array([float(x) for x in d.ImageOrientationPatient[3:]])
            axis_x[:2] = -axis_x[:2]
            axis_y[:2] = -axis_y[:2]

            # Read the dicom file at the second time point
            dicom_name = '{0}/{0}_002.dcm'.format(dir_name)
            d2 = dicom.read_file(dicom_name)
            dt = (d2.TriggerTime - d.TriggerTime) * 1e-3

            # Read the dicom file at the second slice
            dir_name = slice_folders[1]
            dicom_name = '{0}/{0}_001.dcm'.format(dir_name)
            d2 = dicom.read_file(dicom_name)
            pos_ul2 = np.array([float(x) for x in d2.ImagePositionPatient])
            pos_ul2[:2] = -pos_ul2[:2]
            axis_z = pos_ul2 - pos_ul
            axis_z = axis_z / np.linalg.norm(axis_z)

            # Affine matrix which converts the voxel coordinate to world coordinate
            affine = np.eye(4)
            affine[:3,0] = axis_x * dx
            affine[:3,1] = axis_y * dy
            affine[:3,2] = axis_z * dz
            affine[:3,3] = pos_ul

            # The 4D volume
            volume = np.zeros((X, Y, Z, T), dtype='float32')

            z_new=-1
            # Go through each slice
            for z in range(0,slice_number-1):
                z_new=z_new+1
                # Read the images
                for t in range(0, T):
                    dir_name = slice_folders[z]
                    dicom_name = '{0}/{0}_{1:03d}.dcm'.format(dir_name, t + 1 )
                    d = dicom.read_file(dicom_name)
                    volume[:, :, z_new, t] = d.pixel_array.transpose()

            # Write the 4D volume
            filename = "LVSA.nii.gz"
            nim = nib.Nifti1Image(volume, affine)
            nim.header['pixdim'][4] = dt
            nim.header['sform_code'] = 1
            nib.save(nim, filename)
