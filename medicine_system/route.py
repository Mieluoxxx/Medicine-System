from random import randrange

from flask import Blueprint, render_template, redirect, request, flash, jsonify
from datetime import date

from sqlalchemy import desc, and_

from models import db, User, Customer, Medicine, Orderlist, Supplier, Purchase, MedicinePrice, Warning
from pyecharts.charts import Line, Calendar, Bar
from pyecharts import options as opts

bp = Blueprint('main', __name__)


@bp.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                if user.is_admin:
                    return redirect('/index')
                else:
                    return redirect('common/index')
            else:
                flash('密码错误')
        else:
            flash('用户名不存在')
    return render_template('login.html')


@bp.route('/common/index')
def common_index():
    return render_template('common/index.html')


@bp.route('/index')
def admin():
    return render_template('index.html')


@bp.route('/price')
def price():
    prices = db.session.query(MedicinePrice.m_id, MedicinePrice.date, Medicine.name, MedicinePrice.cost, MedicinePrice.price) \
        .join(MedicinePrice.medicine) \
        .order_by(MedicinePrice.date.desc()).all()
    return render_template('price/price.html', prices=prices)


@bp.route('/warning')
def warning():
    warnings = Warning.query.order_by(desc(Warning.date)).all()
    return render_template('warning/warning.html', warnings=warnings)


@bp.route('/customer')
def customer():
    customers = Customer.query.all()
    return render_template('customer/customer.html', Customers=customers)


@bp.route('/customer/add', methods=['GET', 'POST'])
def customer_add():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_sex = request.form.get('customer_sex')
        customer_phone = request.form.get('customer_phone')
        customer_address = request.form.get('customer_address')
        if customer_name != "" and customer_sex != "" \
                and customer_phone != "" and customer_address != "":
            new_customer = Customer(name=customer_name, sex=customer_sex, phone=customer_phone,
                                    address=customer_address)
            print(customer_name, customer_sex, customer_phone, customer_address)
            db.session.add(new_customer)
            db.session.commit()
        return redirect('/customer')
    return render_template('customer/customer_add.html')


@bp.route('/customer/delete')
def customer_delete():
    customer_id = request.args.get('id')
    customer = Customer.query.filter_by(id=customer_id).first()
    new_Warning = Warning(description="删除客户：" + customer.name, date=date.today())
    if customer is None:
        return '客户不存在'
    db.session.add(new_Warning)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customer')


@bp.route('/customer/change', methods=['GET', 'POST'])
def customer_change():
    customer_id = request.args.get('id')
    customer = Customer.query.filter_by(id=customer_id).first()
    if request.method == 'POST':
        name, sex, phone, address = customer.name, customer.sex, customer.phone, customer.address
        customer_name = request.form.get('customer_name')
        customer_sex = request.form.get('customer_sex')
        customer_phone = request.form.get('customer_phone')
        customer_address = request.form.get('customer_address')

        if not customer_name:
            flash('客户姓名不能为空')
            return redirect('/customer_change')
        if not customer_sex:
            flash('客户性别不能为空')
            return redirect('/customer_change')
        if not customer_phone:
            flash('客户联系方式不能为空')
            return redirect('/customer_change')

        customer.name = customer_name
        customer.sex = customer_sex
        customer.phone = customer_phone
        customer.address = customer_address
        new_Warning = Warning(
            description="修改客户：{}->{},{}->{},{}->{},{}->{}"
            .format(name, customer_name, sex, customer_sex, phone,
                    customer_phone, address, customer_address),
            date=date.today())
        db.session.add(new_Warning)
        db.session.add(customer)
        db.session.commit()
        return redirect('/customer')
    return render_template('customer/customer_change.html', customer=customer)


@bp.route('/supplier')
def supplier():
    supplier = Supplier.query.all()
    return render_template('supplier/supplier.html', Suppliers=supplier)


@bp.route('/supplier/add', methods=['GET', 'POST'])
def supplier_add():
    if request.method == 'POST':
        supplier_name = request.form.get('supplier_name')
        supplier_person = request.form.get('supplier_person')
        supplier_phone = request.form.get('supplier_phone')
        supplier_address = request.form.get('supplier_address')
        if supplier_name != "" and supplier_person != "" \
                and supplier_phone != "" and supplier_address != "":
            new_supplier = Supplier(name=supplier_name, contact_person=supplier_person,
                                    phone=supplier_phone, address=supplier_address)
            db.session.add(new_supplier)
            db.session.commit()
        return redirect('/supplier')
    return render_template('supplier/supplier_add.html')


@bp.route('/supplier/delete')
def supplier_delete():
    supplier_id = request.args.get('id')
    supplier = Supplier.query.filter_by(id=supplier_id).first()
    new_Warning = Warning(description="删除供应商：" + supplier.name, date=date.today())
    if supplier is None:
        return '供应商不存在'
    db.session.add(new_Warning)
    db.session.delete(supplier)
    db.session.commit()
    return redirect('/supplier')


@bp.route('/supplier/change', methods=['GET', 'POST'])
def supplier_change():
    supplier_id = request.args.get('id')
    supplier = Supplier.query.filter_by(id=supplier_id).first()
    if request.method == 'POST':
        name, person, phone, address = supplier.name, supplier.contact_person, supplier.phone, supplier.address
        supplier_name = request.form.get('supplier_name')
        supplier_person = request.form.get('supplier_person')
        supplier_phone = request.form.get('supplier_phone')
        supplier_address = request.form.get('supplier_address')

        if not supplier_name:
            flash('供应商姓名不能为空')
            return redirect('/supplier_change')
        if not supplier_person:
            flash('联系人不能为空')
            return redirect('/supplier_change')
        if not supplier_phone:
            flash('联系方式不能为空')
            return redirect('/supplier_change')
        if not supplier_address:
            flash('供应商地址不能为空')
            return redirect('/supplier_change')

        supplier.name = supplier_name
        supplier.contact_person = supplier_person
        supplier.phone = supplier_phone
        supplier.address = supplier_address

        new_Warning = Warning(
            description="修改供应商：{}->{},{}->{},{}->{},{}->{}"
            .format(name, supplier_name, person, supplier_person, phone,
                    supplier_phone, address, supplier_address),
            date=date.today())

        db.session.add(new_Warning)
        db.session.add(supplier)
        db.session.commit()
        return redirect('/supplier')
    return render_template('supplier/supplier_change.html', supplier=supplier)


@bp.route('/common/medicine')
def common_medicine():
    medicines = Medicine.query.order_by(Medicine.id).all()
    m_p = db.session.query(MedicinePrice) \
        .order_by(desc(MedicinePrice.date)) \
        .distinct(MedicinePrice.m_id) \
        .order_by(MedicinePrice.m_id).all()
    medicines = zip(medicines, m_p)

    subquery = db.session.query(
        MedicinePrice.m_id,
        db.func.row_number().over(
            partition_by=MedicinePrice.m_id,
            order_by=MedicinePrice.date.desc()
        ).label('rn'),
        Medicine.name,
        MedicinePrice.cost,
        MedicinePrice.price,
        Medicine.stock
    ).join(Medicine, Medicine.id == MedicinePrice.m_id).subquery()

    test = db.session.query(
        subquery.c.m_id,
        subquery.c.name,
        subquery.c.cost,
        subquery.c.price,
        subquery.c.stock
    ).filter(subquery.c.rn == 1).order_by(subquery.c.m_id).all()
    return render_template('common/medicine.html', tests=test)


@bp.route('/medicine')
def medicine():
    medicines = Medicine.query.order_by(Medicine.id).all()
    m_p = db.session.query(MedicinePrice).order_by(desc(MedicinePrice.date)).distinct(MedicinePrice.m_id).order_by(
        MedicinePrice.m_id).all()
    medicines = zip(medicines, m_p)

    subquery = db.session.query(
        MedicinePrice.m_id,
        db.func.row_number().over(
            partition_by=MedicinePrice.m_id,
            order_by=MedicinePrice.date.desc()
        ).label('rn'),
        Medicine.name,
        MedicinePrice.cost,
        MedicinePrice.price,
        Medicine.stock
    ).join(Medicine, Medicine.id == MedicinePrice.m_id).subquery()

    test = db.session.query(
        subquery.c.m_id,
        subquery.c.name,
        subquery.c.cost,
        subquery.c.price,
        subquery.c.stock
    ).filter(subquery.c.rn == 1).order_by(subquery.c.m_id).all()

    return render_template('medicine/medicine.html', Medicines=medicines, tests=test)


@bp.route('/medicine/add', methods=['GET', 'POST'])
def medicine_add():
    if request.method == 'POST':
        medicine_id = request.form.get('medicine_id')
        medicine_name = request.form.get('medicine_name')
        medicine_s_id = int(request.form.get('supplier_id'))
        price = float(request.form.get('price'))
        medicine_description = request.form.get('medicine_description')
        if medicine_id != "" and medicine_name != "" \
                and price != "" and medicine_s_id != "" \
                and medicine_description != "":
            new_medicine = Medicine(id=medicine_id, name=medicine_name,
                                    s_id=medicine_s_id, description=medicine_description)

            new_price = MedicinePrice(m_id=medicine_id, price=price, date=date.today())
            db.session.add(new_medicine)
            db.session.add(new_price)
            db.session.commit()
        return redirect('/medicine')
    return render_template('medicine/medicine_add.html')


@bp.route('/medicine/delete')
def medicine_delete():
    medicine_id = request.args.get('id')
    medicine = Medicine.query.filter(Medicine.id.like('%{}%'.format(medicine_id))).first()
    new_Warning = Warning(description="删除药物：" + medicine.name, date=date.today())
    if medicine is None:
        return '药物不存在'
    db.session.add(new_Warning)
    db.session.delete(medicine)
    db.session.commit()
    return redirect('/medicine')


@bp.route('/medicine/change', methods=['GET', 'POST'])
def medicine_change():
    medicine_id = request.args.get('id')
    medicine = Medicine.query.filter(Medicine.id.like('%{}%'.format(medicine_id))).first()
    m_p = db.session.query(MedicinePrice).filter(MedicinePrice.m_id.like(f'%{medicine_id}%')).order_by(
        desc(MedicinePrice.date)).first()
    if request.method == 'POST':
        medicine_id = request.form.get('medicine_id')
        medicine_name = request.form.get('medicine_name')
        medicine_s_id = request.form.get('supplier_id')
        price = float(request.form.get('price'))
        medicine_description = request.form.get('medicine_description')

        if not medicine_id:
            flash('批准文号不能为空')
            return redirect('/medicine_change')
        if not medicine_name:
            flash('药物名称不能为空')
            return redirect('/medicine_change')
        if not medicine_s_id:
            flash('供应商编号不能为空')
            return redirect('/medicine_change')
        if not price:
            flash('药物售价不能为空')
            return redirect('/medicine_change')

        medicine.id = medicine_id
        medicine.name = medicine_name
        medicine.s_id = medicine_s_id
        medicine.description = medicine_description
        new_price = MedicinePrice(m_id=medicine_id, price=price, cost=m_p.cost, date=date.today())
        db.session.add(new_price)
        db.session.add(medicine)
        db.session.commit()
        return redirect('/medicine')
    return render_template('medicine/medicine_change.html', medicine=medicine, mp=m_p)


# 定义路由，用于处理获取药品详情的请求
@bp.route('/common/medicine/detail')
@bp.route('/medicine/detail')
def medicine_detail():
    # 获取药品 ID
    id = request.args.get('id')

    # 从数据库中获取药品信息
    medicine = Medicine.query.filter(Medicine.id.like('%{}%'.format(id))).first()
    supplier = Supplier.query.filter_by(id=medicine.s_id).first()
    # 将药品信息转换为字典
    medicine_dict = medicine.to_dict()
    supplier_dict = supplier.to_dict()
    # 将药品信息转换为 JSON 格式，并将其作为响应发送回客户端
    return jsonify(medicine_dict, supplier_dict)


@bp.route('/common/orderlist')
def common_orderlist():
    orderlist = Orderlist.query.all()
    return render_template('common/orderlist.html', Orderlists=orderlist)


@bp.route('/orderlist')
def orderlist():
    orderlist = Orderlist.query.all()
    return render_template('orderlist/orderlist.html', Orderlists=orderlist)


@bp.route('/common/orderlist/add', methods=['GET', 'POST'])
def common_orderlist_add():
    if request.method == 'POST':
        orderlist_name = request.form.get('order_name')
        orderlist_c_id = int(request.form.get('order_c_id'))
        orderlist_m_id = request.form.get('order_m_id')
        orderlist_quantity = int(request.form.get('order_quantity'))
        if orderlist_name and orderlist_c_id and orderlist_m_id and orderlist_quantity:
            if orderlist_c_id not in [c.id for c in Customer.query.all()]:
                flash('Invalid customer ID')
            elif orderlist_m_id not in [m.id for m in Medicine.query.all()]:
                flash('Invalid medicine ID')
            elif orderlist_quantity <= 0:
                flash('Invalid quantity')
            else:
                new_orderlist = Orderlist(m_id=orderlist_m_id, c_id=orderlist_c_id, name=orderlist_name,
                                          quantity=orderlist_quantity, date=date.today())
                try:
                    db.session.add(new_orderlist)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(str(e))
                return redirect('/common/orderlist')
        else:
            flash('Invalid input')
    return render_template('common/orderlist_add.html', customers=Customer.query.all(),
                           medicines=Medicine.query.all())


@bp.route('/orderlist/add', methods=['GET', 'POST'])
def orderlist_add():
    if request.method == 'POST':
        orderlist_name = request.form.get('order_name')
        orderlist_c_id = int(request.form.get('order_c_id'))
        orderlist_m_id = request.form.get('order_m_id')
        orderlist_quantity = int(request.form.get('order_quantity'))
        if orderlist_name and orderlist_c_id and orderlist_m_id and orderlist_quantity:
            if orderlist_c_id not in [c.id for c in Customer.query.all()]:
                flash('Invalid customer ID')
            elif orderlist_m_id not in [m.id for m in Medicine.query.all()]:
                flash('Invalid medicine ID')
            elif orderlist_quantity <= 0:
                flash('Invalid quantity')
            else:
                new_orderlist = Orderlist(m_id=orderlist_m_id, c_id=orderlist_c_id, name=orderlist_name,
                                          quantity=orderlist_quantity, date=date.today())
                try:
                    db.session.add(new_orderlist)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(str(e))
                return redirect('/orderlist')
        else:
            flash('Invalid input')
    return render_template('orderlist/orderlist_add.html', customers=Customer.query.all(),
                           medicines=Medicine.query.all())


@bp.route('/common/orderlist/delete')
def common_orderlist_delete():
    orderlist_id = request.args.get('id')
    order = Orderlist.query.filter_by(id=orderlist_id).first()
    # 检查订单是否已经退货
    if order.is_returned:
        return "该订单已经退货过了"

    orderlist_name = order.name
    orderlist_type = "退货"
    orderlist_m_id = order.m_id
    orderlist_c_id = order.c_id
    orderlist_quantity = order.quantity

    # 更新订单的退货状态
    order.is_returned = True
    new_order = Orderlist(m_id=orderlist_m_id, c_id=orderlist_c_id,
                          name=orderlist_name, quantity=orderlist_quantity,
                          date=date.today(), type=orderlist_type)

    db.session.add(new_order)
    db.session.commit()
    return redirect('/common/orderlist')


@bp.route('/orderlist/delete')
def orderlist_delete():
    orderlist_id = request.args.get('id')
    order = Orderlist.query.filter_by(id=orderlist_id).first()
    # 检查订单是否已经退货
    if order.is_returned:
        return "该订单已经退货过了"

    orderlist_name = order.name
    orderlist_type = "退货"
    orderlist_m_id = order.m_id
    orderlist_c_id = order.c_id
    orderlist_quantity = order.quantity

    # 更新订单的退货状态
    order.is_returned = True
    new_order = Orderlist(m_id=orderlist_m_id, c_id=orderlist_c_id,
                          name=orderlist_name, quantity=orderlist_quantity,
                          date=date.today(), type=orderlist_type)

    db.session.add(new_order)
    db.session.commit()
    return redirect('/orderlist')


@bp.route('/orderlist/detail')
def orderlist_detail():
    # 获取订单 ID
    id = request.args.get('id')
    print(id)
    # 从数据库中获取订单信息
    order = Orderlist.query.filter_by(id=id).first()
    medicine = Medicine.query.filter_by(id=order.m_id).first()
    customer = Customer.query.filter_by(id=order.c_id).first()
    m_p = db.session.query(MedicinePrice).filter(
        and_(MedicinePrice.m_id.like(f'%{medicine.id}%'), MedicinePrice.date <= order.date)).order_by(
        MedicinePrice.date.desc()).first()
    # 将订单信息转换为字典
    order_dict = order.to_dict()
    medicine_dict = medicine.to_dict()
    customer_dict = customer.to_dict()
    mp_dict = m_p.to_dict()
    # 将订单信息转换为 JSON 格式，并将其作为响应发送回客户端
    return jsonify(order_dict, medicine_dict, customer_dict, mp_dict)


@bp.route('/purchase')
def purchase():
    purchase = Purchase.query.all()
    return render_template('purchase/purchase.html', Purchases=purchase)


@bp.route('/purchase/add', methods=['GET', 'POST'])
def purchase_add():
    if request.method == 'POST':
        purchase_name = request.form.get('purchase_name')
        medicine_id = request.form.get('medicine_id')
        purchase_num = int(request.form.get('purchase_num'))
        price = float(request.form.get('price'))
        if purchase_name and medicine_id and purchase_num and price:
            if medicine_id not in [m.id for m in Medicine.query.all()]:
                flash('Invalid medicine ID')
            elif purchase_num <= 0:
                flash('Invalid quantity')
            elif price <= 0:
                flash('Invalid price')
            else:
                new_purchase = Purchase(medicine_id=medicine_id, name=purchase_name,
                                        quantity=purchase_num, date=date.today())
                latest_record = MedicinePrice.query.filter_by(m_id=medicine_id).order_by(
                    desc(MedicinePrice.date)).first()
                first_record = MedicinePrice.query.filter_by(m_id=medicine_id).order_by(
                    MedicinePrice.date).first()
                if latest_record.price != 0:
                    new_price = MedicinePrice(m_id=medicine_id, cost=price,
                                              price=first_record.price, date=date.today())
                    db.session.add(new_price)
                else:
                    latest_record.price = price
                    db.session.add(latest_record)
                try:
                    db.session.add(new_purchase)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(str(e))
                return redirect('/purchase')
        else:
            flash('Invalid input')
    return render_template('purchase/purchase_add.html', suppliers=Supplier.query.all(),
                           medicines=Medicine.query.all())


@bp.route('/purchase/delete')
def purchase_delete():
    purchase_id = request.args.get('id')
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    # 检查订单是否已经退货
    if purchase.is_returned:
        return "该采购单已经退货过了"

    purchase_name = purchase.name
    purchase_type = "退货"
    purchase_medicine_id = purchase.medicine_id
    purchase_quantity = purchase.quantity

    # 更新订单的退货状态
    purchase.is_returned = True
    new_purchase = Purchase(medicine_id=purchase_medicine_id, name=purchase_name,
                            quantity=purchase_quantity, date=date.today(),
                            type=purchase_type)

    db.session.add(new_purchase)
    db.session.commit()
    return redirect('/purchase')


@bp.route('/purchase/detail')
def purchase_detail():
    # 获取订单 ID
    id = request.args.get('id')
    # 从数据库中获取订单信息
    purchase = Purchase.query.filter_by(id=id).first()
    medicine = Medicine.query.filter_by(id=purchase.medicine_id).first()
    supplier = Supplier.query.filter_by(id=medicine.s_id).first()
    m_p = db.session.query(MedicinePrice).filter(
        and_(MedicinePrice.m_id.like(f'%{medicine.id}%'), MedicinePrice.date <= purchase.date)).order_by(
        MedicinePrice.date.desc()).first()
    # 将订单信息转换为字典
    if purchase and medicine and supplier:
        purchase_dict = purchase.to_dict()
        medicine_dict = medicine.to_dict()
        supplier_dict = supplier.to_dict()
        mp_dict = m_p.to_dict()
        # 将订单信息转换为 JSON 格式，并将其作为响应发送回客户端
        return jsonify(purchase_dict, medicine_dict, supplier_dict, mp_dict)


def bar_base(data):
    c = (
        Bar()
        .add_xaxis([i[0] for i in data])
        .add_yaxis("销售额", [i[1] for i in data])
        .add_yaxis("利润", [i[2] for i in data])
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(type_="value"),
            title_opts=opts.TitleOpts(title="每日销售额和利润"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return c


@bp.route("/barChart")
def get_bar_chart():
    result = db.session.query(
        Orderlist.date,
        db.func.round(db.func.sum(Orderlist.quantity * MedicinePrice.price), 2).label('sales'),
        db.func.round(db.func.sum(Orderlist.quantity * (MedicinePrice.price - MedicinePrice.cost)), 2).label('profit')
    ).join(
        MedicinePrice,
        (Orderlist.m_id == MedicinePrice.m_id) & (MedicinePrice.date <= Orderlist.date)
    ).group_by(Orderlist.date).order_by(Orderlist.date).all()
    data = []
    for row in result:
        date, order_amount, profit = row
        data.append((date.strftime('%Y-%m-%d'), order_amount, profit))
        print("时间", date, "销售额", order_amount, "利润", profit)
    bar = bar_base(data)
    return bar.dump_options_with_quotes()


@bp.route('/data')
def test():
    return render_template('data.html')
