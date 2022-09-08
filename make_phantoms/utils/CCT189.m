function ell = CCT189(patient_diameter, attenuation_coefficient, relative_lesion_diameter)
    % creates CATPHAN 600 low contrast detectability module but
    % with options for variable patient diameter and lesion diameter
    % ======= 
    % inputs:
    % patient_diameter: diameter of circle in mm
    %  - relative_lesion_diameter: diameter of lesion diameter relative to patient diameter [unitless], absolute diameter can be found as relative_lesion_diameter*patient_diameter
    %  - attenuation_coefficient:  [units: 1/mm] default is for water at 60 keV, if taking values from standard tables which report in 1/cm, be sure to divide by 10 to convert to 1/mm
    if exist('patient_diameter', 'var') == false
        patient_diameter = 150;
    end

    if exist('relative_lesion_diameter', 'var') == false
        relative_lesion_diameter = 0.4;
    end

    if exist('attenuation_coefficient', 'var') == false
        attenuation_coefficient = 0.2;
    end

    d = relative_lesion_diameter*patient_diameter / 2;
    ell = [0 0 patient_diameter/2 patient_diameter/2 0 attenuation_coefficient;                                  % water
    d*cosd(45)  d*sind(45)   3/2  3/2 0 14/1000*attenuation_coefficient;     % 3mm, 14 HU
   -d*cosd(45)  d*sind(45)   5/2  5/2 0 7/1000*attenuation_coefficient;     % 5 mm, 7 HU
   -d*cosd(45) -d*sind(45)   7/2  7/2 0 5/1000*attenuation_coefficient;     % 7 mm, 5 HU
    d*cosd(45) -d*sind(45)  10/2 10/2 0 3/1000*attenuation_coefficient;     % 10 mm, 3 HU
    ];
end