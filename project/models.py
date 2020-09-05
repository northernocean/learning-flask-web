from project import db


class Puppy(db.Model):

    # __tablename__ = "puppy"
    # default name will be puppy

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # first argument: Class Name
    # backref: Indicates the string name of a property to be placed on
    #          the related mapper's class that will handle this relationship 
    #          in the other direction. I.e., owner.puppy where owner is an instance of Owner
    owner = db.relationship("Owner", backref="puppy", uselist=False)

    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name} (id: {str(self.id)}, owner: {self.owner} )"

    def __repr__(self):
        return f'{{"id":"{self.id}", "name":"{self.name}", "owner":"{self.owner}"}}'


class Owner(db.Model):

    # __tablename__ = "owner"
    # default name will be owner
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # foreign key argument: "table.column_name". This will set up the physical column to hold the foreign key.
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppy.id"))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f'{{"name":"{self.name}"}}'
