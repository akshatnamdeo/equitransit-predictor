import osmium
import sys
from collections import Counter
import datetime
from tqdm import tqdm
import os

class OSMStatsHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMStatsHandler, self).__init__()
        self.num_nodes = 0
        self.num_ways = 0
        self.num_relations = 0
        self.highway_types = Counter()
        self.railway_types = Counter()
        self.public_transport = Counter()
        self.transit_routes = Counter()
        self.transit_stops = 0
        self.subway_stations = 0
        self.bus_stops = 0
        
        # Track area bounds
        self.min_lat = 90.0
        self.max_lat = -90.0
        self.min_lon = 180.0
        self.max_lon = -180.0
        
        # For progress tracking
        self.progress = None
        self.current_element = 0
        self.total_elements = 0

    def node(self, n):
        self.num_nodes += 1
        self._update_progress()
        
        # Update geographic bounds
        if n.location.valid():
            lat = n.location.lat
            lon = n.location.lon
            self.min_lat = min(self.min_lat, lat)
            self.max_lat = max(self.max_lat, lat)
            self.min_lon = min(self.min_lon, lon)
            self.max_lon = max(self.max_lon, lon)
        
        # Count transport-related nodes
        tags = {tag.k: tag.v for tag in n.tags}
        if 'public_transport' in tags:
            self.public_transport[tags['public_transport']] += 1
            if tags.get('public_transport') == 'stop_position':
                self.transit_stops += 1
        
        if tags.get('highway') == 'bus_stop':
            self.bus_stops += 1
            
        if tags.get('railway') == 'station':
            if tags.get('subway') == 'yes' or 'subway' in tags.get('network', '').lower():
                self.subway_stations += 1

    def way(self, w):
        self.num_ways += 1
        self._update_progress()
        
        tags = {tag.k: tag.v for tag in w.tags}
        
        if 'highway' in tags:
            self.highway_types[tags['highway']] += 1
            
        if 'railway' in tags:
            self.railway_types[tags['railway']] += 1

    def relation(self, r):
        self.num_relations += 1
        self._update_progress()
        
        tags = {tag.k: tag.v for tag in r.tags}
        
        if tags.get('type') == 'route':
            if 'route' in tags:
                self.transit_routes[tags['route']] += 1
    
    def _update_progress(self):
        """Update the progress bar."""
        if self.progress is not None:
            self.current_element += 1
            if self.current_element % 10000 == 0:  # Update every 10000 elements to avoid slowdown
                self.progress.update(10000)
                self.progress.set_description(f"Nodes: {self.num_nodes:,} | Ways: {self.num_ways:,} | Relations: {self.num_relations:,}")
    
    def set_progress_bar(self, total_estimate):
        """Initialize the progress bar with estimated total elements."""
        self.total_elements = total_estimate
        self.progress = tqdm(total=total_estimate, unit='elements')
        self.progress.set_description("Processing OSM data")

def estimate_elements(pbf_file):
    """Estimate the number of elements in the file based on file size."""
    file_size = os.path.getsize(pbf_file)
    # Rough estimate: ~1 million elements per 50MB
    estimated_elements = int(file_size / 50000000 * 1000000)
    return max(estimated_elements, 1000000)  # At least 1 million to be safe

def main(pbf_file):
    print(f"Starting analysis of {pbf_file}...")
    print(f"Time started: {datetime.datetime.now()}")
    
    # Create handler
    handler = OSMStatsHandler()
    
    # Estimate total elements for progress bar
    total_estimate = estimate_elements(pbf_file)
    print(f"Estimated elements to process: ~{total_estimate:,}")
    handler.set_progress_bar(total_estimate)
    
    # Process the file
    try:
        handler.apply_file(pbf_file)
        if handler.progress:
            handler.progress.close()
    except Exception as e:
        print(f"Error processing file: {e}")
        if handler.progress:
            handler.progress.close()
        return
    
    # Basic stats
    print("\n=== Basic Statistics ===")
    print(f"Nodes: {handler.num_nodes:,}")
    print(f"Ways: {handler.num_ways:,}")
    print(f"Relations: {handler.num_relations:,}")
    
    # Geographic bounds
    print("\n=== Geographic Boundaries ===")
    print(f"Latitude range: {handler.min_lat:.6f} to {handler.max_lat:.6f}")
    print(f"Longitude range: {handler.min_lon:.6f} to {handler.max_lon:.6f}")
    
    # Check if this matches New York State's approximate boundaries
    ny_bounds = {
        'min_lat': 40.5, 'max_lat': 45.0,
        'min_lon': -80.0, 'max_lon': -72.0
    }
    
    if (handler.min_lat > ny_bounds['min_lat'] and handler.max_lat < ny_bounds['max_lat'] and
        handler.min_lon > ny_bounds['min_lon'] and handler.max_lon < ny_bounds['max_lon']):
        print("✓ Geographic boundaries are consistent with New York State")
    else:
        print("⚠ Geographic boundaries may not match New York State")
    
    # Transit infrastructure
    print("\n=== Transit Infrastructure ===")
    print(f"Bus stops: {handler.bus_stops:,}")
    print(f"Subway stations: {handler.subway_stations:,}")
    print(f"Total transit stops: {handler.transit_stops:,}")
    
    print("\n=== Top 10 Highway Types ===")
    for highway, count in handler.highway_types.most_common(10):
        print(f"{highway}: {count:,}")
    
    print("\n=== Railway Types ===")
    for railway, count in handler.railway_types.most_common():
        print(f"{railway}: {count:,}")
    
    print("\n=== Public Transport Types ===")
    for pt, count in handler.public_transport.most_common():
        print(f"{pt}: {count:,}")
    
    print("\n=== Transit Routes ===")
    for route, count in handler.transit_routes.most_common():
        print(f"{route}: {count:,}")
    
    # Project relevance check
    print("\n=== Relevance for MTA Project ===")
    if handler.subway_stations > 0 and handler.bus_stops > 0:
        print("✓ File contains subway stations and bus stops")
        print("✓ This appears to be a suitable OSM file for your MTA transit project")
    else:
        print("⚠ Warning: File may not contain sufficient transit information")
    
    print(f"\nAnalysis completed at {datetime.datetime.now()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_osm.py new-york-latest.osm.pbf")
        sys.exit(1)
    
    main(sys.argv[1])