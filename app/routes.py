import os
from datetime import date, datetime

from app import app, db
from flask import render_template, request, redirect, url_for

from app.forms import ItemCreationForm, ItemUpdateForm, ItemImagesForm, ItemAddJournal
from app.models import Auto, Journal, User


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/index')
@app.route('/')
def index():
    auto_list = Auto.query.all()
    return render_template('index.html', auto_list=auto_list)


@app.route('/auto-create', methods=['GET', 'POST'])
def auto_create():
    form = ItemCreationForm()
    if form.validate_on_submit():
        new_item = Auto()
        new_item.title = form.title.data
        new_item.description = form.description.data
        new_item.price = form.price.data
        new_item.is_available = form.is_available.data
        new_item.is_automatic = form.is_automatic.data
        file = form.main_pic.data
        if allowed_file(file.filename):
            logo = f'images/items/{file.filename}'
            file.save(os.path.join(app.config['STATIC_ROOT'], logo))
            new_item.main_pic = logo
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('auto_create.html', form=form)


@app.route('/auto-update/<item_id>', methods=['GET', 'POST'])
def item_update(item_id):
    item = Auto.query.get(item_id)
    journal1 = Journal.query.filter_by(auto_id=item_id).all()
    if journal1:
        for j in journal1:
            diff = datetime.strptime(j.time_end, '%d.%m.%Y %H:%M') - datetime.strptime(j.time_start, '%d.%m.%Y %H:%M')
            j.price = float(diff.seconds / 60) * float(item.price)
    form = ItemUpdateForm(title=item.title, price=item.price.__round__(1), description=item.description, main_pic=item.main_pic, is_available=item.is_available, is_automatic=item.is_automatic)
    success_url = url_for('index')
    if form.validate_on_submit():
        action = request.form.get('action', '')
        if action == 'save':
            item.title = form.title.data
            item.price = form.price.data
            item.description = form.description.data
            item.is_available = form.is_available.data
            item.is_automatic = form.is_automatic.data
            file = form.main_pic.data
            if allowed_file(file.filename):
                logo = f'images/items/{file.filename}'
                file.save(os.path.join(app.config['STATIC_ROOT'], logo))
                item.main_pic = logo
        elif action == 'del':
            db.session.delete(item)
        db.session.commit()
        return redirect(success_url)
    return render_template('auto_update.html', item=item, journal=journal1, form=form)


@app.route('/auto-images/<item_id>', methods=['GET', 'POST'])
def images_update(item_id):
    item = Auto.query.get(item_id)
    form = ItemImagesForm()
    success_url = url_for('images_update', item_id=item_id)
    if form.validate_on_submit():
        action = request.form.get('action', '')
        if action == 'save':
            file = form.pictures.data
            if allowed_file(file.filename):
                logo = f'images/items/{file.filename}'
                file.save(os.path.join(app.config['STATIC_ROOT'], logo))
                if item.pictures:
                    item.pictures = f'{item.pictures},{logo}'
                else:
                    item.pictures = logo
        elif action == 'del':
            item.picture_id = form.picture_id.data
            if len(item.pictures.split(',')) == 1:
                item.pictures = ''
            elif len(item.pictures.split(',')) > 1:
                pictures_list = item.pictures.split(',')
                list_id = int(item.picture_id - 1)
                pictures_list.pop(list_id)
                item.pictures = ','.join(str(item1) for item1 in pictures_list)
        db.session.commit()
        return redirect(success_url)
    return render_template('auto_images.html', item=item, form=form)


@app.route('/auto-detail/<item_id>', methods=['GET', 'POST'])
def auto_detail(item_id):
    item = Auto.query.get(item_id)
    form = ItemAddJournal()
    if form.validate_on_submit():
        action = request.form.get('action', '')
        now = datetime.now()
        if action == 'rent_start':
            item1 = Journal()
            item1.auto_id = item_id
            item1.user_id = 1
            item1.time_start = now.strftime("%d.%m.%Y %H:%M")
            item.is_available = False
            db.session.add(item1)
        elif action == 'rent_stop':
            item2 = Journal.query.filter_by(auto_id=item_id, user_id=1).order_by(Journal.id.desc()).first()
            item2.time_end = now.strftime("%d.%m.%Y %H:%M")
            item.is_available = True
        db.session.commit()
        return redirect(url_for('auto_detail', item_id=item_id))
    return render_template('auto_detail.html', item=item, form=form)


@app.route('/rental-log')
def rental_log():
    item_journal = Journal.query.all()
    list_id = []
    list_car = []
    if item_journal:
        for j in item_journal:
            item = Auto.query.filter_by(id=j.auto_id).first()
            list_id.append(item.id)
            dict_car = {'id': 0, 'title': '', 'count': 0, 'time': 0, 'cost': 0}
            diff = datetime.strptime(j.time_end, '%d.%m.%Y %H:%M') - datetime.strptime(j.time_start,
                                                                                        '%d.%m.%Y %H:%M')
            if list_car:
                is_append = False
                for car in list_car:
                    if is_append:
                        break
                    if item.title == car['title']:
                        car['count'] += 1
                        car['time'] += float(diff.seconds / 60)
                        car['cost'] += float(diff.seconds / 60) * float(item.price)
                    else:
                        for id1 in list_id:
                            is_error = False
                            for car in list_car:
                                if id1 == car['id']:
                                    is_error = True
                                    break
                        if not is_error:
                            dict_car['title'] = item.title
                            dict_car['count'] = 1
                            dict_car['id'] = item.id
                            dict_car['main_pic'] = item.main_pic
                            dict_car['time'] = float(diff.seconds / 60)
                            dict_car['cost'] = float(diff.seconds / 60) * float(item.price)
                            list_car.append(dict_car)
                            is_append = True
            else:
                dict_car['title'] = item.title
                dict_car['count'] = 1
                dict_car['id'] = item.id
                dict_car['main_pic'] = item.main_pic
                dict_car['time'] = float(diff.seconds / 60)
                dict_car['cost'] = float(diff.seconds / 60) * float(item.price)
                list_car.append(dict_car)

    return render_template('rental_log.html', item_journal=list_car)