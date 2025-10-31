# Mallorca Real Estate Agency Scraper

A Python scraper for collecting real estate agency data from Mallorca using Google Maps Places API.

## Description

This scraper collects contact information and location data for real estate agencies across 10 major locations in Mallorca. It searches in multiple languages (Spanish, English, German) to ensure comprehensive coverage of agencies serving different international markets.

## Features

- Searches 10 major locations across Mallorca
- Multi-language search queries (Spanish, English, German)
- Collects comprehensive agency data:
  - Name
  - Address
  - Phone number
  - Website
  - GPS coordinates (latitude/longitude)
  - Google Place ID
  - Business types
- Automatic deduplication by phone number
- CSV export for easy data processing
- Detailed logging of scraping progress
- Error handling for API failures

## Requirements

- Python 3.7+
- Google Maps API key with Places API enabled

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

3. Add your Google Maps API key to the `.env` file:

```
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

## Getting a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Places API** for your project
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

**Note:** The Places API has usage costs. Check [Google Maps pricing](https://cloud.google.com/maps-platform/pricing) for current rates.

## Usage

Run the scraper:

```bash
python scraper.py
```

The script will:
1. Load your API key from the `.env` file
2. Search for real estate agencies in 10 Mallorca locations
3. Collect and deduplicate agency data
4. Save results to `data/agencies.csv`

## Output

The scraper generates a CSV file at `data/agencies.csv` with the following columns:

- `name` - Agency name
- `address` - Full formatted address
- `phone` - Formatted phone number
- `website` - Website URL (if available)
- `latitude` - GPS latitude
- `longitude` - GPS longitude
- `place_id` - Google Places ID
- `types` - Business category types

## Locations Covered

The scraper searches the following locations in Mallorca:

1. Palma de Mallorca (5km radius)
2. Calvià (5km radius)
3. Manacor (5km radius)
4. Alcúdia (5km radius)
5. Pollença (5km radius)
6. Andratx (5km radius)
7. Sóller (5km radius)
8. Cala d'Or (5km radius)
9. Santa Ponsa (5km radius)
10. Llucmajor (5km radius)

## Search Queries

The scraper uses three language-specific queries for comprehensive coverage:

- `agencia inmobiliaria` (Spanish)
- `real estate agency` (English)
- `immobilienagentur` (German)

## Error Handling

The scraper includes:
- Try/except blocks for API errors
- Detailed error logging
- Graceful handling of missing data fields
- API rate limit awareness

## Limitations

- Google Places API returns up to 20 results per search
- API usage costs apply per request
- Some agencies may not have all data fields (website, phone, etc.)
- Duplicate detection is based on phone numbers only

## License

This project is part of the Riona AI Agent suite and follows the same MIT License.
