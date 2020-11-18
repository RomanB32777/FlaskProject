# from . import profile
# from flask import render_template

# NAME = 'Misha'

# @profile.route('/')
# def about():
#     return render_template("about.html", name = NAME)



# from . import profile
# from flask import render_template, flash, redirect
# from .models import User


from . import profile
from flask import render_template, redirect, session, url_for, g, flash
from .forms import LoginForm, AddPost, RegisterForm
from flask_login import current_user, login_user, logout_user
from .models import User, Posts
from werkzeug.security import generate_password_hash, check_password_hash
from cloudipsp import Api, Checkout

NAME = 'Misha'

@profile.route('/')
def about():
    return render_template("about.html", name = NAME)


# @profile.route('/main_page/<int:user_id>/')
# def main_page(user_id):
#     user = User.objects(user_id = user_id).first()
#     return render_template("profile.html", user = user)

@profile.route('/main_page/<int:user_id>/')
@profile.route('/main_page/', defaults={'user_id': 0})
def main_page(user_id):
    if not user_id:
        if not current_user.is_authenticated:
            return redirect(url_for('profile.login'))
        return render_template("profile.html", user = current_user)
    else:
        user = User.objects(user_id = str(user_id)).first()
        if user is None:
            return render_template("about.html", name = NAME)
        else:
            return render_template("profile.html", user = user)

@profile.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.about'))
    form = RegisterForm()
    if form.years.data is None :
        flash('Введите правильно число', 'error')
        return redirect(url_for('profile.register'))
    # for f in form:
    #     print(f)
    old_user = User.objects(username=form.username.data).first()
    if old_user is not None :
    #     flash('Всё гуд!')
    # else:
        flash('Такой пользователь уже есть', 'error')
        return redirect(url_for('profile.register'))
    hash = generate_password_hash(str(form.password.data))
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = hash,
            full_name = form.full_name.data
                    )
        user.save()
    
    return render_template('register.html', form=form)


@profile.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.about'))
    form = LoginForm()
    if form.validate_on_submit():
        
        if form.years.data is None :
            flash('Введите правильно число', 'error')
            return redirect(url_for('profile.register'))
        user = User.objects(username=form.username.data).first()
        if user is None:
            flash('Invalid username', 'error')
            return redirect(url_for('profile.login'))
        if user and check_password_hash(str(form.password.data)):
            login_user(user)
            return redirect(url_for('profile.main_page'))
    return render_template('login.html', form=form)

@profile.route('/admin', methods = ['GET', 'POST'])#methods = ['GET', 'POST']-пишется когда есть форма(для заполнения)
def admin():
    abc = 12345678910
    form = login() #создаём переменную form, типа login
    if form.validate_on_submit():#проверка что пользователь нажал на кнопку
        if form.login.data == abc:
            print("sfsf")
            return redirect(url_for('profile.main_page'))
            # return redirect(url_for('profile.add_product')
        else:
            return redirect(url_for('profile.main_page'))
        #         return redirect(url_for('profile.about')
    return render_template("login.html", form = form)

@profile.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.about'))

@profile.route('/post/buy/<int:post_id>/')
def post_page(post_id):
    api = Api(merchant_id=1460849,
          secret_key='dLQEnCTzxbdV49sLP3jbfq3MMFWTh2dU')
    checkout = Checkout(api=api)
    data = {
    "currency": "RUB",
    "amount":  "100"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@profile.route('/posts/',  methods=['GET', 'POST'])
def posts():
    posts_list = []
    posts = Posts.objects[:20]
    for post in posts:
        sender = User.objects(user_id=post.user_id).first()

        posts_list.append({
            'user_name' : sender.username,
            'text' : post.text,
            'header' : post.header,
            'user_id' : sender.user_id
                        })
    form = AddPost()
    if form.validate_on_submit():
        post = Posts(
            user_id = current_user.user_id,
            text = form.posttext.data,
            header = form.posthead.data
                    )
        post.save()

    return render_template("posts.html", posts=posts_list, form=form, check=current_user.is_authenticated)