from flask import Flask, render_template, request, session, redirect

import more_itertools

import altair as alt
import pandas as pd


alt.data_transformers.disable_max_rows()


app = Flask(__name__)

# These are read-only GLOBAL variables.
council = pd.read_csv("data/esb_att.csv")  # From the cleaned CSV.
county = sorted(council['County Councils'].unique())  # The list of Council Countys.
df1 = pd.melt(council,["County Councils"], var_name = 'Date' , value_name = 'count')
df1["Date"] = pd.to_datetime(df1["Date"])


print(df1.shape)  # This is the size of the DataFrame, rows by columns.


def produce_table(county, size=5):
    output = "<table>"
    for sample in more_itertools.chunked(county, size):
        # sample is the next 5 countys
        output += "<tr>"
        for s in sample:
            output += f"<td><input type='checkbox' name='{s}' value='{s}'>{s}</td>"
        output += "</tr>"
    output += "</table>"
    return output


@app.route("/")
@app.route("/county")
def show_county():
    the_table = produce_table(county, 5)
    return render_template("checks.html", data=the_table)


@app.route("/processchecks", methods=["POST"])
def process_checks():
    ## print('*'*60)
    ## print(request.form)  # This gets at the FORM data.
    ## print(list(request.form.keys()))
    session["selection"] = list(request.form.keys())
    ## print('*'*60)
    return redirect("/showdata")


@app.route("/showdata")
def display_session():
    # Extract only that data which is included in the list of selected stocks.
    df = pd.concat(
        df1[df1['County Councils'] == sample] for sample in session["selection"]
    )

    print(df.shape)  # This is the size of the DataFrame, rows by columns.

    # Let's produce the "untidy" dataframe from the filtered data using the selected list of stocks.
    stats = pd.concat(
        (
            df[df["County Councils"] == sample]
            .describe()
            .rename({"count": sample}, axis="columns")
            for sample in session["selection"]
        ),
        axis="columns",
    )
    table = stats.to_html()
    return render_template("untidy.html", data=table)


brush = alt.selection(type='interval')

@app.route("/visual")
def display_the_plot():
    df = pd.concat(
        df1[df1['County Councils'] == sample] for sample in session["selection"]
    )
    ## print(df.shape)
    ## print(session["selection"])

    plot = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("Date", title="Year"),
            y=alt.Y("count", title="ESB Connections"),
            color="County Councils",
        )
    )
    plot.save("templates/plot.html")
    return render_template("plot.html")


@app.route("/visual1")
def display_the_plot1():
    df = pd.concat(
        df1[df1['County Councils'] == sample] for sample in session["selection"]
    )


    plot1 = (
	alt.Chart(df).mark_point().encode(
        	x=alt.X(
        	"Date", 
        	title="Year",
        	),
        	 y=alt.Y(
        	"count",
        	title="ESB Connections",
    	),
    	color=alt.condition(brush, 'County Councils', alt.value('grey'))
	).add_selection(brush)
    )
    plot1.save("templates/plot1.html")
    return render_template("plot1.html")


@app.route("/visual2")
def display_the_plot2():
    df = pd.concat(
        df1[df1['County Councils'] == sample] for sample in session["selection"]
    )


    plot2 = (	
	alt.Chart(df).mark_bar().encode(
    		x=alt.X(
       	        "Date", 
        	title="Years",
    		),
    		y=alt.Y(
        	"count",
        	title="ESB Connections",
    	),
    	color='County Councils',
    	column='County Councils:N'
    )
    )
    plot2.save("templates/plot2.html")
    return render_template("plot2.html")






app.secret_key = ".v/vndfl/n/dlfkn/ldfkn/ldkngLKN"


if __name__ == "__main__":
    app.run(debug=True)
