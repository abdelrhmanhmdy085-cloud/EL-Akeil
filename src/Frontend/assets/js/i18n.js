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
            const res = await fetch(`assets/lang/${lang}.json`);
            translations[lang] = await res.json();
        }
        applyTranslations(lang);
    } catch (e) {
        console.error('Failed to load language:', e);
    }
}

function applyTranslations(lang) {
    const t = translations[lang];
    if (!t) return;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) el.innerText = t[key];
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (t[key]) el.placeholder = t[key];
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
            <div class="lang-toggle-btn" onclick="toggleLanguage()" title="Switch Language">
                🌍 <span id="lang-label">${saved === 'ar' ? 'EN' : 'AR'}</span>
            </div>
        `;
    }
    loadLanguage(saved);
}

function toggleLanguage() {
    const current = localStorage.getItem(LANG_KEY) || DEFAULT_LANG;
    // Toggle logic: If Ar -> En, else -> Ar
    const next = current === 'ar' ? 'en' : 'ar';

    // Update label to show the OTHER option
    const label = document.getElementById('lang-label');
    if (label) label.innerText = next === 'ar' ? 'EN' : 'AR';

    loadLanguage(next);
}

document.addEventListener('DOMContentLoaded', initLanguage);
