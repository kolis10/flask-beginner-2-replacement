from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50))
    job_place = db.Column(db.String(50))
    job_pay = db.Column(db.String(20))

    def __repr__(self):
        return '<Jobs %r>' % self.username

    def serialize(self):
        return {
            "job_name": self.job_name,
            "job_place": self.job_place,
            "job_pay": self.job_pay
        }

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(40))
    date_of_birth = db.Column(db.String(10))
    email = db.Column(db.String(120))

    achievements = db.relationship('Achievements', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "username": self.username,
            "date of birth": self.date_of_birth,
            "email": self.email,
            "achievements": [x.serialize() for x in self.achievements]
        }

class Achievements(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    achievement = db.Column(db.String(100))
    reward = db.Column(db.String(40))
    
    user = db.relationship('Users', back_populates='achievements')

    def __repr__(self):
        return '<Achievements %r>' % self.achievement

    def serialize(self):
        return {
            "user_id": self.user_id,
            "achievement": self.achievement,
            "username": self.user.username,
            "reward": self.reward
        }

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }