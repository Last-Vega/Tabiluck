from . import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'users.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
                        )
    post_name = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    posted_date = db.Column(db.Date)
    traveled_flag = db.Column(db.Integer)
    transportation_flag = db.Column(db.Integer)
    period = db.Column(db.Integer)
    image_name = db.Column(db.String(100))

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            post_name=self.post_name,
            content=self.content,
            posted_date=self.posted_date,
            traveled_flag=self.traveled_flag,
            transportation_flag=self.transportation_flag,
            period=self.period,
            image_name=self.image_name
        )

    def __repr__(self):
        return '<Post {}, {}>'.format(self.post_name, self.posted_date)


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    e_mail = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def to_dict(self):
        return dict(
            id=self.id,
            user_name=self.user_name,
            e_mail=self.e_mail,
            password=self.password
        )

    def __repr__(self):
        return '<User %r>' % self.user_name


class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))
    post_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'posts.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
                        )

    def to_dict(self):
        return dict(
            id=self.id,
            tag_name=self.tag_name,
            post_id=self.post_id
        )

    def __repr__(self):
        return '<Tag %r>' % self.tag_name


class Like(db.Model):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}
    liker_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'posts.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True
    )

    def to_dict(self):
        return dict(
            liker_id=self.liker_id,
            post_id=self.post_id
        )

    def __repr__(self):
        return '<Like %r, %r>' % self.liker_id, self.post_id


class Schedule(db.Model):
    __tablename__ = 'schedules'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'posts.id',
            onupdate='CASCADE',
            ondelete='CASCADE'),
    )
    title = db.Column(db.String(1000))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    transportation = db.Column(db.String(100))
    memo = db.Column(db.String(1000))
    image_name = db.Column(db.String(1000))

    def to_dict(self):
        return dict(
            id=self.id,
            post_id=self.post_id,
            title=self.title,
            latitude=self.latitude,
            longitude=self.longitude,
            start_time=self.start_time,
            end_time=self.end_time,
            transportation=self.transportation,
            memo=self.memo,
            image_name=self.image_name
        )

    def __repr__(self):
        return '<Schedule {}>'.format(self.title)


class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer,
                             db.ForeignKey(
                                 'users.id',
                                 onupdate='CASCADE',
                                 ondelete='CASCADE')
                             )
    post_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'posts.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
                        )
    comment_time = db.Column(db.DateTime)
    comment = db.Column(db.String(1000))

    def to_dict(self):
        return dict(
            id=self.id,
            commenter_id=self.commenter_id,
            post_id=self.post_id,
            comment_time=self.comment_time,
            comment=self.comment
        )

    def __repr__(self):
        return '<Comment %r>' % self.comment


class Follow(db.Model):
    __tablename__ = 'follow'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    followee_id = db.Column(db.Integer,
                            db.ForeignKey(
                                'users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE')
                            )
    follower_id = db.Column(db.Integer,
                            db.ForeignKey(
                                'users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE')
                            )

    def to_dict(self):
        return dict(
            id=self.id,
            followee_id=self.followee_id,
            follower=self.follower_id
        )

    def __repr__(self):
        return '<Follow %r %r>' % self.follower_id, self.followee_id
