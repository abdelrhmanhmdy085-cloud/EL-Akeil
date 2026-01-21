import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Utensils } from 'lucide-react';

const API_URL = 'http://localhost:5000/api';

const LevelsPage = ({ lang }: { lang: 'ar' | 'en' }) => {
  const [levels, setLevels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/levels`)
      .then(res => setLevels(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-20">Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-gray-900">
        {lang === 'ar' ? 'مستويات الطعام' : 'Food Levels'}
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {levels.map((level) => (
          <Link
            key={level.id}
            to={`/level/${level.id}`}
            className="bg-white p-8 rounded-2xl border border-gray-100 hover:border-brand-200 hover:shadow-lg transition-all group relative overflow-hidden"
          >
            <div className="relative z-10 flex flex-col h-full justify-between gap-4">
              <h3 className="font-bold text-gray-800 text-2xl">
                {lang === 'ar' ? level.name_ar : level.name_en}
              </h3>
              <p className="text-gray-500">
                {lang === 'ar' ? 'اكتشف الأطباق المميزة في هذا المستوى' : 'Explore unique dishes in this level'}
              </p>
              <div className="w-16 h-1 bg-brand-600 rounded-full group-hover:w-full transition-all duration-500"></div>
            </div>
            <div className="absolute -right-8 -bottom-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <Utensils size={160} />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default LevelsPage;
