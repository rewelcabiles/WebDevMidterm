import datetime
import os
import JeGames.misc_functions as misc
from flask import render_template, url_for, flash, redirect, request, session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from JeGames.forms import RegisterForm, LoginForm, AddGameForm, SetFeaturedForm
from JeGames.models import AppUser, Game, Platform, owned_games, WebsiteSetting
from JeGames import app, db, bcrypt 
from sqlalchemy import func, desc, or_, and_
from datetime import datetime

@app.route('/game/<game_id>/<path:filename>')
def game_media(game_id, filename):
    if filename == None:
        filename = "1.jpg"
    return send_from_directory(os.path.join(app.instance_path, app.config["UPLOAD_FOLDER"]), str(game_id)+"/"+filename, as_attachment=True)

@app.route("/")
def index():
    new_release = Game.query.limit(5).all()
    most_popular = Game.query.join(owned_games).group_by(Game.id).order_by(desc(func.count(Game.id))).limit(5).all()
    coming_soon = Game.query.filter_by(status = "coming soon").limit(5).all()
    top_rated = Game.query.order_by(desc(Game.rating)).limit(4).all()
    limited_offer = Game.query.filter(Game.discount_expirable == True, Game.discount_end_date > datetime.now(), Game.discount > 0).order_by(Game.discount_end_date).limit(4).all()
    discount = Game.query.filter(Game.discount_expirable == False, Game.discount > 0).limit(4).all()
    featured_games_setting = WebsiteSetting.query.filter_by(setting_group="featured_games").all()
    featured_games = []
    for i in featured_games_setting:
        featured_games.append(Game.query.filter_by(id=i.setting_value).first())
    return render_template(
        "index.html",
        active_page = "index",
        new_release = new_release,
        most_popular = most_popular,
        coming_soon = coming_soon,
        top_rated = top_rated,
        limited_offer = limited_offer,
        discount = discount,
        featured_games = featured_games)


@app.route("/browse_games")
def browse_page():
    items_per_page = 16
    query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    is_free = request.args.get('free', False, type=bool)

    
    lo = request.args.get('lo', False, type=bool)
    uf = request.args.get('uf', False, type=bool)
    ut = request.args.get('ut', False, type=bool)

    windows = request.args.get('windows', False, type=bool)
    mac = request.args.get('mac', False, type=bool)
    linux = request.args.get('linux', False, type=bool)
    # To implement
    action = request.args.get('action', False, type=bool)
    adventure = request.args.get('adventure', False, type=bool)
    casual = request.args.get('casual', False, type=bool)
    racing = request.args.get('racing', False, type=bool)
    rpg = request.args.get('rpg', False, type=bool)
    simulation = request.args.get('simulation', False, type=bool)
    sports = request.args.get('sports', False, type=bool)
    strategy = request.args.get('strategy', False, type=bool)

    cs = request.args.get('cs', "", type=str)

    if cs == "new_release":
        db_query = Game.query

    elif cs == "top_selling":
        db_query = Game.query.join(owned_games).group_by(Game.id).order_by(desc(func.count(Game.id)))

    elif cs == "upcoming":
        db_query = Game.query.filter_by(status = "coming soon")

    elif cs == "top_rated":
        db_query = Game.query.order_by(desc(Game.rating))

    elif cs == "limited_offer":
        db_query =  Game.query.filter(Game.discount_expirable == True, Game.discount_end_date > datetime.now(), Game.discount > 0).order_by(Game.discount_end_date)
    elif cs == "onsale":
        db_query =  Game.query.filter(Game.discount_expirable == False, Game.discount > 0)

    else:
        if query == '':
            db_query = Game.query.join(Platform)
        else:
            db_query = Game.query.filter(Game.title.ilike("%" + query + "%"))

        if lo:
            db_query = db_query.filter(Game.has_discount)

        if uf:
            db_query = db_query.filter(Game.discount_price <= 400)

        if ut:
            db_query = db_query.filter(Game.discount_price <= 200)
            
        if windows: 
            db_query = db_query.filter(Game.platforms.any(name="windows", available = True))

        if mac: 
            db_query = db_query.filter(Game.platforms.any(name="mac", available = True))
        
        if linux: 
            db_query = db_query.filter(Game.platforms.any(name="linux", available = True))
    
    games = db_query.paginate(page=page, per_page=items_per_page)
    pagination = misc.Pagination(page, items_per_page, db_query.count())

    return render_template(
        "game_browse.html",
        pagination = pagination,
        games = games,
        active_page = "browse",
        is_free = is_free,
        page = page,
        q = query,
        uf = uf,
        ut = ut,
        lo = lo,
        windows = windows,
        mac = mac,
        linux = linux,
        cs = cs
        )

@app.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page == "logout":
                next_page = "index"
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("You have entered an invalid username or password", "flash_error")

    return render_template("signin.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route("/create_account", methods=["POST", "GET"])
def create_account_page():
    form = RegisterForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        register_date = datetime.datetime.now()
        hashed = bcrypt.generate_password_hash(form.password.data)

        new_user = AppUser(
            username = username,
            password = hashed,
            email = email,
            register_date = register_date,
            admin = 0
            )

        db.session.add(new_user)
        db.session.commit()
        flash('Account created succesfully! Login now!', 'flash_success')
        return redirect(url_for('login_page'))
    return render_template("signup.html", form=form)

@app.route("/support")
def support_page():
    return render_template(
        "support.html",
        active_page = "support")

@app.route("/game/<game_id>", methods=["GET"])
def game_page(game_id):
    game = Game.query.filter_by(id=game_id).first()
    reviews = game.reviews.all()
    windows_platform = game.platforms.filter(Platform.name == "windows").filter(Platform.game_id == game.id).first()
    linux_platform = game.platforms.filter(Platform.name == "linux").filter(Platform.game_id == game.id).first()
    mac_platform = game.platforms.filter(Platform.name == "mac").filter(Platform.game_id == game.id).first()

    has_game = False
    if game in current_user.owned_games:
        has_game = True
    else:
        has_game = False

    return render_template(
        "game_page.html", 
        game=game, 
        reviews=reviews, 
        has_game=has_game,
        win_platform = windows_platform,
        linux_platform = linux_platform,
        mac_platform = mac_platform
        )

@app.route("/game/<game_id>/modify", methods=["GET", "POST"])
@login_required
def modify_game_page(game_id):
    if current_user.admin == False:
        return redirect(url_for("index"))
    
    form = AddGameForm()

    if form.validate_on_submit():
        game = Game.query.filter_by(id=game_id).first()
        complete_path = misc.create_game_path(game.id)

        # Storing image
        if form.image_main.data:
            new_image_name = str(game.id) + "_main_image.jpg"
            path = os.path.join(complete_path, new_image_name)
            form.image_main.data.save(path)
            game.image_main = new_image_name

        if form.image_banner.data:
            new_image_name = str(game.id) + "_banner_image.jpg"
            path = os.path.join(complete_path, new_image_name)
            form.image_banner.data.save(path)
            game.image_banner = new_image_name


        if form.win_available.data:
            platform_name = "windows"
            windows = game.platforms.filter(Platform.name == platform_name).filter(Platform.game_id == game.id).first()
            if not windows:
                windows = Platform()
                windows.game_id = game.id
                db.session.add(windows)
                db.session.commit()
            windows.name = platform_name
            windows.available = form.win_available.data
            windows.min_os = form.win_min_os.data
            windows.min_processor = form.win_min_processor.data
            windows.min_memory = form.win_min_memory.data
            windows.min_storage = form.win_min_storage.data
            windows.min_graphics = form.win_min_graphics.data
            
            windows.max_os = form.win_max_os.data
            windows.max_processor = form.win_max_processor.data
            windows.max_memory = form.win_max_memory.data
            windows.max_storage = form.win_max_storage.data
            windows.max_graphics = form.win_max_graphics.data

        if form.linux_available.data:
            platform_name = "linux"
            linux = game.platforms.filter(Platform.name == platform_name).filter(Platform.game_id == game.id).first()
            if not linux:
                linux = Platform()
                linux.game_id = game.id
                db.session.add(linux)
                db.session.commit()
            linux.name = platform_name
            linux.available = form.linux_available.data
            linux.min_os = form.linux_min_os.data
            linux.min_processor = form.linux_min_processor.data
            linux.min_memory = form.linux_min_memory.data
            linux.min_storage = form.linux_min_storage.data
            linux.min_graphics = form.linux_min_graphics.data
            
            linux.max_os = form.linux_max_os.data
            linux.max_processor = form.linux_max_processor.data
            linux.max_memory = form.linux_max_memory.data
            linux.max_storage = form.linux_max_storage.data
            linux.max_graphics = form.linux_max_graphics.data

        if form.mac_available.data:
            platform_name = "mac"
            mac = game.platforms.filter(Platform.name == platform_name).filter(Platform.game_id == game.id).first()
            if not mac:
                mac = Platform()
                mac.game_id = game.id
                db.session.add(mac)
                db.session.commit()
            mac.name = platform_name
            mac.available = form.mac_available.data
            mac.min_os = form.mac_min_os.data
            mac.min_processor = form.mac_min_processor.data
            mac.min_memory = form.mac_min_memory.data
            mac.min_storage = form.mac_min_storage.data
            mac.min_graphics = form.mac_min_graphics.data
            
            mac.max_os = form.mac_max_os.data
            mac.max_processor = form.mac_max_processor.data
            mac.max_memory = form.mac_max_memory.data
            mac.max_storage = form.mac_max_storage.data
            mac.max_graphics = form.mac_max_graphics.data

        game.title = form.title.data
        game.description = form.description.data
        game.price = form.price.data
        game.discount = form.discount.data
        game.discount_expirable = form.discount_expirable.data
        game.discount_start_date = form.discount_start_date.data
        game.discount_end_date = form.discount_end_date.data
        game.developer = form.developer.data
        game.publisher = form.publisher.data
        game.status = form.status.data
        game.features = form.features.data
        game.other_details = form.other_details.data
        game.languages = form.languages.data
        
        db.session.commit()
        return redirect(url_for('game_page', game_id=game_id))

    elif request.method == "GET":
        game = Game.query.filter_by(id=game_id).first()
        form.title.data = game.title
        form.description.data = game.description
        form.price.data = game.price
        form.discount.data = game.discount
        form.discount_expirable.data = game.discount_expirable
        if game.discount_start_date == None:
            form.discount_start_date.data = datetime.now()
        else:
            form.discount_start_date.data = game.discount_start_date

        form.discount_end_date.data = game.discount_end_date
        form.developer.data = game.developer
        form.publisher.data = game.publisher
        form.status.data = game.status
        form.features.data = game.features
        form.other_details.data = game.other_details
        form.languages.data = game.languages
        
    return render_template(
        'add_game.html',
        form = form, 
        modify=True)

@app.route("/admin/add_game", methods=["POST", "GET"])
@login_required
def admin_add_game():
    if current_user.admin == False:
        return redirect(url_for("index"))
    form = AddGameForm()
    if form.validate_on_submit():
        new_game = Game(
            title = form.title.data,
            description = form.description.data,
            price = form.price.data,
            developer = form.developer.data,
            publisher = form.publisher.data,
            status = form.status.data,
            rating = form.rating.data,
            other_details = form.other_details.data,
            languages = form.languages.data,
        )
        
        db.session.add(new_game)
        db.session.commit()
        # Storing image
        complete_path = misc.create_game_path(new_game.id)
        if form.image_main.data:
            new_image_name = str(new_game.id) + "_main_image.jpg"
            path = os.path.join(complete_path, new_image_name)
            form.image_main.data.save(path)
            new_game.image_main = new_image_name

        if form.image_banner.data:
            new_image_name = str(new_game.id) + "_banner_image.jpg"
            path = os.path.join(complete_path, new_image_name)
            form.image_banner.data.save(path)
            new_game.image_banner = new_image_name

        windows = Platform(
            game_id = new_game.id,
            name = "windows",
            available = form.win_available.data,
            min_os = form.win_min_os.data,
            min_processor = form.win_min_processor.data,
            min_memory = form.win_min_memory.data,
            min_storage = form.win_min_storage.data,
            min_graphics = form.win_min_graphics.data,            
            max_os = form.win_max_os.data,
            max_processor = form.win_max_processor.data,
            max_memory = form.win_max_memory.data,
            max_storage = form.win_max_storage.data,
            max_graphics = form.win_max_graphics.data
        )

        linux = Platform(
            game_id = new_game.id,
            name = "linux",
            available = form.linux_available.data,
            min_os = form.linux_min_os.data,
            min_processor = form.linux_min_processor.data,
            min_memory = form.linux_min_memory.data,
            min_storage = form.linux_min_storage.data,
            min_graphics = form.linux_min_graphics.data,            
            max_os = form.linux_max_os.data,
            max_processor = form.linux_max_processor.data,
            max_memory = form.linux_max_memory.data,
            max_storage = form.linux_max_storage.data,
            max_graphics = form.linux_max_graphics.data
        )

        mac = Platform(
            game_id = new_game.id,
            name = "mac",
            available = form.mac_available.data,
            min_os = form.mac_min_os.data,
            min_processor = form.mac_min_processor.data,
            min_memory = form.mac_min_memory.data,
            min_storage = form.mac_min_storage.data,
            min_graphics = form.mac_min_graphics.data,            
            max_os = form.mac_max_os.data,
            max_processor = form.mac_max_processor.data,
            max_memory = form.mac_max_memory.data,
            max_storage = form.mac_max_storage.data,
            max_graphics = form.mac_max_graphics.data
        )

        db.session.add(windows)
        db.session.add(linux)
        db.session.add(mac)
        db.session.commit()
        misc.create_game_path(new_game.id)
        flash('Game created succesfully!', 'flash_success')
        return redirect(url_for('admin_page'))
    return render_template('add_game.html',form = form, modify=False)

@app.route("/admin/functions")
@login_required
def admin_page():
    if current_user.admin == False:
        return redirect(url_for("index"))
    return render_template("admin_page.html")

@app.route("/admin/edit_featured", methods=["POST", "GET"])
@login_required
def edit_featured():
    if current_user.admin == False:
        return redirect(url_for("index"))
    form = SetFeaturedForm()
    if form.validate_on_submit():
        f1 = WebsiteSetting.query.filter("feature1" == WebsiteSetting.setting_name).first()
        f2 = WebsiteSetting.query.filter("feature2" == WebsiteSetting.setting_name).first()
        f3 = WebsiteSetting.query.filter("feature3" == WebsiteSetting.setting_name).first()
        f4 = WebsiteSetting.query.filter("feature4" == WebsiteSetting.setting_name).first()
        f5 = WebsiteSetting.query.filter("feature5" == WebsiteSetting.setting_name).first()

        f1.setting_value = form.f1.data
        f2.setting_value = form.f2.data
        f3.setting_value = form.f3.data
        f4.setting_value = form.f4.data
        f5.setting_value = form.f5.data

        db.session.commit()

    elif request.method == "GET":
        f1 = WebsiteSetting.query.filter("feature1" == WebsiteSetting.setting_name).first()
        f2 = WebsiteSetting.query.filter("feature2" == WebsiteSetting.setting_name).first()
        f3 = WebsiteSetting.query.filter("feature3" == WebsiteSetting.setting_name).first()
        f4 = WebsiteSetting.query.filter("feature4" == WebsiteSetting.setting_name).first()
        f5 = WebsiteSetting.query.filter("feature5" == WebsiteSetting.setting_name).first()

        form.f1.data = f1.setting_value
        form.f2.data = f2.setting_value
        form.f3.data = f3.setting_value
        form.f4.data = f4.setting_value
        form.f5.data = f5.setting_value

    return render_template("admin_featured_games.html", form = form)


UPLOAD_FOLDER = '/games'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


