import pytest
from scrapers.brokers.wise_it import WiseITScraper
from model.broker import Broker

def test_wise_it_scraper(test_app):
    with test_app.app_context():
        # Create test broker
        broker = Broker(
            name="Wise IT",
            webpage="https://getwiser.se/",
            description="Test broker",
            location="Stockholm"
        )
        
        # Initialize scraper
        scraper = WiseITScraper(broker)
        
        # Run scraper
        missions = scraper.scrape()
        
        # Verify results
        assert len(missions) > 0
        
        # Check mission structure
        for mission in missions:
            assert 'title' in mission
            assert 'description' in mission
            assert 'location' in mission
            assert 'required_skills' in mission
            assert 'broker_id' in mission
            assert 'posted_date' in mission
            assert 'status' in mission 