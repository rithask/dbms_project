from flask import Flask, render_template, request
import services

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        print(request.form)
        register_number = request.form['registerNumber']
        dob = request.form['dob']
        sem = request.form['semester']
    
        # Call the service to get the result
        result = services.fetch_result(register_number, dob, sem)

        # Check if the request was successful
        if result.status_code == 200:
            # Extract JSON data from the response
            json_data = result.json()

            # Purify the result
            purified_data = services.purify_details(json_data)
            purified_result = purified_data['resultDetails']
            
            return render_template("result.html", data=purified_data, result=purified_result)
        else:
            # Handle the error or return an error message
            return f"Failed to fetch data. Status code: {result.status_code}"
