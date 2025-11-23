# Nasheed Collection Audio Catalog

## Overview
This repository contains a comprehensive JSON catalog of all audio files in the Nasheed collection. The catalog is designed to be API-friendly and provides easy access to all audio files with proper organization and metadata.

## Files Created

### 1. `complete_nasheed_catalog.json`
The main comprehensive catalog containing all 100+ audio files with:
- Complete metadata for each file
- Artist information
- Categories and tags
- Language detection
- API endpoint definitions
- Search indices

### 2. `create_full_catalog.py`
Python script that generates the complete catalog automatically by:
- Scanning all MP3 files in the directory
- Extracting artist names using pattern matching
- Categorizing files based on content
- Detecting languages
- Creating search indices
- Generating API-friendly structure

## Catalog Structure

```json
{
  "metadata": {
    "collection_name": "Nasheed Collection",
    "total_files": 100+,
    "format": "mp3",
    "base_path": "/workspace"
  },
  "files": [
    {
      "id": 1,
      "filename": "original_filename.mp3",
      "title": "Clean Title",
      "artist": "Artist Name",
      "format": "mp3",
      "path": "/workspace/filename.mp3",
      "category": "category",
      "language": "language",
      "tags": ["tag1", "tag2"]
    }
  ],
  "indices": {
    "artists": { "Artist Name": [file_ids] },
    "categories": { "category": [file_ids] },
    "languages": { "language": [file_ids] }
  },
  "api_endpoints": {
    "all_files": "/api/files",
    "by_artist": "/api/files/artist/{artist_name}",
    "by_category": "/api/files/category/{category_name}",
    "search": "/api/files/search?q={query}"
  }
}
```

## Categories Used
- **emotional**: Sad, touching, emotional nasheeds
- **motivational**: Inspiring, uplifting content
- **supplication**: Duas and prayers
- **prophet**: About Prophet Muhammad (PBUH)
- **quran**: Quranic recitations
- **seasonal**: Ramadan, Eid related
- **social**: Palestine, Syria, social issues
- **classical**: Traditional Islamic poetry
- **dhikr**: Remembrance of Allah
- **unity**: Community, togetherness
- **religious**: General religious content

## Languages Detected
- **Arabic**: Traditional Islamic language
- **English**: English nasheeds
- **Urdu**: Urdu/Hindi nasheeds
- **Bangla**: Bengali nasheeds

## Major Artists in Collection
- Omar Esa
- Maher Zain
- Muhammad al Muqit
- Nadeem Mohammed
- Ahmed Bukhatir
- Zain Bhikha
- Khaled Siddique
- Labbayk
- And many more...

## API Usage Examples

### Get all files
```
GET /api/files
```

### Get files by artist
```
GET /api/files/artist/Omar%20Esa
```

### Get files by category
```
GET /api/files/category/motivational
```

### Search files
```
GET /api/files/search?q=allah
```

### Get file details
```
GET /api/files/1
```

## File Access
All files can be accessed using their full path:
```
/workspace/filename.mp3
```

## Usage Notes
- This collection is for backup purposes only
- Files should not be distributed or shared
- All files are in MP3 format
- Paths are absolute from the workspace root

## Generation
To regenerate the catalog, run:
```bash
python3 create_full_catalog.py
```

This will scan all MP3 files and create a fresh catalog with updated metadata and indices.