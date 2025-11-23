import os
import json
import re
from datetime import datetime

def extract_artist(filename):
    """Extract artist from filename"""
    name = filename.replace('.mp3', '')
    
    # Known artists
    artists = ['Omar Esa', 'Maher Zain', 'Muhammad al Muqit', 'Muhammad Al Muqit', 
               'Muhammad Al-Muqit', 'Nadeem Mohammed', 'Ahmed Bukhatir', 'Zain Bhikha',
               'Khaled Siddique', 'Labbayk', 'Ahmad Hussain', 'Mishari Rashid Al Afasy',
               'Sami Yusuf', 'Mesut Kurtis', 'Mohammed Alomari', 'Anas Dosari',
               'Kamal Uddin', 'Othman Al Ibrahim', 'Ehsaan Tahmid', 'Ali Gulam',
               'Ishaq Ayubi', 'Yusuf Islam', 'Raid al-Qahtani', 'Seyifunmi']
    
    for artist in artists:
        if artist.lower() in name.lower():
            return artist
    
    # Pattern matching
    if ' by ' in name:
        return name.split(' by ')[-1].split(' - ')[0].strip()
    elif ' - ' in name and not name.startswith(('01.', '02.', '03.')):
        parts = name.split(' - ')
        if len(parts) > 1:
            return parts[0].strip()
    
    return "Unknown"

def categorize(filename):
    """Categorize based on filename"""
    text = filename.lower()
    if any(word in text for word in ['emotional', 'tear', 'sad', 'broken']):
        return "emotional"
    elif any(word in text for word in ['motivational', 'rise', 'happy']):
        return "motivational"
    elif any(word in text for word in ['allah', 'rabbi', 'lord', 'dua']):
        return "supplication"
    elif any(word in text for word in ['prophet', 'nabi', 'muhammad']):
        return "prophet"
    elif any(word in text for word in ['quran', 'surah']):
        return "quran"
    elif any(word in text for word in ['ramadan', 'eid']):
        return "seasonal"
    else:
        return "religious"

def detect_language(filename):
    """Detect language"""
    text = filename.lower()
    if any(word in text for word in ['bangla', 'matir']):
        return "bangla"
    elif any(word in text for word in ['urdu', 'pyaareh', 'kiya']):
        return "urdu"
    elif any(word in text for word in ['arabic', 'ya ', 'al ', 'bil ']):
        return "arabic"
    else:
        return "english"

def clean_title(filename):
    """Clean title"""
    title = filename.replace('.mp3', '')
    title = re.sub(r'^\d+\.\s*', '', title)
    title = re.sub(r'\s*-\s*Official.*?Video', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*by\s+[^-]+', '', title, flags=re.IGNORECASE)
    return title.strip('\'"').strip()

# Generate catalog
files = []
file_id = 1

for filename in os.listdir('/workspace'):
    if filename.endswith('.mp3'):
        title = clean_title(filename)
        artist = extract_artist(filename)
        category = categorize(filename)
        language = detect_language(filename)
        
        files.append({
            "id": file_id,
            "filename": filename,
            "title": title,
            "artist": artist,
            "format": "mp3",
            "path": f"/workspace/{filename}",
            "category": category,
            "language": language,
            "tags": [category, language]
        })
        file_id += 1

# Sort by artist, then title
files.sort(key=lambda x: (x['artist'], x['title']))

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
        "description": "Collection of Islamic vocal music (Nasheeds) for backup purposes",
        "total_files": len(files),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "format": "mp3",
        "base_path": "/workspace",
        "version": "1.0"
    },
    "files": files,
    "indices": {
        "artists": artists,
        "categories": categories,
        "languages": languages
    },
    "api_endpoints": {
        "all_files": "/api/files",
        "by_artist": "/api/files/artist/{artist_name}",
        "by_category": "/api/files/category/{category_name}",
        "by_language": "/api/files/language/{language_code}",
        "search": "/api/files/search?q={query}",
        "file_details": "/api/files/{file_id}"
    }
}

# Write catalog
with open('/workspace/audio_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Generated catalog with {len(files)} files")
print(f"Artists: {len(artists)}")
print(f"Categories: {len(categories)}")
print(f"Languages: {len(languages)}")