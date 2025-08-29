from flask import Flask,render_template,request, redirect, url_for
from main import Main
main = Main()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/FlightFind', methods = ["GET","POST"])
def ui():
    if request.method == "POST":
        cities = [request.form["from_country"], request.form["to_country"]]
        city_codes = main.iata_find(cities)
        username = request.form["user_name"]

        data = {
            username : {
               "first_name" : request.form["first_name"],
                "last_name" : request.form["last_name"],
                "from_country" : request.form["from_country"],
                "to_country" : request.form["to_country"],
                "travel_date" : request.form["travel_date"].replace("/","-"),
                "depature_date" : request.form["depature_date"].replace("/","-"),
                "nonstop" : request.form.get("nonstop"),
                "from_iata": city_codes[0],
                "to_iata": city_codes[1],
                "price" : request.form["max_price"]
            }
        }
        # return "pushed"
        if data[username]["nonstop"] and len(data[username]["price"]) > 2: 
            main.data_handler(data)
            flight_data = main.flight_find(username, data[username]["nonstop"])

            if not flight_data.nonstop_found:
                return render_template("flight_ui.html", nostop=False, price=True, message="No nonstop flights found. Showing flights with stops.")   

            return redirect(url_for('prices', username=username, price=float(data[username]["price"]) ))
        else:
            print("ran")
            return render_template("flight_ui.html", nostop=False, price = False)
    
    return render_template("flight_ui.html", nostop=True)
    
@app.route('/pricing/<username>/<price>')
def prices(username, price):
    price_float = float(price)
    print(f"{price_float} : {type(price_float)}")
    cons = main.get_flight_data()
    contents = main.pricing(cons, price_float)
    if contents:
        prices = [price["price"] for price in contents]
        flights = [deats["data"] for deats in contents]
        data = {key:value for key,value in enumerate(flights)}

        return render_template("prices.html", data= True, details=contents, prices=prices, flights=data, username=username)
    
    return render_template("prices.html", data= False)

if __name__ == "__main__":
    app.run(debug=True, port=5001)