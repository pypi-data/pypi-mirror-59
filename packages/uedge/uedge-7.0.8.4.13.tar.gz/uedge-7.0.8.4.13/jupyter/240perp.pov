// Persistence Of Vision raytracer version 2.0 sample file.

// Sample file:  A good starting point for your own test images.

#include "colors.inc"

#declare gap=0.3;
#declare bh=0;
#declare torang = 206.25;
#declare torang = 176.25; #declare torang = 0.25; #declare torang = 191.25; #declare torang = clock;
#declare plas = color BrightGold*2;


//Reduced distsq ----------------->       2.14729
#declare campos = <     -124.689,     -66.7353,      202.006>;
#declare ski = <      0.00000,      1.00000,      0.00000>;
#declare la =  <     -135.349,     -122.146,     -28.4399>;
#declare vert =       74.1148;
#declare horiz =       120.000;
#declare dir =  la - campos;



camera {

location campos
//sky ski
direction dir
look_at  la
up <0,      vert,0>
right <     horiz,0,0>
}


#include "d3d.inc"

#declare BIN0 = color Red*2;
#declare BIN1 = color Red*2;
#declare BIN2 = color Red*2;
#declare BIN3 = color Red*2;
#declare BIN4 = color Red*2;
#declare BIN5 = color Red*2;
#declare BIN6 = color Red*2;
#declare BIN7 = color Red*2;
#declare BIN8 = color Red*2;
#declare BIN9 = color Red*2;
#declare tBIN0 = 1.0;
#declare tBIN1 = 1.0;
#declare tBIN2 = 1.0;
#declare tBIN3 = 0.92;
#declare tBIN4 = 0.90;
#declare tBIN5 = 0.88;
#declare tBIN6 = 0.86;
#declare tBIN7 = 0.84;
#declare tBIN8 = 0.82;
#declare tBIN9 = 0.80;

/*
union {
#include "nc45.inc"
}
*/
lathe {
linear_spline 
4, 
<161, -96>,
<160, -96>,
<160, -95>,
<161, -95>
pigment { rgbf <1,0,0,1> }
hollow
interior {
media { 
   emission 0.05
   scattering {1, 0.1 } 
   //absorption 0.01
   }
fade_distance 0.01
fade_power 0.5
}
}

object { d3dtiles }
object { d3dvacuum }

// light source to illuminate vessel
light_source { campos colour White}

