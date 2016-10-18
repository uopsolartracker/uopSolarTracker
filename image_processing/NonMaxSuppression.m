function [Out] = NonMaxSuppression(Gxy,Iangle)
    [height,width,] = size(Gxy); % Assuming Gxy and Iangle are the same size
    Out = Gxy;
    for x = 1:height
        for y = 1:width
            theta = Iangle(x,y)*180/pi; % Convert to degrees
            if(theta < 0) % Deal with the case where theta is negative
                theta = theta + pi;
            end
            if(theta <= 22.5 || theta > 157.5)
                if((x-1) > 0 && Gxy(x-1,y) > Gxy(x,y))
                    Out(x,y) = 0;
                elseif((x+1) <= height && Gxy(x+1,y) > Gxy(x,y))
                    Out(x,y) = 0;
                end
            elseif(theta > 22.5 && theta <= 67.5)
                if((y-1) > 0 && (x-1) > 0 && Gxy(x-1,y-1) > Gxy(x,y))
                    Out(x,y) = 0;
                elseif((y+1) <= width && (x+1) <= height && Gxy(x+1,y+1) > Gxy(x,y))
                    Out(x,y) = 0;
                end
            elseif(theta > 67.5 && theta <= 112.5)
                if((y-1) > 0 && Gxy(x,y-1) > Gxy(x,y))
                    Out(x,y) = 0;
                elseif((y+1) <= height && Gxy(x,y+1) > Gxy(x,y))
                    Out(x,y) = 0;
                end
            elseif(theta > 112.5 && theta <= 157.5)
                if((y+1) <= width && (x-1) > 0 && Gxy(x-1,y+1) > Gxy(x,y))
                    Out(x,y) = 0;
                elseif((y-1) > 0 && (x+1) <= height && Gxy(x+1,y-1) > Gxy(x,y))
                    Out(x,y) = 0;
                end
            end
        end
    end
end