#!/usr/bin/env python3
"""
Mallorca Real Estate Agency Scraper
Collects real estate agency data from Mallorca using Google Maps Places API
"""

import os
import logging
import googlemaps
import pandas as pd
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Mallorca locations with coordinates
LOCATIONS = [
    {"name": "Palma de Mallorca", "lat": 39.5696, "lng": 2.6502, "radius": 5000},
    {"name": "Calvià", "lat": 39.5569, "lng": 2.5039, "radius": 5000},
    {"name": "Manacor", "lat": 39.5696, "lng": 3.2096, "radius": 5000},
    {"name": "Alcúdia", "lat": 39.8544, "lng": 3.1214, "radius": 5000},
    {"name": "Pollença", "lat": 39.8766, "lng": 3.0149, "radius": 5000},
    {"name": "Andratx", "lat": 39.5761, "lng": 2.4237, "radius": 5000},
    {"name": "Sóller", "lat": 39.7653, "lng": 2.7147, "radius": 5000},
    {"name": "Cala d'Or", "lat": 39.3755, "lng": 3.2293, "radius": 5000},
    {"name": "Santa Ponsa", "lat": 39.5189, "lng": 2.4708, "radius": 5000},
    {"name": "Llucmajor", "lat": 39.4931, "lng": 2.8853, "radius": 5000},
]

# Search queries in different languages
QUERIES = [
    "agencia inmobiliaria",      # Spanish
    "real estate agency",         # English
    "immobilienagentur"          # German
]


def extract_place_data(place):
    """Extract relevant data from a place result"""
    return {
        'name': place.get('name', ''),
        'address': place.get('formatted_address', ''),
        'phone': place.get('formatted_phone_number', ''),
        'website': place.get('website', ''),
        'latitude': place.get('geometry', {}).get('location', {}).get('lat', ''),
        'longitude': place.get('geometry', {}).get('location', {}).get('lng', ''),
        'place_id': place.get('place_id', ''),
        'types': ', '.join(place.get('types', []))
    }


def search_agencies(api_key):
    """Search for real estate agencies in Mallorca"""
    gmaps = googlemaps.Client(key=api_key)
    all_agencies = []

    for location in LOCATIONS:
        logger.info(f"Searching in {location['name']}...")

        for query in QUERIES:
            try:
                # Perform nearby search
                results = gmaps.places_nearby(
                    location=(location['lat'], location['lng']),
                    radius=location['radius'],
                    keyword=query,
                    type='real_estate_agency'
                )

                # Process results
                for place in results.get('results', []):
                    # Get detailed information
                    place_details = gmaps.place(place['place_id'], fields=[
                        'name', 'formatted_address', 'formatted_phone_number',
                        'website', 'geometry', 'place_id', 'types'
                    ])

                    agency_data = extract_place_data(place_details.get('result', {}))
                    all_agencies.append(agency_data)

                logger.info(f"  Found {len(results.get('results', []))} results for '{query}'")

            except googlemaps.exceptions.ApiError as e:
                logger.error(f"API error for {location['name']} - {query}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error for {location['name']} - {query}: {e}")

    return all_agencies


def main():
    """Main execution function"""
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        logger.error("GOOGLE_MAPS_API_KEY not found in environment variables")
        return

    logger.info("Starting Mallorca real estate agency scraper...")

    # Search for agencies
    agencies = search_agencies(api_key)

    if not agencies:
        logger.warning("No agencies found")
        return

    # Convert to DataFrame
    df = pd.DataFrame(agencies)
    logger.info(f"Total results collected: {len(df)}")

    # Remove duplicates by phone number
    df_deduped = df.drop_duplicates(subset=['phone'], keep='first')
    logger.info(f"After deduplication: {len(df_deduped)} unique agencies")

    # Save to CSV
    output_path = 'data/agencies.csv'
    df_deduped.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
