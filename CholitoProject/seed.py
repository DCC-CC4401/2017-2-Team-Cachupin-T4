from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from naturalUser.models import NaturalUser
from municipality.models import MunicipalityUser
from municipality.models import Municipality
from ong.models import ONGUser
from ong.models import ONG
from animals.models import Animal
from animals.models import AnimalType

content_type = ContentType.objects.get_for_model(NaturalUser)
permission = Permission.objects.create(
    codename='natural_user_access',
    name='Can Publish Posts',
    content_type=content_type,
)

content_type = ContentType.objects.get_for_model(MunicipalityUser)
permission = Permission.objects.create(
    codename='municipality_user_access',
    name='Can Publish Posts',
    content_type=content_type,
)

# remove all users
for user in User.objects.all():
    user.delete()

# remove all natural users
for nuser in NaturalUser.objects.all():
    nuser.delete()

# remove all munis
for mun in Municipality.objects.all():
    mun.delete()

# remove all municipal users
for muser in MunicipalityUser.objects.all():
    muser.delete()

# remove all Ong
for on in ONG.objects.all():
    on.delete()

# remove all Ongs users
for ouser in ONGUser.objects.all():
    ouser.delete()

# remove all Animals
for an in Animal.objects.all():
    an.delete()

# remove all Animal Types
for at in AnimalType.objects.all():
    at.delete()

#create super user
User.objects.create_superuser('admin', 'admin@example.com','password123')

#Create natural user
mail='user1@example.com'
user_name='user1'
pas='passus1'
f_name='natural'
l_name='user1'
img= '/n_users/avatar/user1.jpg'

parent_user = User.objects.create_user(mail, user_name, pas)
use = NaturalUser(user=parent_user, avatar=img)
use.save()

#Create municipality user
mail='munisantiago@example.com'
user_name='muni'
pas='passus2'
f_name='Municipalidad'
l_name='Santiago'
img= '/n_users/avatar/user2.jpg'

muni_name= "Municipalidad de Santiago"
muni_dir= "Avenida Siempre Viva"
muni_lat =10
muni_lng = 20
muni_img = '/n_users/avatar/user2.jpg'

parent_user = User.objects.create_user(mail, user_name, pas)
muni = Municipality(name = muni_name,
                    lat= muni_lat,
                    lng= muni_lng,
                    directions = muni_dir,
                    avatar = muni_img)
muni.save()
use = MunicipalityUser(user=parent_user, municipality=muni)
use.save()

#Create ong user
mail='onganimalistas@example.com'
user_name='onganimalistas'
pas='passus3'
f_name='Animalistas'
l_name=''
img= '/n_users/avatar/user3.jpg'

ong_name= "Municipalidad de Santiago"
ong_dir= "Avenida Siempre Viva"
ong_lat =10
ong_lng = 20

parent_user = User.objects.create_user(mail, user_name, pas)
ong = ONG(name = ong_name,
                    lat= ong_lat,
                    lng= ong_lng,
                    directions = ong_dir)
ong.save()
# use = ONGUser(user=parent_user, municipality=muni)
use = ONGUser(ong=ong)
use.save()

name = 'animal'
gender = 1
description = 'Lorem Ipsum'
animal_type = AnimalType(name='gato')
animal_type.save()
color = 'rojo'
estimated_age = 15
days_in_adoption = 30


# Create Animals
for i in range(5):
    animal_name = name + str(i)
    animal = Animal(name=animal_name,
                    gender=gender,
                    description=description,
                    animal_type=animal_type,
                    color=color,
                    days_in_adoption=days_in_adoption,
                    estimated_age=estimated_age)
    animal.save()


