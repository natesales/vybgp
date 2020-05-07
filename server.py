from flask import Flask, request, render_template, redirect, make_response, Markup
import requests
from vyos import Router

asn = 34553
vyos = Router("10.0.10.2")

app = Flask(__name__)

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

app.run("localhost", port=8000, debug=True)
