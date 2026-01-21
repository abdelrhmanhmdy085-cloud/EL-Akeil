import { Star } from 'lucide-react';

interface DishCardProps {
  dish: any;
  lang: 'ar' | 'en';
}

const DishCard = ({ dish, lang }: DishCardProps) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow border border-gray-100">
      <div className="relative h-48 overflow-hidden">
        <img
          src={dish.image || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c'}
          alt={dish.name}
          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
        />
        {!dish.is_available && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <span className="text-white font-bold bg-red-600 px-3 py-1 rounded">
              {lang === 'ar' ? 'غير متوفر' : 'Unavailable'}
            </span>
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-bold text-lg text-gray-900 truncate flex-1">{dish.name}</h3>
          <div className="flex items-center gap-1 text-yellow-500">
            <Star size={16} fill="currentColor" />
            <span className="text-sm font-semibold">{dish.rating}</span>
          </div>
        </div>

        <p className="text-gray-500 text-sm mb-3">
          {lang === 'ar' ? 'شيف:' : 'Chef:'} {dish.chef_name || 'Anonymous'}
        </p>

        <div className="flex flex-wrap gap-2 mb-4">
          <span className="px-2 py-1 bg-brand-50 text-brand-700 text-xs font-medium rounded-full">
            {lang === 'ar' ? dish.category?.name_ar : dish.category?.name_en}
          </span>
          <span className={`px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700`}>
            {lang === 'ar' ? dish.level?.name_ar : dish.level?.name_en}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-brand-800 font-bold text-lg">
            {dish.price} {lang === 'ar' ? 'ج.م' : 'EGP'}
          </span>
          <button className="bg-brand-700 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-brand-800 transition-colors">
            {lang === 'ar' ? 'اطلب الآن' : 'Order Now'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DishCard;
