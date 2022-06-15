from app import db


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text())
    price = db.Column(db.Float(9, 2))
    main_pic = db.Column(db.String())
    pictures = db.Column(db.String())
    is_automatic = db.Column(db.Boolean, default=True, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.title


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_start = db.Column(db.String())
    time_end = db.Column(db.String())