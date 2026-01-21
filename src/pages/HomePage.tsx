import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ChevronRight, Sparkles } from 'lucide-react';
import logo from '../assets/El Akil.png';

const API_URL = 'http://localhost:5000/api';

const HomePage = ({ lang }: { lang: 'ar' | 'en' }) => {
  const [categories, setCategories] = useState<any[]>([]);
  const [levels, setLevels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [catsRes, levelsRes] = await Promise.all([
          axios.get(`${API_URL}/categories`),
          axios.get(`${API_URL}/levels`)
        ]);
        setCategories(catsRes.data);
        setLevels(levelsRes.data);
      } catch (err) {
        console.error("Error fetching data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="text-center py-20">Loading...</div>;

  const occasionsLevel = levels.find(l => l.name_en === 'Occasions & Holidays');
  const normalLevels = levels.filter(l => l.name_en !== 'Occasions & Holidays');

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="bg-brand-900 rounded-3xl p-8 md:p-12 text-white relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            {lang === 'ar' ? 'أكل بيتي على أصوله' : 'Authentic Homemade Food'}
          </h1>
          <p className="text-brand-100 text-lg mb-8">
            {lang === 'ar'
              ? 'استمتع بأشهى المأكولات المحضرة بكل حب من أمهر الشيفات في منطقتك.'
              : 'Enjoy the most delicious meals prepared with love by the most skilled chefs in your area.'}
          </p>
          <button className="bg-white text-brand-900 px-8 py-3 rounded-full font-bold hover:bg-brand-50 transition-colors">
            {lang === 'ar' ? 'اكتشف المنيو' : 'Explore Menu'}
          </button>
        </div>
        <div className="absolute right-0 bottom-0 opacity-20 transform translate-x-1/4 translate-y-1/4">
          <img src={logo} alt="Logo" className="w-96" />
        </div>
      </section>

      {/* Browse by Level - Horizontal Scroll */}
      <section>
        <div className="flex justify-between items-end mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {lang === 'ar' ? 'اختر مستوى الأكل' : 'Browse by Level'}
            </h2>
            <p className="text-gray-500">
              {lang === 'ar' ? 'من السريع للمميز، كله عندنا' : 'From fast to specialty, we have it all'}
            </p>
          </div>
          <Link to="/levels" className="text-brand-700 font-semibold flex items-center gap-1 hover:underline">
            {lang === 'ar' ? 'عرض الكل' : 'View All'}
            <ChevronRight size={20} className={lang === 'ar' ? 'rotate-180' : ''} />
          </Link>
        </div>
        <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
          {normalLevels.map((level) => (
            <Link
              key={level.id}
              to={`/level/${level.id}`}
              className="flex-shrink-0 w-48 h-32 rounded-2xl p-4 flex flex-col justify-between relative overflow-hidden group border border-gray-100 shadow-sm hover:shadow-md transition-shadow bg-white"
            >
              <span className="font-bold text-lg relative z-10">
                {lang === 'ar' ? level.name_ar : level.name_en}
              </span>
              <div className="w-12 h-1 bg-brand-600 rounded-full group-hover:w-20 transition-all"></div>
              <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:opacity-10 transition-opacity">
                 <Utensils size={80} />
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Browse by Category - Grid */}
      <section>
        <div className="flex justify-between items-end mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {lang === 'ar' ? 'نوع الأكل' : 'Browse by Category'}
            </h2>
            <p className="text-gray-500">
              {lang === 'ar' ? 'كل اللي نفسك فيه هتلاقيه' : 'Whatever you crave, you will find'}
            </p>
          </div>
          <Link to="/categories" className="text-brand-700 font-semibold flex items-center gap-1 hover:underline">
            {lang === 'ar' ? 'عرض الكل' : 'View All'}
            <ChevronRight size={20} className={lang === 'ar' ? 'rotate-180' : ''} />
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {categories.map((category) => (
            <Link
              key={category.id}
              to={`/category/${category.id}`}
              className="bg-white p-6 rounded-2xl text-center border border-gray-100 hover:border-brand-200 hover:shadow-md transition-all group"
            >
              <div className="text-4xl mb-3 transform group-hover:scale-110 transition-transform">
                {category.icon}
              </div>
              <h3 className="font-bold text-gray-800">
                {lang === 'ar' ? category.name_ar : category.name_en}
              </h3>
            </Link>
          ))}
        </div>
      </section>

      {/* Occasions & Holidays - Special Highlight */}
      {occasionsLevel && (
        <section className="bg-gradient-to-r from-purple-700 to-indigo-800 rounded-3xl p-8 text-white">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="flex-1 space-y-4 text-center md:text-start">
              <div className="inline-flex items-center gap-2 bg-white/20 px-4 py-1 rounded-full text-sm font-semibold backdrop-blur-sm">
                <Sparkles size={16} />
                {lang === 'ar' ? 'خاص وحصري' : 'Special & Exclusive'}
              </div>
              <h2 className="text-3xl font-bold">
                {lang === 'ar' ? occasionsLevel.name_ar : occasionsLevel.name_en}
              </h2>
              <p className="text-purple-100 text-lg">
                {lang === 'ar'
                  ? 'دلل ضيوفك بأفخم العزومات والأكلات المخصصة للمناسبات السعيدة.'
                  : 'Treat your guests with the most luxurious banquets and dishes specially for happy occasions.'}
              </p>
              <Link
                to={`/level/${occasionsLevel.id}`}
                className="inline-block bg-white text-purple-900 px-8 py-3 rounded-full font-bold hover:bg-purple-50 transition-colors"
              >
                {lang === 'ar' ? 'تصفح تشكيلة المناسبات' : 'Browse Occasions Selection'}
              </Link>
            </div>
            <div className="hidden md:block w-64 h-64 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-sm">
              <Sparkles size={120} className="text-white/20" />
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

const Utensils = ({ size }: { size: number }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/>
    <path d="M7 2v20"/>
    <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>
  </svg>
);

export default HomePage;
