from models.mail import Mail
from flask import (
    Blueprint,
    render_template,
    request,
)

from routes import current_user

main = Blueprint('mail', __name__)


@main.route('/')
def index():
    u = current_user()
    mails = Mail.find_all(receiver_id=u.id)
    return render_template('mail/index.html', mails=mails)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    mail = Mail.new(form)
    # mail.save()
