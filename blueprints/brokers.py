from flask import Blueprint, render_template
from forms.brokers import BrokerForm


brokers_bp = Blueprint('brokers', __name__, url_prefix = '/brokers')


@brokers_bp.route('/')
def broker_index():
    from model.broker import Broker
    from app import db

    brokers = db.session.query(Broker).all()

    form = BrokerForm()
    return render_template('brokers/index.html', form=form, brokers=brokers)

@brokers_bp.route('/', methods=['POST'])
def broker_post():
    form = BrokerForm()
    
    if (form.validate_on_submit()):
        from model.broker import Broker
        from app import db


        broker = Broker(
            name = form.data['name'],
            email = form.data['email'],
            webpage = form.data['webpage']
        )

        db.session.add(broker)
        db.session.commit()

        print('Saving to database...', broker.id)
        return 'Saving to database...'
    else: 
        return render_template('brokers/index.html', form=form)