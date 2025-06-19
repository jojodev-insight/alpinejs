"""
Database initialization with default categories
"""
from app import create_app, db
from app.models.expense import Category

def init_database():
    """Initialize database with default categories"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if categories already exist
        if Category.query.count() == 0:
            # Create default categories
            default_categories = [
                {'name': 'Food & Dining', 'description': 'Restaurants, groceries, and food delivery', 'color': '#ff6b6b'},
                {'name': 'Transportation', 'description': 'Gas, public transport, ride sharing', 'color': '#4ecdc4'},
                {'name': 'Shopping', 'description': 'Clothing, electronics, personal items', 'color': '#45b7d1'},
                {'name': 'Entertainment', 'description': 'Movies, games, hobbies, and fun activities', 'color': '#96ceb4'},
                {'name': 'Bills & Utilities', 'description': 'Electricity, water, internet, phone', 'color': '#feca57'},
                {'name': 'Healthcare', 'description': 'Medical, dental, pharmacy expenses', 'color': '#ff9ff3'},
                {'name': 'Education', 'description': 'Books, courses, school supplies', 'color': '#a8e6cf'},
                {'name': 'Travel', 'description': 'Vacation, business trips, accommodation', 'color': '#fd79a8'},
                {'name': 'Home & Garden', 'description': 'Furniture, repairs, gardening supplies', 'color': '#fdcb6e'},
                {'name': 'Other', 'description': 'Miscellaneous expenses', 'color': '#6c5ce7'}
            ]
            
            for category_data in default_categories:
                category = Category(**category_data)
                db.session.add(category)
            
            try:
                db.session.commit()
                print(f"✅ Successfully created {len(default_categories)} default categories")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating categories: {e}")
        else:
            print("✅ Categories already exist, skipping creation")
        
        print("✅ Database initialization completed!")

if __name__ == '__main__':
    init_database()
