const LANG_KEY = 'elakeil_lang';
const DEFAULT_LANG = 'ar';
const SUPPORTED_LANGS = ['ar', 'en', 'fr', 'de', 'es', 'it', 'tr', 'ru', 'zh'];
const translations = {};

async function loadLanguage(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) lang = DEFAULT_LANG;
    localStorage.setItem(LANG_KEY, lang);

    // Set RTL/LTR
    const direction = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.dir = direction;
    document.documentElement.lang = lang;
    document.body.className = direction;

    // Load JSON
    try {
        if (!translations[lang]) {
            const url = `assets/lang/${lang}.json?t=${Date.now()}`;
            console.log(`Fetching translations from: ${url}`);
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const jsonData = await res.json();
            console.log(`Fetched JSON data for ${lang}:`, jsonData);
            translations[lang] = jsonData;
            console.log(`Language loaded: ${lang}, keys:`, Object.keys(translations[lang]).length);
        }
        applyTranslations(lang);
    } catch (e) {
        console.error('Failed to load language:', lang, e);
    }
}

function applyTranslations(lang) {
    const t = translations[lang];
    if (!t) {
        console.warn('Translations not loaded for language:', lang);
        return;
    }

    console.log(`Applying translations for ${lang}. Elements with data-i18n:`, document.querySelectorAll('[data-i18n]').length);

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            console.log(`Translating ${key}: "${el.textContent}" -> "${t[key]}"`);
            el.textContent = t[key];
        } else {
            console.warn(`Missing translation key: ${key}`);
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (t[key]) el.placeholder = t[key];
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (t[key]) el.title = t[key];
    });

    document.querySelectorAll('[data-i18n-aria-label]').forEach(el => {
        const key = el.getAttribute('data-i18n-aria-label');
        if (t[key]) el.setAttribute('aria-label', t[key]);
    });
}

function initLanguage() {
    let saved = localStorage.getItem(LANG_KEY);
    if (!saved) {
        // Auto-detect
        const browserLang = navigator.language.split('-')[0];
        saved = SUPPORTED_LANGS.includes(browserLang) ? browserLang : DEFAULT_LANG;
    }

    const nav = document.getElementById('langControls');
    if (nav) {
        nav.innerHTML = `
            <button type="button" class="lang-toggle-btn" onclick="toggleLanguage()"
                    data-i18n-title="lang_toggle_label" data-i18n-aria-label="lang_toggle_label">
                🌍 <span id="lang-label">${saved === 'ar' ? 'EN' : 'AR'}</span>
            </button>
        `;
    }
    
    // Wait for DOM to be fully ready before loading language
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => loadLanguage(saved));
    } else {
        loadLanguage(saved);
    }
}

function toggleLanguage() {
    const current = localStorage.getItem(LANG_KEY) || DEFAULT_LANG;
    // Toggle logic: If Ar -> En, else -> Ar
    const next = current === 'ar' ? 'en' : 'ar';

    // Update label to show the OTHER option
    const label = document.getElementById('lang-label');
    if (label) label.innerText = next === 'ar' ? 'EN' : 'AR';

    console.log(`Switching language from ${current} to ${next}`);
    loadLanguage(next);
}

document.addEventListener('DOMContentLoaded', initLanguage);
