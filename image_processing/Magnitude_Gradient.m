function [Gxy,Gangle] = Magnitude_Gradient(G_horiz,G_vert)
    [height,width,] = size(G_horiz); % Assuming the sizes of horizontal and vertical match
    Gxy = zeros(height,width);
    Gangle = zeros(height,width);
    for x = 1:height
        for y = 1:width
            Gxy(x,y) = sqrt((G_horiz(x,y))^2 + (G_vert(x,y))^2); % Euclidian
            Gangle(x,y) = atan2(G_horiz(x,y),G_horiz(x,y));
        end
    end
end