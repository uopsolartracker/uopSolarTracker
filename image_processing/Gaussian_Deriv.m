function [kernel,w] = Gaussian_Deriv(sigma)
    a = round(2.5*sigma - 0.5);
    w = 2*a + 1;
    kernel = zeros(w,1);
    sum = 0;
    for i = 1:w
        kernel(i) = -1*(i - 1 - a)*exp((-1*(i - 1 - a)*(i - 1 - a)) / (2*(sigma)^2));
        sum = sum - i*kernel(i);
    end
    kernel = kernel./sum;
end