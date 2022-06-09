from flask import Blueprint
from flask import render_template
from .models import db
from .models import Cuisine
import datetime as DT

bp = Blueprint('main', __name__)

# Seeder function to insert sample data to database
#@bp.route('/cuisine/seeder')
#def seeder():
    # c1 = Cuisine(name='Wine & Prosciutto', description='Homemade prosciutto and red wine', date_from=DT.datetime(2022, 3, 5), date_to=DT.datetime(2022, 5, 5), image='proscuitto.jpg', quantity=500, price=80)
    # db.session.add(c1)

    # c2 = Cuisine(name='Ragu & Antipasti', description='Veal ragu & Vegetable antipasti', date_from=DT.datetime(2022, 6, 5), date_to=DT.datetime(2022, 7, 5), image='ragu.jpg', quantity=300, price=60)
    # db.session.add(c2)

    # c3 = Cuisine(name='Tempura & Miso', description='A miso soup entrée, Sake and Vegetable tempura', date_from=DT.datetime(2022, 7, 5), date_to=DT.datetime(2022, 8, 5), image='tempura.jpg', quantity=250, price=100)
    # db.session.add(c3)

    # db.session.commit()
    # return 'Seed Completed'

@bp.route('/')
def index():
    cuisines    = Cuisine.query.all()
    cs          = list()
    for cuisine in cuisines:
        if DT.datetime.now() < cuisine.date_from:
            cuisine.status = 'Upcoming'
        elif DT.datetime.now() > cuisine.date_from and DT.datetime.now() < cuisine.date_to:
            cuisine.status = 'Active'
        else:
            cuisine.status = 'Inactive'
        cs.append(cuisine)
    return render_template('base.html', cuisines=cs)