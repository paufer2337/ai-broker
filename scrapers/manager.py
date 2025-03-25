from datetime import datetime
import logging
from model.mission import Mission
from .brokers import SCRAPER_MAP

class ScraperManager:
    @staticmethod
    def get_scraper_for_broker(broker):
        """Returns appropriate scraper for a broker or None"""
        for broker_name, scraper_class in SCRAPER_MAP.items():
            if broker_name in broker.name.lower():
                return scraper_class(broker)
        return None
    
    @staticmethod
    def update_missions(db):
        from model.broker import Broker
        
        brokers = Broker.query.all()
        for broker in brokers:
            scraper = ScraperManager.get_scraper_for_broker(broker)
            if scraper:
                try:
                    missions = scraper.scrape()
                    for mission_data in missions:
                        existing = Mission.query.filter_by(
                            title=mission_data['title'],
                            broker_id=broker.id
                        ).first()
                        
                        if not existing:
                            mission = Mission(**mission_data)
                            db.session.add(mission)
                    
                    broker.last_sync = datetime.utcnow()
                    db.session.commit()
                    
                except Exception as e:
                    logging.error(f"Error scraping {broker.name}: {str(e)}")
            else:
                logging.info(f"No scraper implemented for {broker.name}") 