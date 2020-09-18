# Lifetiem_from_intensity_code

# For intesnity image denoising: 
Refer to [Code:] (https://github.com/ND-HowardGroup/Biophotonics_Congress_Conference_2020_code)

Refer to [Plugin:] (https://github.com/ND-HowardGroup/Image_denoising/tree/master/Image_Denoising_Plugin)

# For estimation of lifetime from intensity code:

Input intensity Image:

![](Final%20results/image_input_PM_FLIM_073.png)

Estimated lifetime Image: From CNN ML model (with autoencoder architecture): In the HSV format, where hue and value are mapped to lifetime and intensity respectively.

![](Final%20results/estimated_128_rgb_3d.png)

Target lifetime Image: In the HSV format, where hue and value are mapped to lifetime and intensity respectively.

![](Final%20results/target_rgb_3d.png)

# ML model:

Input dimensions are: 360x360 slices into 128x128 images
pass through the autoencoder with minimum latent space of 8x8 (in between convolutional layers the Batch-norm is enabled) and bring it back to original image dimension of 128x128 with 3 output channels (to represent the HSV format where hue and value are mapped to lifetime and intensity respectively). Now stich the output images of 128x128 to 360x360 size.

ML best model: The last layer is sigmoid and best input and output chunk size is 128x128. 

# Dataset:

#Images: The training and test dataset can be downloaded from here https://curate.nd.edu/show/jd472v2759b

#Citation for dataset: Please cite the LFI dataset using the following format: 
Mannam, Varun. “Lifetime From Intensity (LFI) Dataset.” Notre Dame, August 13, 2019. https://doi.org/10.7274/r0-ac46-ft93.

## License & Copyright
© 2019 Varun Mannam, University of Notre Dame

Licensed under the [GPL](https://github.com/varunmannam/Poster_code_fall19/blob/master/LICENSE)


# Data 
For the data visualization [Youtube].(https://www.youtube.com/watch?v=v3Bk3JNA5nM&ab_channel=YideZhang)
