#imports os and module to run new codes/apps by initialzing new processes
#Installations Required: Python, IDE runner ex. VSC,
#os.path.join constructs directory based on combining path components
#process.communicate is used to capture output and error from command

#formatting: f' string formatting

import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Command failed with error: {err}")
    else:
        print(out)

def main():
    bids_dir = input("Enter the path to the BIDS data folder: ")
    acqparams = input("Enter the path to acqparams.txt: ")
    index = input("Enter the path to index.txt: ")

    subjects = [d for d in os.listdir(bids_dir) if os.path.isdir(os.path.join(bids_dir, d))]

    for subject in subjects:
        subject_dir = os.path.join(bids_dir, subject, 'ses-1', 'dwi')

        #mrconvert - converts the DWI data to the MRtrix format 
        in_file_ap = os.path.join(subject_dir, f'{subject}_dir_AP-ses-1_dwi.nii.gz')
        out_file_mif = os.path.join(subject_dir, f'{subject}_dir_AP-ses-1_dwi.mif')
        bvec_file = os.path.join(subject_dir, f'{subject}_ses-1_dwi.bvec')
        bval_file = os.path.join(subject_dir, f'{subject}_ses-1_dwi.bval')
        command = f'mrconvert {in_file_ap} {out_file_mif} -fslgrad {bvec_file} {bval_file}'
        run_command(command)

        #dwidenoise - denoises the DWI data using MRtrix command
        in_file_dn = os.path.join(subject_dir, f'{subject}_dwi_dn.mif')
        command = f'dwidenoise {out_file_mif} {in_file_dn}'
        run_command(command)

        #mrdegibbs - corrects for gibbs r artifacts using MRtrix command
        out_file_un = os.path.join(subject_dir, f'{subject}_dwi_dn_un.nii.gz')
        command = f'mrdegibbs {in_file_dn} {out_file_un}'
        run_command(command)

        #createtopupinfile (assuming this is a custom function you will define)
        #topup_in_file = createtopupinfile(subject_dir, subject)
        
        #run topup
        #topup_out_prefix = os.path.join(subject_dir, f'{subject}_topup_result')
        #command = f'topup --imain={topup_in_file} --datain={acqparams} --config=b02b0.cnf --out={topup_out_prefix}'
        #run_command(command)
        
        #run eddy
        #eddy_out_prefix = os.path.join(subject_dir, f'{subject}_eddy_out')
        #command = f'eddy --imain={out_file_un} --mask={subject_dir}/brain_mask.nii.gz --acqp={acqparams} --index={index} --topup={topup_out_prefix} --out={eddy_out_prefix}'
        #run_command(command)

if __name__ == "__main__":
    main()