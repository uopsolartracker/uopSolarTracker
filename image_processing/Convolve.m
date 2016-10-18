% This function finds the convolution between an image a kernel made up of
% weights. This function assumes the input is a grayscale image
function [Out] = Convolve(Input,kernel)
    [height,width,] = size(Input);
    Out = zeros(height,width);
    [ker_h,ker_w,] = size(kernel);
    for x = 1:height
        for y = 1:width
            sum = 0;
            for k = 1:ker_h
                for l = 1:ker_w
                    offsetx = x + k - floor(ker_h/2) - 1;
                    offsety = y + l - floor(ker_w/2) - 1;
                    % Check offset is within bounds of image
                    if(offsetx >= 1 && offsety >= 1 && offsetx <= height && offsety <= width)
                        sum = sum + Input(offsetx,offsety)*kernel(k,l);
                    end
                end
            end
            Out(x,y) = sum;
        end
    end
end