function [ hra ] = hourAngle( DOY, hora, long, LSTM )
%hourAngle calcula el "hour Angle" 
% Convierte la hora local (LST) 
%  en los grados que se mueve el sol por el cielo. Debe seer 0 al mediodia
% B engrados
B = (DOY-81)*(360/365);

%equation of time (in minutes)
EoT = 9.87*sind(2*B)  - 7.53*cosd(B) - 1.5*sind(B);

%time correction factor (in minutes)
TC = 4*(long - LSTM) + EoT;

%local solar time (en horas)
LST = hora + TC/60;

% hour angel (en grados)
hra = 15*(LST - 12);

end

