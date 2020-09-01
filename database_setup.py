import os
from app import db, Puppy, Owner, Toy

rufus = Puppy("Rufus", 3, "Lab")
fido = Puppy("Fido", 2, "Poodle")

db.session.add_all([rufus,fido])
db.session.commit()

print(Puppy.query.all())

jose = Owner("Jose",rufus.id)
toy1 = Toy('Chew Toy',rufus.id)
toy2 = Toy("Ball",rufus.id)

db.session.add_all([jose,toy1,toy2])
db.session.commit()

rufus = Puppy.query.filter_by(name='Rufus').first()
print(repr(rufus))

print(rufus.report_toys())
