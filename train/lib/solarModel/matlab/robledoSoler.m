function [ GHI ] = robledoSoler( z )
%robledoSoler calculo GHI usando el modelo de Robledo-Soler (2000)
% z es el Zenith Angle
GHI = 1159.24*abs(cosd(z))^1.179 * exp(-0.0019*(90-abs(z)));

end

