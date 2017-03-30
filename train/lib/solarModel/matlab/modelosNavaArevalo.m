% Aplicamos el modelo a Nava de Arevalo
latNavas = 40.9904320;
longNavas = -4.7578942;

dias = 0:364; % para cada dia del anio
horas = 0:(1/60):23; %resolucion de minutos
GHIRS = [];
GHIAdnot = [];
GHIKast = [];
GHIDPP = [];
GHIMeinel = [];
for doy = dias
    for h = 1:length(horas)
    %% calculo
    [z,cosz] = zentihAngle(latNavas,longNavas,doy,horas(h));
    GHIRS(doy+1,h) = robledoSoler(z);
    GHIKast(doy+1,h)= kasten(cosz);
    GHIAdnot(doy+1,h)= adnot(cosz);
    GHIDPP(doy+1,h) = dpp( z,cosz );
    %GHIMeinel(doy+1,h)= meinel(cosz,extraTerretRad(doy));
    end
end
% Represento 2 o 3 dias
diasToPlot =[1, 81, 200];
for i = 1:length(diasToPlot)
    d = diasToPlot(i);
    figure(i);
    titulo=sprintf('Dia %d',d);
    title(titulo);
    plot(horas,GHIRS(d,:), "color", "yellow");
    hold on;
    %print -djpg image.jpg
    plot(horas,GHIAdnot(d,:), "color", "red");
    plot(horas,GHIKast(d,:), "color", "blue");
    plot(horas,GHIDPP(d,:), "color", "green");
    %plot(horas,GHIMeinel(d,:), "color", "black");
    legend('Robledo-soler','Adnot','Kast', 'DPP');
    hold off;
end
