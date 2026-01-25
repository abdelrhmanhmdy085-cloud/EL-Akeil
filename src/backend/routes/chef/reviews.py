from flask import Blueprint, request, jsonify
from sqlalchemy import desc

chef_reviews_bp = Blueprint('chef_reviews', __name__, url_prefix='/api/chef')

@chef_reviews_bp.route('/reviews', methods=['GET'])
def get_chef_reviews():
    """الحصول على تقييمات الشيف"""
    try:
        chef_id = request.headers.get('Chef-ID') or request.args.get('chef_id')
        
        if not chef_id:
            return jsonify({'error': 'Chef ID required'}), 400
        
        from backend.models import Review, Dish
        
        reviews = Review.query.join(Dish).filter(
            Dish.chef_id == chef_id
        ).order_by(desc(Review.created_at)).all()
        
        rating_stats = {
            'average': 0,
            'total': len(reviews),
            'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
        
        if reviews:
            total_rating = sum(r.rating for r in reviews)
            rating_stats['average'] = round(total_rating / len(reviews), 1)
            
            for review in reviews:
                if 1 <= review.rating <= 5:
                    rating_stats['distribution'][review.rating] += 1
        
        return jsonify({
            'status': 'success',
            'stats': rating_stats,
            'reviews': [r.to_dict() for r in reviews]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chef_reviews_bp.route('/reviews/<int:review_id>/response', methods=['POST'])
def add_review_response(review_id):
    """الرد على تقييم"""
    try:
        from backend.models import db, Review
        
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        chef_id = request.headers.get('Chef-ID')
        
        # Verify chef owns the dish
        if review.dish.chef_id != int(chef_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        response_text = request.json.get('response')
        
        if not response_text:
            return jsonify({'error': 'Response text required'}), 400
        
        review.chef_response = response_text
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Response added'
        }), 200
        
    except Exception as e:
        from backend.models import db
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
