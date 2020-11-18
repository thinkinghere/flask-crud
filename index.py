from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from forms import NewsForm
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost:3306/news?charset=utf8'
app.config['SECRET_KEY'] = 'csrf key'
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    images = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    creat_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.title  # 查询的时候会打印出


db.create_all()


class OrmTest:
    def add_one(self):
        new_obj = News(
            title='标题',
            content='内容',
            types='标题',
        )
        db.session.add(new_obj)  # db 封装了session
        db.session.commit()
        return new_obj

    def query(self):
        print(News.query.all())


@app.route('/')
def index():
    news_list = News.query.all()
    print(news_list)
    return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>/')
def cat(name):
    return render_template('cat.html', name=name)


@app.route('/detail/<int:pk>/')  # 指定int
def detail(pk):
    return render_template('detail.html', pk=pk)


@app.route('/add/', methods=('GET', 'POST'))
def add():
    form = NewsForm()
    if form.validate_on_submit():
        new_obj = News(
            title=form.title.data,  # 从form中获取数据
            content=form.content.data,
            types=form.types.data,
            images=form.images.data,
            creat_at=datetime.now()
        )
        db.session.add(new_obj)
        db.session.commit()
        return redirect(url_for('index'))  # 添加成功后跳转
    return render_template('add.html', form=form)


@app.route('/update/<int:pk>', methods=('GET', 'POST'))
def update(pk):
    new_obj = News.query.get(pk)
    if not new_obj:
        return redirect(url_for('index'))
    form = NewsForm(obj=new_obj)
    if form.validate_on_submit():
        new_obj.title = form.title.data,  # 从form中获取数据
        new_obj.content = form.content.data,
        new_obj.types = form.types.data,
        new_obj.images = form.images.data,
        new_obj.creat_at = datetime.now()
        db.session.add(new_obj)
        db.session.commit()
        return redirect(url_for('index'))  # 添加成功后跳转
    return render_template('edit.html', form=form)


@app.route('/delete/<int:pk>', methods=('GET', 'POST'))
def delete(pk):
    new_obj = News.query.get(pk)
    if not new_obj:
        return 'no'
    new_obj.is_valid = False
    db.session.add(new_obj)
    db.session.commit()
    return 'yes'


if __name__ == '__main__':
    # obj = OrmTest()
    # obj.add_one()
    # obj.query()
    app.run(debug=True)
