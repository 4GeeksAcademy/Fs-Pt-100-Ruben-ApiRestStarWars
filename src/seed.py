from app import app, db
from models import db, Users, Vehicles, Planets, Characters, Favourites


with app.app_context():
    db.drop_all()
    db.create_all()

    #users
    user1 = Users(email="HarryPotter@gmail.com", password="1234", username="HarryPotter", firstname="Harry", lastname="Potter")
    user2 = Users(email="HermioneGranger@gmail.com", password="5678", username="HermioneGranger", firstname="Hermione", lastname="Granger")
    db.session.add_all([user1, user2])
    db.session.commit()

    #Vehicles
    vehicle1 = Vehicles(name="Snowspeeder", model="t-47 airspeeder", cost_credits="unknown", max_speed="650", crew="2")
    vehicle2 = Vehicles(name="Sail barge", model="Modified Luxury Sail Barge", cost_credits="285000", max_speed="100", crew="26")
    db.session.add_all([vehicle1, vehicle2])
    
   

    #Planets
    planet1 = Planets(name="Tatooine", climate="Arid", population="200000", terrain="Desert")
    planet2 = Planets(name="Alderaan", climate="Temperate", population="2000000000", terrain="Grasslands, Mountains")
    db.session.add_all([planet1, planet2])
    
    


    #Characters
    character1 = Characters(name="Luke Skywalker", gender="Male", height="172", birth_year="19BBY", skin_color="Fair", eyes_color="Blue")
    character2 = Characters(name="Obi-Wan Kenobi", gender="Male", height="182", birth_year="57BBY", skin_color="Fair", eyes_color="Blue-Gray")
    db.session.add_all([character1, character2])

    
    print("✅ Datos sembrados correctamente.")