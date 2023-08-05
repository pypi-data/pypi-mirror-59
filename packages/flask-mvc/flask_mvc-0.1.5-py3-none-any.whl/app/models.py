from app import db
from sqlalchemy.orm import validates
from sqlalchemy_mixins import AllFeaturesMixin
from app import fields
from app import widgets

'''
AttributeError: 'NoneType' object has no attribute 'key' 
==> 
    # Add relation to foreign key field !!!
    namespace_id = db.Column(db.Integer, db.ForeignKey('namespace.id'))  # ohne id
    namespace = db.relationship("Namespace") 
'''


class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True
    __search_fields__ = []
    # to do : id !!!

    def get_view_url(self):
        return f'/app/admin/{self.__class__.__name__.lower()}/view/{self.id}'

    def get_edit_url(self):
        return f'/app/admin/{self.__class__.__name__.lower()}/edit/{self.id}'

    def get_delete_url(self):
        return f'/app/admin/{self.__class__.__name__.lower()}/delete/{self.id}'
    
    @classmethod 
    def get_add_url(cls):
        return f'/app/admin/{cls.__name__.lower()}/add'

    @classmethod 
    def get_index_url(cls):
        return f'/app/admin/{cls.__name__.lower()}'

    @classmethod 
    def get_verbose_name(cls):
        return ' '.join([field.capitalize() for field in cls.__name__.split('_')])

    @classmethod 
    def get_columns(cls, include=[], exclude=[]):
        columns = list()
        for col in cls.__table__.columns:
            if (not include and col.key not in exclude) or col.key in include:
                if col.key.endswith('_id'):
                    lookup_relation_key = col.key.replace('_id', '')
                    columns.append(cls.__mapper__.relationships.get(lookup_relation_key))
                else:
                    columns.append(col)
        for rel in cls.__mapper__.relationships:
            if rel not in columns:
                if (not include and rel.key not in exclude) or rel.key in include:
                    columns.append(rel)
        return columns

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    @classmethod
    def get_cleaned_object(cls, data):
        result = dict()
        for key,value in cls.__table__.columns.items():
            if key in data:
                result[key] = value.clean(data.getlist(key)[-1])
            else:
                print(f'WARNING: Missing value for key: {key}!')
        return result

    @classmethod
    def search(cls, search_term):
        from sqlalchemy import or_
        # to do: implement "contains" operator in Mixin
        search_term = search_term.replace('%', '')
        search_term = f'%{search_term}%'

        if cls.__search_fields__:
            # .where() seems not to support or query. But it is the better idea.
            search_parameters = {sf: search_term for sf in cls.__search_fields__}
            return cls.where(**search_parameters)
            '''
            query_params = []
            for sf in cls.__search_fields__:
                sf_split = sf.split('__') # in: name__ilike, name__contains
                field_name = sf_split[0]
                query_operator = sf_split[1] if 1 in sf_split else None
                
                field_attr = getattr(cls, field_name)
                if query_operator:
                    field_attr = getattr(field_attr, query_operator)
                    query_params.append(field_attr(search_term)) 
                else: # exact match
                    query_params.append(field_name == search_term)
            #  print(cls.name.like('ed').__dict__)
            print (query_params)
            '''

        # return db.session.query(cls).filter(cls.name.ilike(search_term)) # or_(cls.name.like('ed'), cls.name.like == 'wendy')

    @classmethod
    def commit(cls):
        cls._session.commit()

    @classmethod
    def rollback(cls):
        cls._session.rollback()

    @classmethod
    def get_view_widget(cls, field_name:str):
        field = getattr(cls, field_name) # col declaration
        return field.view_widget

    @classmethod
    def get_edit_widget(cls, field_name:str, params={}):
        field = getattr(cls, field_name) # col declaration (not value)
        if hasattr(field, 'edit_widget'):
            return field.edit_widget(cls, field_name, None, params)

        relationship = cls.__mapper__.relationships.get(field_name)
        if relationship is not None:
            return relationship.get_edit_widget()(cls, field_name, None, params)

        return widgets.ModelTextWidget(cls, field_name, None, params)

    def get_view_widget_rendered(self, field_name:str, params={}):
        field = getattr(self.__class__, field_name)
        if hasattr(field, 'view_widget'):
            return field.view_widget(self.__class__, field_name, self, params)

        relationship = self.__mapper__.relationships.get(field_name)
        if relationship is not None:
            return relationship.get_view_widget()(self.__class__, field_name, self, params)

        return widgets.ModelWidget(self.__class__, field_name, self, params)

    def get_edit_widget_rendered(self, field_name:str, params={}):
        field = getattr(self.__class__, field_name)
        if hasattr(field, 'edit_widget'):
            return field.edit_widget(self.__class__, field_name, self, params)

        relationship = self.__mapper__.relationships.get(field_name)
        if relationship is not None:
            return relationship.get_edit_widget()(self.__class__, field_name, self, params)

        return widgets.ModelWidget(self.__class__, field_name, self, params)
        

class Namespace(BaseModel):
    __search_fields__ = ['name__ilike']

    id = fields.PrimaryKeyField()
    name = fields.StringField(index=True, unique=True)
    templates = fields.relationship("Template") # templates = db.relationship("Template") # todo backref: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    @validates('name')
    def validate_name(self, key, value):
        value = value.strip()
        if not value:
            raise AssertionError('Name cannot be blank!')
        return value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} ({self.id})'


class Template(BaseModel):
    __search_fields__ = ['name__ilike']

    id = fields.PrimaryKeyField()
    name = fields.StringField(index=True, unique=True)
    primitive = fields.BooleanField(nullable=False, server_default=db.false())
    namespace_id = fields.ForeignKeyField('namespace.id')
    namespace = fields.relationship("Namespace") # foreign_keys='Friend.user_id'

    @validates('name')
    def validate_name(self, key, value):
        value = value.strip()
        if not value:
            raise AssertionError('Name cannot be blank!')
        return value

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} ({self.id})'


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    


class Instance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    template = db.relationship("Template")
    # created + modified ?


class Variable(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    name = db.Column(db.String(64), index=True, unique=True) # not unique?
    required = db.Column(db.Boolean)
    multivalue = db.Column(db.Boolean)


class Type_Instances(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_Integer(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_Decimal(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float(precision=None, asdecimal=True, decimal_return_scale=True))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_Boolean(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Boolean)
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_String(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_Image(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Type_File(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


######## Initialize active Record from sqlalchemy-mixins ########
BaseModel.set_session(db.session)

'''
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
'''
registry = dict()
for cls in db.Model._decl_class_registry.values():
    if isinstance(cls, type) and issubclass(cls, db.Model):
        registry[cls.__name__.lower()] = cls