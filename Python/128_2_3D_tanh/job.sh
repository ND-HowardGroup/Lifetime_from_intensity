#!/bin/csh

#$ -M vmannam@nd.edu	 # Email address for job notification
#$ -m abe		 # Send mail when job begins, ends and aborts
#$ -q gpu		 # Specify queue
#$ -l gpu_card=1
#$ -N m2_sig_hsv_3d_zf_128_chunk_tanh        # Specify job name

#$ -pe smp 4                # Specify parallel environment and legal core size
setenv OMP_NUM_THREADS 4	         # Required modules

module load pytorch
python3 hsv_pm_flim_3d_dataset_zebrafish_slices_sig_0201_128_chunk_tanh.py


