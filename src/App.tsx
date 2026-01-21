import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import CategoriesPage from './pages/CategoriesPage';
import LevelsPage from './pages/LevelsPage';
import CategoryDetailPage from './pages/CategoryDetailPage';
import LevelDetailPage from './pages/LevelDetailPage';

function App() {
  const [lang, setLang] = useState<'ar' | 'en'>(
    (localStorage.getItem('lang') as 'ar' | 'en') || 'ar'
  );

  useEffect(() => {
    localStorage.setItem('lang', lang);
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
  }, [lang]);

  const toggleLang = () => {
    setLang(prev => prev === 'ar' ? 'en' : 'ar');
  };

  return (
    <Router>
      <div className={`min-h-screen bg-gray-50 ${lang === 'ar' ? 'font-arabic' : ''}`}>
        <Navbar lang={lang} toggleLang={toggleLang} />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage lang={lang} />} />
            <Route path="/categories" element={<CategoriesPage lang={lang} />} />
            <Route path="/levels" element={<LevelsPage lang={lang} />} />
            <Route path="/category/:id" element={<CategoryDetailPage lang={lang} />} />
            <Route path="/level/:id" element={<LevelDetailPage lang={lang} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
