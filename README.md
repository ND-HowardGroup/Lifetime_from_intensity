# Poster_code_Fall19

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
pass through the autoencoder with minimum latent space of 8x8 (in between convolutional layers the Batch-norm is enabled) and bring it back to original image dimension of 128x128 with 3 output channels (to represent the HSV format where hue and value are mapped to lifetime and intensity respectively). 
in the best model: The last layer is sigmoid
best input and output chunk size: 128x128


## License & Copyright
© 2019 Varun Mannam, University of Notre Dame

Licensed under the [Apache License 2.0](https://github.com/varunmannam/Poster_code_fall19/blob/master/LICENSE.txt)


# Data 
For the data visualization [Youtube].(https://www.youtube.com/watch?v=v3Bk3JNA5nM&ab_channel=YideZhang)
