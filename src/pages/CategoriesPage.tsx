import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const API_URL = 'http://localhost:5000/api';

const CategoriesPage = ({ lang }: { lang: 'ar' | 'en' }) => {
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/categories`)
      .then(res => setCategories(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-20">Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-gray-900">
        {lang === 'ar' ? 'تصنيفات الطعام' : 'Food Categories'}
      </h1>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
        {categories.map((category) => (
          <Link
            key={category.id}
            to={`/category/${category.id}`}
            className="bg-white p-8 rounded-2xl text-center border border-gray-100 hover:border-brand-200 hover:shadow-lg transition-all group"
          >
            <div className="text-5xl mb-4 transform group-hover:scale-110 transition-transform">
              {category.icon}
            </div>
            <h3 className="font-bold text-gray-800 text-lg">
              {lang === 'ar' ? category.name_ar : category.name_en}
            </h3>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default CategoriesPage;
