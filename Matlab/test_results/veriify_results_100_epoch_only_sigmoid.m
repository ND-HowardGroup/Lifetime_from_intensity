close all
clear all
clc

%author: varun mannam
%date: 02-01-2020
%eepochs = 100
format long;
font = 12;

est1 = load('estimated_test_hsv_m2_3d_128_sig.mat');
est1 = est1.estimated_test_hsv_m2_3d;

est2 = load('estimated_test_hsv_m2_3d_128_tan.mat');
est2 = est2.estimated_test_hsv_m2_3d;

est3 = load('estimated_test_hsv_m2_3d_256_sig.mat');
est3 = est3.estimated_test_hsv_m2_3d;

est4 = load('estimated_test_hsv_m2_3d_256_tan.mat');
est4 = est4.estimated_test_hsv_m2_3d;


est1 = permute(est1,[2,3,1]);
est2 = permute(est2,[2,3,1]);
est3 = permute(est3,[2,3,1]);
est4 = permute(est4,[2,3,1]);


rgb1 = hsv2rgb(est1);
rgb2 = hsv2rgb(est2);
rgb3 = hsv2rgb(est3);
rgb4 = hsv2rgb(est4);

%hue
hmax = 0.7;
hmin = 0;



% customized hsv colormap
m = 1000; % number of colormap bins
map_hue = linspace(hmax,hmin,m)'; % scale of hue
map_saturation = ones(m,1);
map_value = ones(m,1);
hsvmap = [map_hue map_saturation map_value];
rgbmap = hsv2rgb(hsvmap);

tau_min1 = 0;
tau_max1 = 10e-9;
tau_min = 1e-9;
tau_max = 4e-9;

figure, 
subplot(1,2,1), imagesc(rgb1);
title('128 chunk sig')
colormap(rgbmap);
c = colorbar;
c.Label.String = 'Lifetime (s)';
c.Label.FontSize = font;
caxis([tau_min tau_max1])
axis equal tight
set(gca,'FontSize',font)

% subplot(2,2,2), imagesc(rgb2);
% title('128 chunk tan')
% colormap(rgbmap);
% c = colorbar;
% c.Label.String = 'Lifetime (s)';
% c.Label.FontSize = font;
% caxis([tau_min tau_max1])
% axis equal tight
% set(gca,'FontSize',font)

subplot(1,2,2), imagesc(rgb3);
title('256 chunk sig')
colormap(rgbmap);
c = colorbar;
c.Label.String = 'Lifetime (s)';
c.Label.FontSize = font;
caxis([tau_min tau_max1])
axis equal tight
set(gca,'FontSize',font)

% subplot(2,2,4), imagesc(rgb4);
% title('256 chunk tan')
% colormap(rgbmap);
% c = colorbar;
% c.Label.String = 'Lifetime (s)';
% c.Label.FontSize = font;
% caxis([tau_min tau_max1])
% axis equal tight
% set(gca,'FontSize',font)

est5 = est1;
est6 = est2;
est7 = est3;
est8 = est4;

hmin = 0;
hmax = 0.7;

temp1 = (est5(:,:,1)-hmax)/(hmin-hmax);
temp1 = mat2gray(temp1,[0.1,0.4]);
est5(:,:,1) =  hmax+(hmin-hmax)*temp1;

temp2 = (est6(:,:,1)-hmax)/(hmin-hmax);
temp2 = mat2gray(temp2,[0.1,0.4]);
est6(:,:,1) =  hmax+(hmin-hmax)*temp2;

temp3 = (est7(:,:,1)-hmax)/(hmin-hmax);
temp3 = mat2gray(temp3,[0.1,0.4]);
est7(:,:,1) =  hmax+(hmin-hmax)*temp3;

temp4 = (est8(:,:,1)-hmax)/(hmin-hmax);
temp4 = mat2gray(temp4,[0.1,0.4]);
est8(:,:,1) =  hmax+(hmin-hmax)*temp4;

rgb5 = hsv2rgb(est5);
rgb6 = hsv2rgb(est6);
rgb7 = hsv2rgb(est7);
rgb8 = hsv2rgb(est8);

figure, 
subplot(1,2,1), imagesc(rgb5);
title('128 chunk sig')
colormap(rgbmap);
c = colorbar;
c.Label.String = 'Lifetime (s)';
c.Label.FontSize = font;
caxis([tau_min tau_max])
axis equal tight
set(gca,'FontSize',font)

% subplot(2,2,2), imagesc(rgb6);
% title('128 chunk tan')
% colormap(rgbmap);
% c = colorbar;
% c.Label.String = 'Lifetime (s)';
% c.Label.FontSize = font;
% caxis([tau_min tau_max])
% axis equal tight
% set(gca,'FontSize',font)

subplot(1,2,2), imagesc(rgb7);
title('256 chunk sig')
colormap(rgbmap);
c = colorbar;
c.Label.String = 'Lifetime (s)';
c.Label.FontSize = font;
caxis([tau_min tau_max])
axis equal tight
set(gca,'FontSize',font)

% subplot(2,2,4), imagesc(rgb8);
% title('256 chunk tan')
% colormap(rgbmap);
% c = colorbar;
% c.Label.String = 'Lifetime (s)';
% c.Label.FontSize = font;
% caxis([tau_min tau_max])
% axis equal tight
% set(gca,'FontSize',font)


imwrite(rgb5,'estimated_lifetime_128_sig.png');
imwrite(rgb6,'estimated_lifetime_128_tan.png');
imwrite(rgb7,'estimated_lifetime_256_sig.png');
imwrite(rgb8,'estimated_lifetime_256_tan.png');



%adding target hsv result
addpath('/Users/varunmannam/Desktop/Spring20/Research_S20/Jan20/0201/images_3d_zf');

ip11 = Tiff('image_input_PM_FLIM_073.tif');
ip11 = double(read(ip11)); 

ip11 = (ip11-min(ip11(:)))/(max(ip11(:))-min(ip11(:)));

ip = Tiff('imageLifetime_PM_FLIM_073.tif');
ip = double(read(ip));

ip = mat2gray(ip,[tau_min,tau_max]); % limit to 1e-9 to 4e-9 in 0 to 1 range

% est1 = load('estimated_test_hsv_m2_3d_256.mat');
% est1 = est1.estimated_test_hsv_m2_3d;
% 
% est2 = load('estimated_test_hsv_m2_3d_128.mat');
% est2 = est2.estimated_test_hsv_m2_3d;

%post_process
hmin = 0;
hmax = 0.7;

hsv_tar = zeros(360,360,3);
hsv_tar(:,:,1) = hmax+(hmin-hmax)*ip;
hsv_tar(:,:,2) = ones(360,360);
hsv_tar(:,:,3) = ip11;

rgb_tar = hsv2rgb(hsv_tar);

