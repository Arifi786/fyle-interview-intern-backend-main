from core import db
from core.libs import helpers
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Teacher %r>' % self.id


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        include_relationships = True
        include_fk = True
        load_instance = True
