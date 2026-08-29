from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import requests

app = Flask(__name__)

# Surah list cache
SURAH_LIST = []
try:
    res = requests.get("https://api.alquran.cloud/v1/surah", timeout=10).json()
    SURAH_LIST = res['data']
except Exception as e:
    print("Surah list fetch error:", e)

# Popular Authentic Reciters
RECITERS = [
    {"id": "ar.alafasy", "name": "Mishary Rashid Alafasy"},
    {"id": "ar.abdulbasitmurattal", "name": "Abdul Basit (Murattal)"},
    {"id": "ar.abdurrahmaansudais", "name": "Abdur-Rahman As-Sudais"},
    {"id": "ar.husary", "name": "Mahmoud Khalil Al-Husary"},
    {"id": "ar.minshawi", "name": "Mohamed Siddiq Al-Minshawi"}
]

# Famous Global Translations for Quran
QURAN_TRANSLATIONS = [
    {"id": "ur.jalandhry", "name": "اردو - فتح محمد جالندھری", "lang": "ur", "dir": "rtl"},
    {"id": "ur.kanzuliman", "name": "اردو - احمد رضا خان (کنز الایمان)", "lang": "ur", "dir": "rtl"},
    {"id": "ur.maududi", "name": "اردو - ابوالاعلیٰ مودودی", "lang": "ur", "dir": "rtl"},
    {"id": "ur.junagarhi", "name": "اردو - محمد جوناگڑھی", "lang": "ur", "dir": "rtl"},
    {"id": "ur.qadri", "name": "اردو - طاہر القادری", "lang": "ur", "dir": "rtl"},
    {"id": "en.sahih", "name": "English - Saheeh International", "lang": "en", "dir": "ltr"},
    {"id": "hi.hindi", "name": "हिन्दी (Hindi) - फ़ارूक़ ख़ان", "lang": "hi", "dir": "ltr"},
    {"id": "bn.bengali", "name": "বাংলা (Bengali) - মুহিউদ্দীন خان", "lang": "bn", "dir": "ltr"},
    {"id": "sd.amroti", "name": "سنڌي (Sindhi) - امروٽي", "lang": "sd", "dir": "rtl"},
    {"id": "ps.abdulwali", "name": "پښتو (Pashto) - عبد الولي", "lang": "ps", "dir": "rtl"},
    {"id": "fa.ansarian", "name": "فارسی (Persian) - انصاریان", "lang": "fa", "dir": "rtl"},
    {"id": "tr.diyanet", "name": "Türkçe (Turkish) - Diyanet", "lang": "tr", "dir": "ltr"},
    {"id": "id.indonesian", "name": "Bahasa Indonesia", "lang": "id", "dir": "ltr"},
    {"id": "fr.hamidullah", "name": "Français (French) - Hamidullah", "lang": "fr", "dir": "ltr"},
    {"id": "es.cortes", "name": "Español (Spanish) - Cortes", "lang": "es", "dir": "ltr"},
    {"id": "de.aburida", "name": "Deutsch (German) - Abu Rida", "lang": "de", "dir": "ltr"},
    {"id": "ru.kuliev", "name": "Русский (Russian) - Кулиев", "lang": "ru", "dir": "ltr"},
    {"id": "zh.jian", "name": "中文 (Chinese) - Ma Jian", "lang": "zh", "dir": "ltr"}
]

# Authentic Hadith Books List
HADITH_BOOKS = [
    {"id": "bukhari", "name": "صحیح بخاری (Sahih Bukhari)", "total": 7563},
    {"id": "muslim", "name": "صحیح مسلم (Sahih Muslim)", "total": 7500},
    {"id": "abudawud", "name": "سنن ابی داؤد (Sunan Abi Dawud)", "total": 5274},
    {"id": "tirmidhi", "name": "جامع ترمذی (Jami at-Tirmidhi)", "total": 3956},
    {"id": "nasai", "name": "سنن نسائی (Sunan an-Nasa'i)", "total": 5758},
    {"id": "ibnmajah", "name": "سنن ابن ماجہ (Sunan Ibn Majah)", "total": 4341}
]

# Hadith Languages
HADITH_LANGUAGES = [
    {"code": "urd", "name": "اردو (Urdu)", "dir": "rtl"},
    {"code": "eng", "name": "English", "dir": "ltr"},
    {"code": "ben", "name": "বাংলা (Bengali)", "dir": "ltr"},
    {"code": "ind", "name": "Bahasa Indonesia", "dir": "ltr"},
    {"code": "tur", "name": "Türkçe (Turkish)", "dir": "ltr"},
    {"code": "fra", "name": "Français (French)", "dir": "ltr"},
    {"code": "rus", "name": "Русский (Russian)", "dir": "ltr"}
]

BISMILLAH_PREFIX = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"

@app.route('/')
def home():
    return redirect(url_for('view_surah', surah_id=1))

@app.route('/surah/<int:surah_id>')
def view_surah(surah_id):
    if surah_id < 1 or surah_id > 114:
        surah_id = 1

    reciter_id = request.args.get('reciter', 'ar.alafasy')
    valid_reciters = [r['id'] for r in RECITERS]
    if reciter_id not in valid_reciters:
        reciter_id = 'ar.alafasy'

    translation_id = request.args.get('translation', 'ur.jalandhry')
    selected_trans = next((t for t in QURAN_TRANSLATIONS if t['id'] == translation_id), QURAN_TRANSLATIONS[0])

    url = f"https://api.alquran.cloud/v1/surah/{surah_id}/editions/quran-uthmani,{selected_trans['id']},{reciter_id}"
    response = requests.get(url, timeout=15).json()
    
    surah_info = response['data'][0]
    arabic_ayahs = response['data'][0]['ayahs']
    trans_ayahs = response['data'][1]['ayahs']
    audio_ayahs = response['data'][2]['ayahs']
    
    surah_data = []
    for ar, tr, au in zip(arabic_ayahs, trans_ayahs, audio_ayahs):
        arabic_text = ar['text']
        if surah_id != 1 and ar['numberInSurah'] == 1:
            if arabic_text.startswith(BISMILLAH_PREFIX):
                arabic_text = arabic_text[len(BISMILLAH_PREFIX):].strip()

        surah_data.append({
            "number": ar['numberInSurah'],
            "arabic": arabic_text,
            "translation": tr['text'],
            "audio": au['audio']
        })
        
    return render_template(
        'index.html', 
        surah_data=surah_data, 
        surah_info=surah_info, 
        all_surahs=SURAH_LIST, 
        current_surah=surah_id,
        reciters=RECITERS,
        current_reciter=reciter_id,
        translations=QURAN_TRANSLATIONS,
        current_translation=selected_trans
    )

# Dedicated Favorites Section Route
@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

# Hadith Section Route
@app.route('/hadith')
@app.route('/hadith/<book_id>')
def view_hadith(book_id='bukhari'):
    page = request.args.get('page', 1, type=int)
    lang_code = request.args.get('lang', 'urd')
    limit = 20
    start_num = (page - 1) * limit + 1
    end_num = start_num + limit

    valid_book_ids = [b['id'] for b in HADITH_BOOKS]
    if book_id not in valid_book_ids:
        book_id = 'bukhari'

    valid_langs = [l['code'] for l in HADITH_LANGUAGES]
    if lang_code not in valid_langs:
        lang_code = 'urd'

    current_book = next(b for b in HADITH_BOOKS if b['id'] == book_id)
    current_lang = next(l for l in HADITH_LANGUAGES if l['code'] == lang_code)
    
    hadiths = []
    try:
        url_trans = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{lang_code}-{book_id}.json"
        res_trans = requests.get(url_trans, timeout=12).json()
        raw_list_trans = res_trans.get('hadiths', [])[start_num - 1 : end_num - 1]
        
        url_ar = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{book_id}.json"
        res_ar = requests.get(url_ar, timeout=12).json()
        raw_list_ar = res_ar.get('hadiths', [])[start_num - 1 : end_num - 1]

        for idx, (tr, ar) in enumerate(zip(raw_list_trans, raw_list_ar)):
            grades = ar.get('grades', [])
            status = "صحیح (Sahih)" if book_id in ['bukhari', 'muslim'] else "موثق / حسن"
            if grades and len(grades) > 0:
                grade_name = grades[0].get('grade', '')
                if grade_name:
                    status = grade_name

            hadiths.append({
                "intl_number": ar.get('hadithnumber', start_num + idx),
                "arabic": ar.get('text', ''),
                "translation": tr.get('text', ''),
                "status": status
            })
    except Exception as e:
        print("Hadith fetch error:", e)

    return render_template(
        'hadith.html',
        books=HADITH_BOOKS,
        current_book=current_book,
        languages=HADITH_LANGUAGES,
        current_lang=current_lang,
        hadiths=hadiths,
        page=page
    )

# PWA Routes
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')
@app.route('/favorites')
def favorites_page():
    return render_template('favourite.html')

if __name__ == '__main__':
    app.run(debug=True)