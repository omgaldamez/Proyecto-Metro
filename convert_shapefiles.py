#!/usr/bin/env python3
import shapefile
import json

def shapefile_to_geojson(shapefile_path):
    """Convert shapefile to GeoJSON FeatureCollection"""
    sf = shapefile.Reader(shapefile_path)
    shapes = sf.shapes()
    
    features = []
    for shape in shapes:
        if shape.shapeType == 5:  # Polygon
            # Build coordinates
            coords = []
            if len(shape.parts) == 0:
                coords = [[(x, y) for x, y in shape.points]]
            else:
                for i, start_idx in enumerate(shape.parts):
                    end_idx = shape.parts[i + 1] if i + 1 < len(shape.parts) else len(shape.points)
                    ring = [(x, y) for x, y in shape.points[start_idx:end_idx]]
                    coords.append(ring)
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": coords
                },
                "properties": {}
            }
            features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

# Convert manzanas
print("Converting poligono_manzanas_cdmx...")
manzanas = shapefile_to_geojson('/Users/monicadamazo/Documents/CENTRO/Proyecto final/Proyecto-Metro/Mapa/poligono_manzanas_cdmx/poligono_manzanas_cdmx')
print(f"  → {len(manzanas['features'])} features")

# Convert 15mun (municipios Edomex)
print("Converting 15mun...")
mun15 = shapefile_to_geojson('/Users/monicadamazo/Documents/CENTRO/Proyecto final/Proyecto-Metro/Mapa/Edo de Mex/conjunto_de_datos/cgu_cce2014_denue_012015_mex/15mun')
print(f"  → {len(mun15['features'])} features")

# Output as JS constants
manzanas_json = json.dumps(manzanas)
mun15_json = json.dumps(mun15)

output = """
// ═══════ BASEMAP DATA - MANZANAS (CDMX) ═══════
const BASEMAP_MANZANAS=""" + manzanas_json + """;

// ═══════ BASEMAP DATA - MUNICIPIOS EDOMEX (15MUN) ═══════
const BASEMAP_MUN15=""" + mun15_json + """;
"""

with open('/Users/monicadamazo/Documents/CENTRO/Proyecto final/Proyecto-Metro/basemap_data.js', 'w') as f:
    f.write(output)

print("\n✓ Generated basemap_data.js")
print(f"  BASEMAP_MANZANAS: {len(manzanas['features'])} features")
print(f"  BASEMAP_MUN15: {len(mun15['features'])} features")
