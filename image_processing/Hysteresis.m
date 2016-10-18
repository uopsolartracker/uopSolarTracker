function [Out] = Hysteresis(NMS_image)
    [height,width,] = size(NMS_image);
    Hyst = zeros(height,width);
%     intensities = hist(NMS_image(:), 0:255); % Get number of pixels at each bin
%     percentage = intensities./(height*width)*100;
    t_hi = floor(prctile(NMS_image(:),90)); % Get 90th percentile
    t_lo = floor(t_hi * 0.2);
    for x = 1:height
        for y = 1:width
            if (NMS_image(x,y) > t_hi)
                Hyst(x,y) = 255; % Strong edge
            elseif(NMS_image(x,y) > t_lo)
                Hyst(x,y) = 125; % Weak edge
            else
                Hyst(x,y) = 0; % Non-edge pixel
            end
        end
    end
    Out = Hyst;
    for x = 1:height
        for y = 1:width
            if(Hyst(x,y) == 125)
                if(anynearest8(Hyst,x,y)) % is 255
                    Out(x,y) = 255;
                else
                    Out(x,y) = 0; % Suppress if no strong pixel connection
                end
            end
        end
    end
end

% This searches the 8 pixels around the center (x,y) for one with
% intensity, returning 1 if found or 0 if not
function [bool] = anynearest8(Hyst,x,y)
    [height,width,] = size(Hyst);
    bool = 0;
    for k = -1:1
        for l = -1:1
            offsetx = x + k;
            offsety = y + l;
            if(offsetx > 0 && offsety > 0 && offsetx <= height...
                    && offsety <= width)
                if(Hyst(offsetx,offsety) == 255)
                    bool = 1;
                    break % We're done here
                end
            end
        end
    end
end