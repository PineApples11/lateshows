# seed.py
from app import app, db
from models import Guest, Episode, Appearance

with app.app_context():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    # Create sample guests
    guest1 = Guest(name="Beyoncé Knowles", occupation="Singer")
    guest2 = Guest(name="Elon Musk", occupation="Entrepreneur")
    guest3 = Guest(name="Serena Williams", occupation="Athlete")

    # Create sample episodes
    episode1 = Episode(date="2023-01-15", number=1)
    episode2 = Episode(date="2023-01-22", number=2)

    # Add guests and episodes to the session
    db.session.add_all([guest1, guest2, guest3, episode1, episode2])
    db.session.commit()

    # Create appearances
    appearance1 = Appearance(rating=4, guest_id=guest1.id, episode_id=episode1.id)
    appearance2 = Appearance(rating=5, guest_id=guest2.id, episode_id=episode1.id)
    appearance3 = Appearance(rating=3, guest_id=guest3.id, episode_id=episode2.id)

    db.session.add_all([appearance1, appearance2, appearance3])
    db.session.commit()

    print("✅ Database seeded successfully!")
