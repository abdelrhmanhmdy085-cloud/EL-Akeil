import { Link } from 'react-router-dom';
import { Globe, Utensils } from 'lucide-react';

interface NavbarProps {
  lang: 'ar' | 'en';
  toggleLang: () => void;
}

const Navbar = ({ lang, toggleLang }: NavbarProps) => {
  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-10 h-10 bg-brand-700 rounded-full flex items-center justify-center">
            <Utensils className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold text-brand-900 hidden sm:block">
            {lang === 'ar' ? 'الأكيل' : 'El Akeil'}
          </span>
        </Link>

        <div className="flex items-center gap-6">
          <Link to="/categories" className="text-gray-600 hover:text-brand-700 font-medium">
            {lang === 'ar' ? 'التصنيفات' : 'Categories'}
          </Link>
          <Link to="/levels" className="text-gray-600 hover:text-brand-700 font-medium">
            {lang === 'ar' ? 'المستويات' : 'Levels'}
          </Link>
          <button
            onClick={toggleLang}
            className="flex items-center gap-1 text-gray-600 hover:text-brand-700"
          >
            <Globe size={20} />
            <span>{lang === 'ar' ? 'English' : 'عربي'}</span>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
