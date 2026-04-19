from app import app
from extensions import db
from scrapers.manager import ScraperManager

def update_database():
    with app.app_context():
        # Update missions from all brokers
        ScraperManager.update_missions(db)
        print("Database updated with latest missions")

if __name__ == '__main__':
    update_database()