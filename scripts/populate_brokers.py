import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from model.broker import Broker

brokers_data = [
    {
        "name": "Academic Work",
        "webpage": "https://www.academicwork.se/",
        "description": "Specialist in staffing and recruitment of young professionals.",
        "location": "Sweden",
        "focus_areas": "IT, Engineering, Business"
    },
    {
        "name": "Ework Group",
        "webpage": "https://www.eworkgroup.com/se/",
        "description": "Consultant supplier in IT, telecom, technology, and business development.",
        "location": "Sweden",
        "focus_areas": "IT, Telecom, Engineering"
    },
    {
        "name": "DFind IT",
        "webpage": "https://www.dfind.se/it/",
        "description": "Recruitment and consulting in IT and tech.",
        "location": "Sweden",
        "focus_areas": "IT, Tech, Development"
    },
    {
        "name": "Workforce Logic",
        "webpage": "https://eu.workforcelogiq.com/",
        "description": "Global workforce management solutions",
        "location": "Sweden",
        "focus_areas": "IT, Technology, Consulting"
    },
    {
        "name": "Cision",
        "webpage": "https://news.cision.com/se/cision",
        "description": "Media and communications technology consulting",
        "location": "Sweden",
        "focus_areas": "IT, Communications, Media"
    },
    {
        "name": "Verama",
        "webpage": "https://app.verama.com/",
        "description": "Digital talent matching platform",
        "location": "Sweden",
        "focus_areas": "IT, Digital, Consulting"
    },
    {
        "name": "Wise IT",
        "webpage": "https://getwiser.se/",
        "description": "IT consultant matching platform",
        "location": "Sweden",
        "focus_areas": "IT, Security, Development"
    },
    {
        "name": "A Society",
        "webpage": "https://www.asocietygroup.com/",
        "description": "IT and security consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Security, Consulting"
    },
    {
        "name": "SWCG",
        "webpage": "https://swcg.com/jobs",
        "description": "Swedish Consulting Group",
        "location": "Sweden",
        "focus_areas": "IT, Security, Management"
    },
    {
        "name": "R2m",
        "webpage": "https://r2m.se/",
        "description": "IT consultant matching platform",
        "location": "Sweden",
        "focus_areas": "IT, Development, Security"
    },
    {
        "name": "Hays",
        "webpage": "https://www.hays.se/",
        "description": "Global recruitment and consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Technology, Security"
    },
    {
        "name": "Gigstep",
        "webpage": "https://www.gigstep.se/",
        "description": "Freelance and consultant marketplace",
        "location": "Sweden",
        "focus_areas": "IT, Development, Consulting"
    },
    {
        "name": "Future and Friends",
        "webpage": "https://futureandfriends.se/",
        "description": "Digital consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Digital, Technology"
    },
    {
        "name": "Cinode",
        "webpage": "https://app.cinode.com/",
        "description": "Consultant matching and management platform",
        "location": "Sweden",
        "focus_areas": "IT, Security, Development"
    },
    {
        "name": "AFRY",
        "webpage": "https://portal.afry.com/",
        "description": "Engineering and digital solutions",
        "location": "Sweden",
        "focus_areas": "IT, Engineering, Security"
    },
    {
        "name": "Smartr",
        "webpage": "https://www.smartr.me/",
        "description": "Smart talent matching platform",
        "location": "Sweden",
        "focus_areas": "IT, Technology, Development"
    },
    {
        "name": "Aliant",
        "webpage": "https://www.aliant.se/",
        "description": "IT consultant broker",
        "location": "Sweden",
        "focus_areas": "IT, Security, Consulting"
    },
    {
        "name": "Connected Skills",
        "webpage": "https://connectedskills.se/",
        "description": "Tech talent network",
        "location": "Sweden",
        "focus_areas": "IT, Development, Security"
    },
    {
        "name": "Inkopia CPro",
        "webpage": "https://itc.inkopia.se/",
        "description": "Consultant management platform",
        "location": "Sweden",
        "focus_areas": "IT, Management, Development"
    },
    {
        "name": "ITnetwork",
        "webpage": "https://itcnetwork.se/",
        "description": "IT consultant network",
        "location": "Sweden",
        "focus_areas": "IT, Security, Networking"
    },
    {
        "name": "Knowledge Agency",
        "webpage": "https://www.knowledgeagency.se/",
        "description": "Knowledge-based consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Security, Knowledge Management"
    },
    {
        "name": "OneAgency",
        "webpage": "https://www.oneagency.se/",
        "description": "Digital consultant agency",
        "location": "Sweden",
        "focus_areas": "IT, Digital, Security"
    },
    {
        "name": "Brainville",
        "webpage": "https://www.brainville.com/",
        "description": "Sweden's largest consultant marketplace",
        "location": "Sweden",
        "focus_areas": "IT, Development, Consulting"
    },
    {
        "name": "Visma",
        "webpage": "https://www.visma.se/",
        "description": "Business software and consulting",
        "location": "Nordic",
        "focus_areas": "IT, Business Systems, Security"
    },
    {
        "name": "Keyman",
        "webpage": "https://www.keyman.se/",
        "description": "IT consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Security, Development"
    },
    {
        "name": "Experis",
        "webpage": "https://www.experis.se/",
        "description": "IT and engineering consulting",
        "location": "Sweden",
        "focus_areas": "IT, Engineering, Security"
    },
    {
        "name": "B3",
        "webpage": "https://www.b3.se/",
        "description": "Digital consulting group",
        "location": "Sweden",
        "focus_areas": "IT, Digital Transformation, Security"
    },
    {
        "name": "Castra",
        "webpage": "https://www.castra.se/",
        "description": "IT consultant broker",
        "location": "Sweden",
        "focus_areas": "IT, Security, Development"
    },
    {
        "name": "Cybertronic",
        "webpage": "https://www.cybertronic.online/",
        "description": "Cybersecurity consulting",
        "location": "Sweden",
        "focus_areas": "Cyber Security, IT Security"
    },
    {
        "name": "TNG",
        "webpage": "https://www.tng.se/",
        "description": "Tech recruitment and consulting",
        "location": "Sweden",
        "focus_areas": "IT, Tech, Security"
    },
    {
        "name": "Fintechconnector",
        "webpage": "https://www.fintechconnector.com/",
        "description": "Fintech consultant matching",
        "location": "Sweden",
        "focus_areas": "Fintech, IT Security, Development"
    },
    {
        "name": "Quality Sourcing",
        "webpage": "https://qualitysourcing.se/",
        "description": "IT consultant quality matching",
        "location": "Sweden",
        "focus_areas": "IT, Quality Assurance, Security"
    },
    {
        "name": "Nox Consulting",
        "webpage": "https://www.noxconsulting.se/",
        "description": "IT security consulting",
        "location": "Sweden",
        "focus_areas": "IT Security, Cyber Security, Development"
    },
    {
        "name": "Onster",
        "webpage": "https://onster.com/se/",
        "description": "IT consultant marketplace",
        "location": "Sweden",
        "focus_areas": "IT, Development, Security"
    },
    {
        "name": "Techfactory",
        "webpage": "https://www.techfactory.se/",
        "description": "Tech talent platform",
        "location": "Sweden",
        "focus_areas": "IT, Tech, Development"
    },
    {
        "name": "Vindex",
        "webpage": "https://www.vindex.se/",
        "description": "IT consultant matching",
        "location": "Sweden",
        "focus_areas": "IT, Security, Development"
    }
]

with app.app_context():
    # Clear existing brokers
    db.session.query(Broker).delete()
    
    # Add new brokers
    for broker_data in brokers_data:
        broker = Broker(**broker_data)
        db.session.add(broker)
    
    db.session.commit()
    print(f"Added {len(brokers_data)} brokers to the database.") 