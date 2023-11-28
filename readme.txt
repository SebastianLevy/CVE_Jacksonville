readme

select the corners of the area you wish to create (eating area, line waiting area, coffee making area etc) - right click for all but last point, middle click for last point in area

do ^ for each area

results in the img w/designated area borders drawn in red
also results in a mask w/ black background, and each area filled in w different color

if given a point x,y - reference the mask, if the mask is a certain color - x,y is within an area, use color to determine which area

dictionary of areas w/ their vertices and color representatives saved in json file
