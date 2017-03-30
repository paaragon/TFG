function [ Io ] = extraTerretRad( doy )
%UNTITLED3 Extraterrestrial Radation
%   Radiacion que llega a la parte exterior de la atmosfera
% depende del dia del anio. Modelo ASCE (Aleen et al)

Io = 1367.7*(1 + 0.033*cosd( (2*pi*doy)/365));

end

