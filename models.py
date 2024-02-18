from consts import Base, db


class Currency(Base):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(3))
    rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    def __init__(self, currency_code, rate, timestamp):
        self.currency_code = currency_code
        self.rate = rate
        self.timestamp = timestamp
