library(raster)
library(gdistance)

# Load raw data w/ NIWA crs 3994
depths <-raster(x="data/bathy/depths.tif")

# not interested in things above ground
depths[depths>0] <- NA


# Want depths to be positive for shallow wave velocity function
depths <- abs(depths)

saveRDS(depths, "data/out/mod_depths.rds")

depths <- aggregate(depths , fact=10) # decrease resolution to 2.5km sqr from original 250m
#depths <- aggregate(depths, fact=20) # decrease resolution to 5km sqr 

plot(depths)
depthDiff <- function(x){x[2] - x[1]}
hd <- transition(depths, function(x) { mean(x)}, 8, symm=FALSE)  

speed <- hd
adj <- adjacent(depths, cells=1:ncell(depths), pairs=TRUE, directions=8)
SQRT_G = sqrt(9.81)

#this is the crux of it all. 
speed[adj] = SQRT_G * sqrt(hd[adj])

Conductance <- geoCorrection(speed)
saveRDS(Conductance, "data/out/conductance.rds")

