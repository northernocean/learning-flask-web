import os
from app import db
from app import Puppy

os.remove("data.sqlite")

# can be done with command line tools (i.e. migrate db)
db.create_all()

sam = Puppy("Sammy", 3)
frank = Puppy("Frankie", 4)

print(sam)
print(frank)

db.session.add_all([frank, sam])

db.session.commit()

print(frank)
print(sam)


