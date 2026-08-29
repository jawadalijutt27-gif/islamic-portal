import requests
url = "http://api.alquran.cloud/v1/surah/1/editions/quran-uthmani,ur.jalandhry"
response = requests.get(url).json()

arabic_ayat = response['data'][0]['ayahs']
urdu_ayat = response['data'][1]['ayahs']

print("--- SURAH AL-FATIHA ---\n")

for ar, ur in zip(arabic_ayat, urdu_ayat):
    print(f"Ayat {ar['numberInSurah']}:")
    print(f"Arabic: {ar['text']}")
    print(f"Urdu:   {ur['text']}")
    print("-" * 30)
    