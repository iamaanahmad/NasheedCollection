#!/usr/bin/python3

import os
import json
import re
from datetime import datetime

# Get all MP3 files
mp3_files = [f for f in os.listdir('/workspace') if f.endswith('.mp3')]

def extract_artist(filename):
    """Extract artist from filename"""
    name = filename.replace('.mp3', '')
    
    # Known artists mapping
    artist_map = {
        'omar esa': 'Omar Esa',
        'maher zain': 'Maher Zain', 
        'muhammad al muqit': 'Muhammad al Muqit',
        'muhammad al-muqit': 'Muhammad al Muqit',
        'nadeem mohammed': 'Nadeem Mohammed',
        'ahmed bukhatir': 'Ahmed Bukhatir',
        'zain bhikha': 'Zain Bhikha',
        'khaled siddique': 'Khaled Siddique',
        'labbayk': 'Labbayk',
        'ahmad hussain': 'Ahmad Hussain',
        'mishari rashid al afasy': 'Mishari Rashid Al Afasy',
        'sami yusuf': 'Sami Yusuf',
        'mesut kurtis': 'Mesut Kurtis',
        'mohammed alomari': 'Mohammed Alomari',
        'anas dosari': 'Anas Dosari',
        'kamal uddin': 'Kamal Uddin',
        'othman al ibrahim': 'Othman Al Ibrahim',
        'ehsaan tahmid': 'Ehsaan Tahmid',
        'ali gulam': 'Ali Gulam',
        'ishaq ayubi': 'Ishaq Ayubi',
        'yusuf islam': 'Yusuf Islam',
        'raid al-qahtani': 'Raid al-Qahtani',
        'seyifunmi': 'Seyifunmi'
    }
    
    name_lower = name.lower()
    for key, value in artist_map.items():
        if key in name_lower:
            return value
    
    # Pattern matching for "by Artist" or "Artist -"
    if ' by ' in name:
        artist = name.split(' by ')[-1].split(' - ')[0].strip()
        return artist if len(artist) > 2 else "Unknown"
    elif ' - ' in name and not name.startswith(('01.', '02.', '03.', '04.', '05.', '06.', '07.', '08.', '09.', '10.', '11.')):
        artist = name.split(' - ')[0].strip()
        return artist if len(artist) > 2 else "Unknown"
    
    return "Unknown"

def categorize(filename):
    """Categorize based on filename"""
    text = filename.lower()
    if any(word in text for word in ['emotional', 'tear', 'sad', 'broken', 'longing']):
        return "emotional"
    elif any(word in text for word in ['motivational', 'rise', 'happy', 'guidance', 'resistant']):
        return "motivational"
    elif any(word in text for word in ['allah', 'rabbi', 'lord', 'dua', 'prayer', 'my hope']):
        return "supplication"
    elif any(word in text for word in ['prophet', 'nabi', 'muhammad', 'mustafa', 'messenger']):
        return "prophet"
    elif any(word in text for word in ['quran', 'surah', 'fatiha']):
        return "quran"
    elif any(word in text for word in ['ramadan', 'eid', 'hajj']):
        return "seasonal"
    elif any(word in text for word in ['palestine', 'syria', 'social']):
        return "social"
    elif any(word in text for word in ['burdah', 'classical', 'qasidah']):
        return "classical"
    elif any(word in text for word in ['dhikr', 'remembrance', 'allahu', 'subhan']):
        return "dhikr"
    elif any(word in text for word in ['unity', 'together', 'community']):
        return "unity"
    else:
        return "religious"

def detect_language(filename):
    """Detect language"""
    text = filename.lower()
    if any(word in text for word in ['bangla', 'matir', 'sharey']):
        return "bangla"
    elif any(word in text for word in ['urdu', 'pyaareh', 'kiya', 'tera']):
        return "urdu"
    elif any(word in text for word in ['arabic', 'ya ', 'al ', 'bil ', 'rahman', 'mawlaya']):
        return "arabic"
    else:
        return "english"

def clean_title(filename):
    """Clean title from filename"""
    title = filename.replace('.mp3', '')
    title = re.sub(r'^\d+\.\s*', '', title)  # Remove track numbers
    title = re.sub(r'\s*-\s*Official.*?Video', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\(Official.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*by\s+[^-]+$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*-\s*[^-]*Nasheed$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*feat\..*', '', title, flags=re.IGNORECASE)
    return title.strip('\'"').strip()

# Generate file entries
files = []
for i, filename in enumerate(sorted(mp3_files), 1):
    title = clean_title(filename)
    artist = extract_artist(filename)
    category = categorize(filename)
    language = detect_language(filename)
    
    files.append({
        "id": i,
        "filename": filename,
        "title": title,
        "artist": artist,
        "format": "mp3",
        "path": f"/workspace/{filename}",
        "category": category,
        "language": language,
        "tags": [category, language, artist.lower().replace(' ', '_')]
    })

# Create indices
artists = {}
categories = {}
languages = {}

for file_entry in files:
    # Artists index
    artist = file_entry['artist']
    if artist not in artists:
        artists[artist] = []
    artists[artist].append(file_entry['id'])
    
    # Categories index
    category = file_entry['category']
    if category not in categories:
        categories[category] = []
    categories[category].append(file_entry['id'])
    
    # Languages index
    language = file_entry['language']
    if language not in languages:
        languages[language] = []
    languages[language].append(file_entry['id'])

# Create complete catalog
catalog = {
    "metadata": {
        "collection_name": "Nasheed Collection",
        "description": "Complete collection of Islamic vocal music (Nasheeds) for backup purposes",
        "total_files": len(files),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "format": "mp3",
        "base_path": "/workspace",
        "version": "2.0",
        "created_by": "Audio Catalog Generator"
    },
    "collection_info": {
        "purpose": "Backup and archival of Nasheed collection",
        "usage": "Personal use only - not for distribution",
        "file_format": "MP3 audio files",
        "total_artists": len(artists),
        "total_categories": len(categories),
        "total_languages": len(languages)
    },
    "files": files,
    "indices": {
        "artists": artists,
        "categories": categories,
        "languages": languages
    },
    "api_endpoints": {
        "description": "RESTful API endpoints for accessing the audio collection",
        "base_url": "https://api.nasheed-collection.com",
        "endpoints": {
            "all_files": {
                "method": "GET",
                "url": "/api/files",
                "description": "Get all audio files"
            },
            "by_artist": {
                "method": "GET", 
                "url": "/api/files/artist/{artist_name}",
                "description": "Get files by specific artist",
                "example": "/api/files/artist/Omar%20Esa"
            },
            "by_category": {
                "method": "GET",
                "url": "/api/files/category/{category_name}",
                "description": "Get files by category",
                "example": "/api/files/category/motivational"
            },
            "by_language": {
                "method": "GET",
                "url": "/api/files/language/{language_code}",
                "description": "Get files by language",
                "example": "/api/files/language/arabic"
            },
            "search": {
                "method": "GET",
                "url": "/api/files/search?q={query}",
                "description": "Search files by title, artist, or tags",
                "example": "/api/files/search?q=allah"
            },
            "file_details": {
                "method": "GET",
                "url": "/api/files/{file_id}",
                "description": "Get detailed information about a specific file",
                "example": "/api/files/1"
            },
            "download": {
                "method": "GET",
                "url": "/api/files/{file_id}/download",
                "description": "Download audio file",
                "example": "/api/files/1/download"
            }
        }
    },
    "statistics": {
        "most_common_artist": max(artists.items(), key=lambda x: len(x[1]))[0],
        "most_common_category": max(categories.items(), key=lambda x: len(x[1]))[0],
        "most_common_language": max(languages.items(), key=lambda x: len(x[1]))[0]
    }
}

# Write to file
with open('/workspace/complete_nasheed_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"✅ Generated complete catalog with {len(files)} files")
print(f"📊 Statistics:")
print(f"   - Artists: {len(artists)}")
print(f"   - Categories: {len(categories)}")
print(f"   - Languages: {len(languages)}")
print(f"   - Most files by: {catalog['statistics']['most_common_artist']}")
print(f"   - Most common category: {catalog['statistics']['most_common_category']}")
print(f"   - Most common language: {catalog['statistics']['most_common_language']}")
print(f"📁 Catalog saved as: complete_nasheed_catalog.json")