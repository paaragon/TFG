function [ GHI ] = meinel( cosz,Io )
%Meinel model (1976)
%   Detailed explanation goes here
AM = 1 / abs(cosz);
GHI = Io * (0.7^0.678);

end

