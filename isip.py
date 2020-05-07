from flask import Flask, render_template, request
import ipaddress
import requests

app = Flask(__name__, template_folder=".")

def run(query):
	return requests.get("http://10.0.10.2:8000/" + query).text.strip()

def validate(ip):
	try:
		ip = ipaddress.ip_address(ip)
	except ValueError:
		return False
	else:
		return str(ip)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template("index.html")
	elif request.method == "POST":
		command = request.form["command"]
		arg = request.form["arg"]

		if command == "ping":
			if validate(arg):
				output = run("ping " + arg + " count 1")
			else:
				output = "Invalid query."

			return render_template("index.html", output=output)

		elif command == "traceroute":
			if validate(arg):
				output = run("traceroute " + arg)
			else:
				output = "Invalid query."

			return render_template("index.html", output=output)

		elif command == "show-ip-bgp-neighbor":
			if validate(arg):
				output = run("show ip bgp neighbor " + arg)
			else:
				output = "Invalid query."

			return render_template("index.html", output=output)

		elif command == "show-ip-bgp-summary":
			return render_template("index.html", output=run("show ip bgp summary"))

		else:
			return render_template("index.html", output="Please select a command.")

app.run("localhost", port=8000)
