function [ gc ] = adnot( cosz )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
a = 951.39;
b = 1.15;

gc = a*(abs(cosz)).^b;

end

