function [ d ] = declination( DOY )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

B = (DOY-81)*(360/365);
d = 23.45*sind(B);

end

