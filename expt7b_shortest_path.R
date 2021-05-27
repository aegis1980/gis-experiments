library(raster)
library(gdistance)
library(sf)
library(httr)
library(jsonlite)

# USGC event ids 
GISBORNE_M73 = 'us7000dffl'# mag 7.3, 174 km NE of Gisborne, New Zealand
KERMADEC_M74 = 'us7000dlk3' # mag 7.4 Kermadecs
KERMADEC_M81 = 'us7000dflf' # mag 8.1 Kermadecs

USGS_BASEURL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventid='

Conductance <- readRDS("data/out/conductance.rds")
mod_depths <- readRDS("data/out/mod_depths.rds") # sed for pretty plot.

makeUSGCrequestForId <- function (eventid) 
{
    url <- paste(USGS_BASEURL,eventid, sep="")
    resp <- GET(url)
    json <- fromJSON(content(resp, "text"), flatten= TRUE)
}


# Inputs are in plain-Jane lat long coords 
# Our work is in ESPG:3994
reproj4326to3994 <- function (lat, lon)
{
    pt = data.frame(lon = lon, lat = lat) %>% 
        st_as_sf(coords = c("lon", "lat"))
    pt  = st_set_crs(pt, 4326)
    pt = st_transform(pt, 3994)
    c(pt[[1]][[1]][1] ,pt[[1]][[1]][2] ) # not a fan. 
}

eventjson <-makeUSGCrequestForId(KERMADEC_M81)
event_lon = eventjson$geometry$coordinates[1]
event_lat = eventjson$geometry$coordinates[2]

# sea level sensors
# modified so in open ocean (no landfall)
LOTT <- c(-37.5299439,178.175767) # NZ east cape - lottin point
GBIT <- c(-36.1760262,175.508472) # NZ great barrier
NCPT <- c(-34.4245609,173.083354) # NZ North cape

PoI <- LOTT

A <- reproj4326to3994(lon = event_lon, lat = event_lat) # 
B <- reproj4326to3994(lon = PoI[2], lat =  PoI[1]) # lottin point

acc <- accCost(Conductance,A) 
AtoB <- shortestPath(Conductance, A,B, output="SpatialLines")

hrs = calc(acc, function(x) {x/3600})

plot(mod_depths, col= rev(gray.colors(255)), legend.lab="depth (m)", colNA = "palegreen")
contour(hrs, add = TRUE , legend.lab="travel time (hrs)")
lines(AtoB, col = "red")



text(A[1] + 10, A[2] + 10, "EQ", col = "red")
text(B[1] - 10, B[2] + 10, "LOTT", col = "red")