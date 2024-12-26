from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle

# إعداد تطبيق Flask
app = Flask(__name__)

# إعداد اتصال قاعدة البيانات
def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xe")
    connection = cx_Oracle.connect(user="root", password="230101", dsn=dsn)
    return connection

# الصفحة الرئيسية (عرض وإضافة طلب)
@app.route('/')
def home():
    return render_template('index.html')

# إضافة منتج جديد
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product-name']
        product_description = request.form['product-description']
        quantity_in_stock = request.form['quantity']
        price = request.form['price']

        connection = get_db_connection()
        cursor = connection.cursor()

        # استعلام إدخال المنتج
        query = """
            INSERT INTO products (product_name, product_description, quantity_in_stock, price)
            VALUES (:product_name, :product_description, :quantity_in_stock, :price)
        """
        cursor.execute(query, [product_name, product_description, quantity_in_stock, price])
        connection.commit()

        cursor.close()
        connection.close()
        return redirect(url_for('home'))

    return render_template('add.html')

# البحث عن طلب
@app.route('/search_order', methods=['POST'])
def search_order():
    order_id = request.form['order_id']
    connection = get_db_connection()
    cursor = connection.cursor()

    # استعلام جلب بيانات الطلب
    query = """
        SELECT order_id, supplier_id, order_date, total_amount
        FROM purchase_orders
        WHERE order_id = :order_id
    """
    cursor.execute(query, [order_id])
    result = cursor.fetchone()

    order = None
    if result:
        order = {
            "order_id": result[0],
            "supplier_id": result[1],
            "order_date": result[2],
            "total_amount": result[3],
        }

    cursor.close()
    connection.close()
    return render_template('index.html', order=order)

if __name__ == '_main_':
    app.run(debug=True)