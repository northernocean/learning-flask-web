from app import db, Puppy

print()

# create
puppy = Puppy("rufus", 5)
db.session.add(puppy)
db.session.commit()

# read
puppies = Puppy.query.all()
for puppy in puppies:
    print(puppy)
print()

# select by id
puppy = Puppy.query.get(1)
print(str(puppy.name))
print()

# filter
qry = Puppy.query.filter_by(name="rufus")
for puppy in qry.all():
    print(puppy)
print()

# update
puppy = Puppy.query.get(1)
puppy.age = 10
db.session.add(puppy)
db.session.commit()
print(puppy)
print()

# delete
puppy = Puppy.query.get(2)
db.session.delete(puppy)
db.session.commit()

# get all puppies again and view changes
puppies = Puppy.query.all()
for puppy in puppies:
    print(puppy)
print()
