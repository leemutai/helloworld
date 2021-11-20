from flask import *
app = Flask(__name__)
from crypt import verify_password,hash_password

#API -- Application Programming Interface
#CRUD--Create Read Update Delete
import pymysql
connection = pymysql.connect(host='bigboyfreezy.mysql.pythonanywhere-services.com', user='bigboyfreezy',password='farahabdi2001',database='bigboyfreezy$default')


@app.route('/profile/<int:customer_id>')
def profile(customer_id):
    try:


        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql= 'select * from customers where customer_id = %s'
        cursor.execute(sql,(customer_id))
        if cursor.rowcount > 0:
            record = cursor.fetchone()
            response = jsonify(record)
            response.status_code = 200
            return response
        else:
            response = jsonify({'msg': 'Not Found'})
            response.status_code = 404
            return response
    except Exception as e:
        response = jsonify({'msg': 'Error Occured'})
        response.status_code = 404
        return response

@app.route('/login', methods = ['POST'])
def login():
    import pymysql
    connection = pymysql.connect(host='bigboyfreezy.mysql.pythonanywhere-services.com', user='bigboyfreezy',password='farahabdi2001',database='bigboyfreezy$default')

    try:
        json = request.json
        email = json['email']
        password = json['password']

        if email and password and request.method == 'POST':
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = 'select * from customers where email = %s '
            cursor.execute(sql,(email))

            if cursor.rowcount == 0:
                response = jsonify({'msg': 'Email Not Found'})
                response.status_code = 404
                return response
            else:

                row = cursor.fetchone()
                hashed_password = row['password']
                # verify
                status = verify_password(hashed_password, password)
                if status == True:

                    response = jsonify(row)
                    response.status_code = 200
                    return response

                elif status == False:
                    response = jsonify({'msg': 'Login Failed'})
                    response.status_code = 404
                    return response
                else:
                    response = jsonify({'msg': 'Login Failed'})
                    response.status_code = 404
                    return response
        else:
            response = jsonify({'msg': 'Your Fields Are Empty'})
            response.status_code = 200
            return response
    except Exception as e:
            response = jsonify({'msg': 'Your Fields Are Empty'})
            response.status_code = 200
            return response

@app.route('/register', methods = ['POST'])
def register():

    try:
        json = request.json
        fname = json['fname']
        lname = json['lname']
        email = json['email']
        password = json['password']
        confirm_password = json['confirm_password']
        tel = json['tel']

        if len(fname) == 0:
            response = jsonify({'msg': 'Empty Firstname'})
            response.status_code = 302
            return response
        elif len(lname) == 0:
            response = jsonify({'msg': 'Empty Lastname'})
            response.status_code = 302
            return response
        elif len(email) == 0:
            response = jsonify({'msg': 'Empty Email'})
            response.status_code = 302
            return response
        elif len(tel) < 10:
            response = jsonify({'msg': 'Empty Phone Number'})
            response.status_code = 302
            return response
        elif len(password) < 8:
            response = jsonify({'msg': 'Telephone number should be atleast ten numbers'})
            response.status_code = 302
            return response
        if password != confirm_password:
            response = jsonify({'msg': 'Password Do Not Match'})
            response.status_code = 302
            return response

        else:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = 'insert into customers(fname,lname,email,password,tel)values(%s,%s,%s,%s,%s) '
            try:

                cursor.execute(sql, (fname,lname,email,hash_password(password),tel))
                connection.commit()
                response = jsonify({'msg': 'Saved successful'})
                response.status_code = 302
                return response
            except:
                response = jsonify({'msg': 'Failed to save'})
                response.status_code = 302
                return response
    except:
        response = jsonify({'msg': 'Something Went Wrong'})
        response.status_code = 302
        return response

list10 = []
@app.route("/myorders",methods = ['POST'])
def customer_pending_orders():



            json = request.json
            tel = json['tel']
            list10.clear()


            sql = 'select DISTINCT order_code from orders where email = %s and status = %s order by pay_date desc'
            cursor = connection.cursor()
            cursor.execute(sql, (tel, 'Pending'))
            if cursor.rowcount > 0:
                rows = cursor.fetchall()
                for row in rows:
                    sql4 = 'select * from orders where order_code = %s and status = %s order by pay_date desc'
                    cursor4 = connection.cursor(pymysql.cursors.DictCursor)
                    cursor4.execute(sql4, (row[0], 'Pending'))
                    rows = cursor4.fetchall()
                    list10.append(rows)
                response = jsonify(list10)
                response.status_code = 200
                return response
            else:
                response = jsonify({'msg':'No records'})
                response.status_code = 302
                return response

@app.route("/products")
def products():

            connection = pymysql.connect(host='bigboyfreezy.mysql.pythonanywhere-services.com', user='bigboyfreezy',password='farahabdi2001',database='bigboyfreezy$default')

            sql = 'select * from products'
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            if cursor.rowcount > 0:
                record = cursor.fetchall()
                response = jsonify(record)
                response.status_code = 200
                return response
            else:
                response = jsonify({'msg':'Not found'})
                response.status_code = 200
                return response

@app.route("/product_single/<int:product_id>")
def product_single(product_id):

            sql = 'select * from products where product_id=%s'
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql,(product_id))
            if cursor.rowcount > 0:
                record = cursor.fetchone()
                response = jsonify(record)
                response.status_code = 302
                return response
            else:
                response = jsonify({'msg':'Not found'})
                response.status_code = 302
                return response


@app.route('/changepassword', methods = ['POST'])
def changepassword():

        if request.method == 'POST':
            json =request.json
            customer_id= request.json['customer_id']
            currentpassword = request.json['currentpassword']
            newpassword = request.json['newpassword']
            confirmpassword = request.json['confirmpassword']

            sql = 'select * from customers where customer_id = %s'
            cursor = connection.cursor()
            cursor.execute(sql, (customer_id))
            print(cursor.rowcount)
            if cursor.rowcount==0:
                response = jsonify({'msg': 'User Does Not Exist'})
                response.status_code = 404
                return response
            else:
                # fetchpassword..just one
                row = cursor.fetchone()
                hashed_password = row[4]
                # verify the hashed and the password if they match
                status = verify_password(hashed_password, currentpassword)
                if status == True:
                    # if new pass is not the same as confirm pass then they dont math and u render the template
                    if newpassword !=confirmpassword:
                        response = jsonify({'msg': 'Password Do Not Match'})
                        response.status_code = 404
                        return response
                    else:
                        sql = 'UPDATE customers SET password = %s where customer_id = %s'
                        cursor = connection.cursor()
                        cursor.execute(sql,(hash_password(newpassword), customer_id))
                        connection.commit()
                        response = jsonify({'msg': 'Password Changed'})
                        response.status_code = 200
                        return response

                else:
                    response = jsonify({'msg': 'Current Password is wrong'})
                    response.status_code = 404
                    return response

        else:
            response = jsonify({'msg': 'POST NEEDED'})
            response.status_code = 404
            return response


@app.route('/edit_profile', methods = ['POST'])
def edit_profile():
        if request.method == "POST":
            json= request.json
            customer_id = request.json['customer_id']
            fname = request.json['fname']
            lname = request.json['lname']
            email = request.json['email']
            tel= request.json['tel']



            cursor = connection.cursor()
            sql = 'update customers set fname = %s, lname = %s, email = %s, tel = %s   where customer_id= %s'
            cursor.execute(sql, (fname, lname, email, tel,customer_id ))
            connection.commit()
            response = jsonify({'msg': 'update successful'})
            response.status_code = 200
            return response

        else:

            response = jsonify({'msg': 'POST NEEDED'})
            response.status_code = 202
            return response


@app.route('/order', methods = ['POST'])
def edit_projjjfile():
        if request.method == "POST":
            json= request.json

            product_name = request.json['product_name']
            product_qtty = request.json['product_qtty']
            product_cost = request.json['product_cost']
            order_code = request.json['order_code']
            total_price = request.json['total_price']
            all_total_price = request.json['all_total_price']
            tel = request.json['tel']
            cursor = connection.cursor()
            sql = 'insert into orders (product_name,product_qtty,product_cost,all_total_price,email,order_code,individual_total)values(%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (product_name, product_qtty,product_cost,all_total_price,tel,order_code,total_price ))
            connection.commit()
            response = jsonify({'msg': 'Order successful'})
            response.status_code = 200
            return response

        else:

            response = jsonify({'msg': 'POST NEEDED'})
            response.status_code = 202
            return response




import requests
import datetime

import base64
from requests.auth import HTTPBasicAuth
@app.route('/payment', methods = ['POST'])
def mpesa_payment():
            json= request.json
            amount = request.json['amount']
            phone = request.json['phone']
            # GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response1 = requests.post(url, json=payload, headers=headers)
            print (response1.text)
            response = jsonify({'msg': 'PAID'})
            response.status_code = 200
            return response

if __name__ == '__main__':
    app.run(port=6060)
    app.debug = True
