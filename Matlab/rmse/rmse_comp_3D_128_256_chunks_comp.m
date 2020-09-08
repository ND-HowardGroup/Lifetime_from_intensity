%
%Author: Varun Mannam
%date: 10th Dec 2019
close all
clear variables
clc
format long
font = 14;
%input and target are normalised to (0 to 1) and multiplied with 255 (8 bit
%information)
%target: -> replaced all NAN values with 0's  and normalised (0 to 10nsec to 0 to 1)
%input =  imread('I_5-13-2016 sham field 9_IU-FLIM_50.png');
%index = 27 for PM_FLIM
% close all
% clear variables
% clc

%gray scale image_Lifetime images directly...
rmse_train1 = load('3D_zebrafish_PM_FLIM_train_rmse_epochs_hsv_m2_128_sig.txt');
rmse_train2 = load('3D_zebrafish_PM_FLIM_train_rmse_epochs_hsv_m2_128_tan.txt');
rmse_train3 = load('3D_zebrafish_PM_FLIM_train_rmse_epochs_hsv_m2_256_sig.txt');
rmse_train4 = load('3D_zebrafish_PM_FLIM_train_rmse_epochs_hsv_m2_256_tan.txt');


rmse_test1 = load('3D_zebrafish_PM_FLIM_test_rmse_epochs_hsv_m2_128_sig.txt');
rmse_test2 = load('3D_zebrafish_PM_FLIM_test_rmse_epochs_hsv_m2_128_tan.txt');
rmse_test3 = load('3D_zebrafish_PM_FLIM_test_rmse_epochs_hsv_m2_256_sig.txt');
rmse_test4 = load('3D_zebrafish_PM_FLIM_test_rmse_epochs_hsv_m2_256_tan.txt');

% x=[1:200]';
% figure(1), 
% plot(x,rmse_train1,'r*','Linewidth',1);
% hold on
% plot(x,rmse_train2,'b--','Linewidth',1);
% 
% plot(x,rmse_test1,'md','Linewidth',1);
% plot(x,rmse_test2,'co','Linewidth',1);
% xlabel('Epochs');
% ylabel('MSE value');
% legend('Train MSE: HSV (128 chunk)','Train MSE: RGB (128 chunk)','Test MSE: HSV (128 chunk)','Test MSE: RGB (128 chunk)');
% title('128 chunk RMSE comparison');
% set(gca,'FontSize',font);
% 
% 
% figure(2), 
% plot(x,rmse_train1,'r*','Linewidth',1);
% hold on
% plot(x,rmse_train2,'b--','Linewidth',1);
% 
% plot(x,rmse_test1,'md','Linewidth',1);
% plot(x,rmse_test2,'co','Linewidth',1);
% xlabel('Epochs');
% ylabel('MSE value');
% legend('Train MSE: HSV (128 chunk)','Train MSE: RGB (128 chunk)','Test MSE: HSV (128 chunk)','Test MSE: RGB (128 chunk)');
% title('128 chunk Zoom RMSE comparison');
% set(gca,'FontSize',font);
% xlim([190 200]);
% 
% 
% x1=[1:100]';
% figure(3), 
% plot(x1,rmse_train3,'r*','Linewidth',1);
% hold on
% plot(x1,rmse_train4,'b--','Linewidth',1);
% 
% plot(x1,rmse_test3,'md','Linewidth',1);
% plot(x1,rmse_test4,'co','Linewidth',1);
% xlabel('Epochs');
% ylabel('MSE value');
% legend('Train MSE: HSV (256 chunk)','Train MSE: RGB (256 chunk)','Test MSE: HSV (256 chunk)','Test MSE: RGB (256 chunk)');
% title('256 chunk RMSE comparison');
% set(gca,'FontSize',font);
% 
% 
% figure(4), 
% plot(x1,rmse_train3,'r*','Linewidth',1);
% hold on
% plot(x1,rmse_train4,'b--','Linewidth',1);
% 
% plot(x1,rmse_test3,'md','Linewidth',1);
% plot(x1,rmse_test4,'co','Linewidth',1);
% xlabel('Epochs');
% ylabel('MSE value');
% legend('Train MSE: HSV (256 chunk)','Train MSE: RGB (256 chunk)','Test MSE: HSV (256 chunk)','Test MSE: RGB (256 chunk)');
% title('256 chunk Zoom RMSE comparison');
% set(gca,'FontSize',font);
% xlim([90 100]);


% x2=[1:100]';
% figure(1)
% plot(x2,rmse_train1(1:100),'r*','Linewidth',1);
% hold on
% plot(x2,rmse_train2(1:100),'b--','Linewidth',1);
% 
% plot(x2,rmse_train3,'md','Linewidth',1);
% plot(x2,rmse_train4,'co','Linewidth',1);
% xlabel('Epochs');
% ylabel('MSE value');
% legend('Train MSE: HSV (128 chunk)','Train MSE: RGB (128 chunk)','Train MSE: HSV (256 chunk)','Train MSE: RGB (256 chunk)');
% title('train RMSE comparison');
% set(gca,'FontSize',font);

x2=[1:100]';
figure(1)
plot(x2,rmse_train1(1:100),'r*','Linewidth',1);
hold on
plot(x2,rmse_train2(1:100),'b--','Linewidth',1);

plot(x2,rmse_train3,'md','Linewidth',1);
plot(x2,rmse_train4,'co','Linewidth',1);
xlabel('Epochs');
ylabel('MSE value');
legend('Train MSE: HSV (128 chunk - sigmoid)','Train MSE: HSV (128 chunk - tanh)','Train MSE: HSV (256 chunk - sigmoid)','Train MSE: HSV (256 chunk - tanh)');
title('train RMSE comparison');
set(gca,'FontSize',font);
xlim([90 100]);


figure(2)
plot(x2,rmse_test1(1:100),'r*','Linewidth',1);
hold on
plot(x2,rmse_test2(1:100),'b--','Linewidth',1);

plot(x2,rmse_test3,'md','Linewidth',1);
plot(x2,rmse_test4,'co','Linewidth',1);
xlabel('Epochs');
ylabel('MSE value');
legend('Test MSE: HSV (128 chunk - sigmoid)','Test MSE: HSV (128 chunk - tanh)','Test MSE: HSV (256 chunk - sigmoid)','Test MSE: HSV (256 chunk - tanh)');
title('test RMSE comparison');
set(gca,'FontSize',font);
xlim([90 100]);

