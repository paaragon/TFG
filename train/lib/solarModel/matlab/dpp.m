function [ GHI ] = dpp( z,cosz )
%DPP model (1978)
DNI = 950.2*(1 - exp(-0.075*(90-abs(z) ) ) );
diff = 14.29 + 21.04 *( pi/2 - abs(z)*pi/180);
GHI = DNI*abs(cosz) + diff;
end

