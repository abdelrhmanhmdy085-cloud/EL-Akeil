import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DishCard from '../components/DishCard';

const API_URL = 'http://localhost:5000/api';

const CategoryDetailPage = ({ lang }: { lang: 'ar' | 'en' }) => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/category/${id}/dishes`)
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="text-center py-20">Loading...</div>;
  if (!data) return <div className="text-center py-20">Not found</div>;

  // Group dishes by level
  const groupedDishes = data.dishes.reduce((acc: any, dish: any) => {
    const levelId = dish.level_id;
    if (!acc[levelId]) {
      acc[levelId] = {
        name: lang === 'ar' ? dish.level.name_ar : dish.level.name_en,
        dishes: []
      };
    }
    acc[levelId].dishes.push(dish);
    return acc;
  }, {});

  return (
    <div>
      <div className="flex items-center gap-4 mb-8">
        <div className="text-5xl">{data.category.icon}</div>
        <h1 className="text-4xl font-bold text-gray-900">
          {lang === 'ar' ? data.category.name_ar : data.category.name_en}
        </h1>
      </div>

      <div className="space-y-12">
        {Object.values(groupedDishes).length > 0 ? (
          Object.values(groupedDishes).map((group: any) => (
            <div key={group.name}>
              <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b-2 border-brand-100 pb-2 inline-block">
                {group.name}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {group.dishes.map((dish: any) => (
                  <DishCard key={dish.id} dish={dish} lang={lang} />
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-20 text-gray-500">
            {lang === 'ar' ? 'لا يوجد أطباق حالياً في هذا التصنيف' : 'No dishes found in this category'}
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoryDetailPage;
