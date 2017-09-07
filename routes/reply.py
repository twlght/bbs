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
    cur_user = current_user()
    if cur_user is None:
        return redirect(url_for('index.index'))
    # print('DEBUG', form)
    m = Reply.new(form, user_id=cur_user.id)  # str
    return redirect(url_for('topic.detail', id=m.topic_id))  # str


if __name__ == '__main__':
    pass