function [ z,cosz ] = zentihAngle( lat,long,DOY,hora )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

 d = declination(DOY);
 
 % assuming spain -> LSTM = 0
 hra =  hourAngle( DOY, hora, long, 0 );
 
 %cosz = cosd(lat)*cosd(d)*cosd(hra)+sind(lat)*sind(d);
 cosz = cosd(lat)*cosd(d)*cosd(hra) + sind(lat)*sind(d);
 z = acosd(cosz);
 
 %%Correccion nacho: si el angulo es mayor de 90, lo dejamos en 90
 %% porque querra decir que es de noche
 if (abs(z) > 90) 
     z=90;
     cosz=0;
 end
end

