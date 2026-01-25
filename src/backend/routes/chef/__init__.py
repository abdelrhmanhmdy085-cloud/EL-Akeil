# Chef Routes Package
from .dishes import chef_dishes_bp
from .reviews import chef_reviews_bp
from .dashboard import chef_dashboard_bp

__all__ = ['chef_dishes_bp', 'chef_reviews_bp', 'chef_dashboard_bp']
