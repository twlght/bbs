from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *  # 导入__init__.py

from models.reply import Reply
from utils import log, log2


main = Blueprint('reply', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    log2('DEBUG', form)
    u = current_user()
    # print('DEBUG', form)
    m = Reply.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))


if __name__ == '__main__':
    pass