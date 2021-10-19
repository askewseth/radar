from flask import Flask, render_template, send_file, request, redirect, url_for, send_from_directory
import csv
import functions as fns 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>This is the radar!</p>"

@app.route('/js/<path:path>')
def send_js(path):
    print("RETURNING FROM DIRECORY: ", path)
    print(send_from_directory('js', path))
    return send_from_directory('js', path) 

@app.route("/download")
def download_data_page():
    data_path = "./data/data.csv"
    return send_file(data_path, as_attachment=True)

# TODO: SETH: 
# Need to have one endpoint that takes
# in from the url parameters:
# * page number
# * page length
# * filter under
# * filter over

@app.route("/data")
def data_page():
    # pull in the url parameters
    page_number = request.args.get('page_number', None)
    page_length = request.args.get('page_length', None)
    print("Num: {}; Len: {}".format(page_number, page_length))

    if page_number is None or page_length is None:
        print("Got none for page number or length")
        return redirect(url_for("data_page", page_number="1", page_length="30"))

    # get the data and process it
    raw_data = fns.get_raw_data()
    processed_data = fns.process_data(raw_data)
    paginated_data, number_of_pages = fns.paginate_data(processed_data, page_number, page_length)
    # print("Paginated: ", paginated_data)

    # get stats like # of people over limit
    speed_limit = 25 
    stats = fns.get_stats(processed_data, speed_limit)
    
    # Pass the data to the front end
    data = {
        "rows": paginated_data,
        "len": len(processed_data),
        "stats": stats,
        "page_number": page_number,
        "page_length": page_length,
        "number_of_pages": number_of_pages
    }

    return render_template("data.html", data=data)

if __name__ == "__main__":
    # port = "5000"
    port = "80"
    app.run(host="0.0.0.0", port=port)

