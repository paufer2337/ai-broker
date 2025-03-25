from flask import Blueprint, render_template, redirect, url_for
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
            name=form.data['name'],
            email=form.data['email'],
            webpage=form.data['webpage'],
            description=form.data['description'],
            location=form.data['location'],
            focus_areas=form.data['focus_areas']
        )

        db.session.add(broker)
        db.session.commit()

        return redirect(url_for('brokers.broker_index'))
    else: 
        return render_template('brokers/index.html', form=form)