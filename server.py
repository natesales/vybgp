from flask import Flask, request, render_template, redirect, make_response, Markup
import requests
from vyos import Router
import ipaddress

asn = 34553
vyos = Router("10.0.10.2")

app = Flask(__name__)

def validate(ip):
	try:
		ip = ipaddress.ip_address(ip)
	except ValueError:
		return False
	else:
		return str(ip)

@app.route("/")
def route_index():
    try:
        output = vyos.op("show ip bgp summary").split("\n\n")[1].strip()
    except IndexError:
        peers_html = ""
    else:
        peers_html = ""
        for peer in output.split("\n")[1:]:
            elements = peer.split(" ")
            while "" in elements:
                elements.remove("")

            peers_html += """<tr>
                                <td class="align-middle"><a class="link-normal" target="_blank" href="https://bgp.tools/asn/""" + elements[2] + """">AS""" + elements[2] + """</a></td>
                                <td class="align-middle"><a class='link-normal' target='_blank'><i>Unknown</i></a></td>
                                <td class="align-middle">""" + elements[0] + """</td>
								<td class="align-middle">Internal</td>
                                <td class="align-middle">""" + elements[-1] + """</td>
                                <td class="align-middle">""" + elements[-2] + """</td>
                                <td class="align-middle pt-3">
                                    <button class="btn btn-danger m-1" onclick="window.location = '/delete?peer=""" + elements[0] + """'">Delete</button>
                                </td>
                            </tr>
                            """

    return render_template("dashboard.html", peers=Markup(peers_html))


# Add a new peer
@app.route("/peer", methods=["POST"])
def route_peer():
    try:
        _asn = request.form["asn"]
        name = request.form["name"]
        address = request.form["address"]
        max_ipv4 = request.form["max-prefixes-ipv4"]
        max_ipv6 = request.form["max-prefixes-ipv6"]
        filter = request.form["filter"]
    except KeyError:
        return redirect("/")
    else:
    	vyos.set("protocols bgp " + str(asn) + " neighbor " + address + " remote-as " + str(_asn))
		return redirect("/")

@app.route("/delete")
def delete():
    vyos.delete("protocols bgp " + str(asn) + " neighbor " + request.args.get("peer"))

    return redirect("/")

@app.route("/lg", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template("lg.html")
	elif request.method == "POST":
		command = request.form["command"]
		arg = request.form["arg"]

		if command == "ping":
			if validate(arg):
				output = vyos.op("ping " + arg + " count 1")
			else:
				output = "Invalid query."

			return render_template("lg.html", output=output)

		elif command == "traceroute":
			if validate(arg):
				output = vyos.op("traceroute " + arg)
			else:
				output = "Invalid query."

			return render_template("lg.html", output=output)

		elif command == "show-ip-bgp-neighbor":
			if validate(arg):
				output = vyos.op("show ip bgp neighbor " + arg)
			else:
				output = "Invalid query."

			return render_template("lg.html", output=output)

		elif command == "show-ip-bgp-summary":
			return render_template("lg.html", output=vyos.op("show ip bgp summary"))

		else:
			return render_template("lg.html", output="Please select a command.")


app.run("localhost", port=8000, debug=True)
