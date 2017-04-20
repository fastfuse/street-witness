
from app import db
from sqlalchemy.dialects.postgresql import JSON



class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode)  #string?
    description = db.Column('description', db.Unicode)  #string?
    timestamp = db.Column('timestamp', db.Date)
    location = db.Column('location', JSON)
    status = db.Column('status', db.Unicode)
    # tag - as list??? many2many

    def __init__(self, title, description, location):
        self.title = title
        self.description = description
        self.location = location
        self.timestamp = datetime.utcnow().replace(microsecond=0) + \
                                                             timedelta(hours=3)
        self.status = 'active'

    def __repr__(self):
        return 'Title: {}'.format(self.title)

