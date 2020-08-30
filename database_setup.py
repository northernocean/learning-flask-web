from app import db
from app import Puppy

# can be done with command line tools (i.e. migrate db)
db.create_all()

sam = Puppy("Sammy", 3)
frank = Puppy("Frankie", 4)

print(sam.id)
print(frank.id)

db.session.add_all([frank, sam])

db.session.commit()

print(sam.id)
print(frank.id)


