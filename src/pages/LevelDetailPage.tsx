import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DishCard from '../components/DishCard';

const API_URL = 'http://localhost:5000/api';

const LevelDetailPage = ({ lang }: { lang: 'ar' | 'en' }) => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/level/${id}/dishes`)
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="text-center py-20">Loading...</div>;
  if (!data) return <div className="text-center py-20">Not found</div>;

  // Group dishes by category
  const groupedDishes = data.dishes.reduce((acc: any, dish: any) => {
    const categoryId = dish.category_id;
    if (!acc[categoryId]) {
      acc[categoryId] = {
        name: lang === 'ar' ? dish.category.name_ar : dish.category.name_en,
        icon: dish.category.icon,
        dishes: []
      };
    }
    acc[categoryId].dishes.push(dish);
    return acc;
  }, {});

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          {lang === 'ar' ? data.level.name_ar : data.level.name_en}
        </h1>
        <p className="text-gray-500">
          {lang === 'ar' ? 'استعرض أفضل الأطباق بهذا المستوى' : 'Browse the best dishes at this level'}
        </p>
      </div>

      <div className="space-y-12">
        {Object.values(groupedDishes).length > 0 ? (
          Object.values(groupedDishes).map((group: any) => (
            <div key={group.name}>
              <div className="flex items-center gap-2 mb-6 border-b-2 border-brand-100 pb-2 inline-flex">
                <span className="text-2xl">{group.icon}</span>
                <h2 className="text-2xl font-bold text-gray-800">
                  {group.name}
                </h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {group.dishes.map((dish: any) => (
                  <DishCard key={dish.id} dish={dish} lang={lang} />
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-20 text-gray-500">
            {lang === 'ar' ? 'لا يوجد أطباق حالياً في هذا المستوى' : 'No dishes found in this level'}
          </div>
        )}
      </div>
    </div>
  );
};

export default LevelDetailPage;
