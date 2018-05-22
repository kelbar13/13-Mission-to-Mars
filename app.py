# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars = mongo.db.collection.find()
    
    print(mars)

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    data = scrape_mars.scrape()
    
    # Store results into a dictionary
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape
    
    # Insert Mars data into database
    mars.update({}, mars_data, upsert=True)
    print(mars_data)
    
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

