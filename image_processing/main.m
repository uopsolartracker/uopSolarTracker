%% Program 3
% By Daniel Herink
%% Intensity of Change
[FileName,FilePath] = uigetfile('sun.jpg');
image = rgb2gray(imread(strcat(FilePath,FileName)));
imshow(image)
sigma = 1;
[vert_Gauss,wk] = Gaussian_Kernel(sigma);
[deriv_Gauss,wd] = Gaussian_Deriv(sigma);
temp_horiz = Convolve(image,vert_Gauss);
horiz_conv = Convolve(temp_horiz,deriv_Gauss');
temp_vert = Convolve(image,vert_Gauss');
vert_conv = Convolve(temp_vert,deriv_Gauss);
figure
imshow(uint8(horiz_conv))
title('Horizontal Components of Intensity Change')
figure
imshow(uint8(vert_conv))
title('Vertical Components of Intensity Change')
%% Magnitude and Angle
[Gxy,Iangle] = Magnitude_Gradient(horiz_conv, vert_conv);
figure
imshow(uint8(Gxy))
title('Magnitude Image')
figure
imshow(Iangle)
title('Gradient Image')
%% Non-Maximal Suppression
NMS_image = NonMaxSuppression(Gxy,Iangle);
% figure
% imshow(uint8(NMS_image))
% title('Non-Maximal Suppressed Image')
Hyst_image = Hysteresis(NMS_image);
figure
imshow(uint8(Hyst_image))
title('Edges')