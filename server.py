from flask import Flask, request, render_template, redirect, make_response, Markup
import requests
import vymgmt

vyos = vymgmt.Router('10.0.10.2', 'vyos', password='vyos', port=22)

router = "http://10.0.10.2:8000"

app = Flask(__name__)

@app.route("/")
def route_index():
    print("Running IP summary...")
    output = requests.get(router + "/show ip bgp summary").text.split("\n\n")[1].strip()
    print("DONE")

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
                                <button class="btn btn-danger m-1">Restart</button>
                                <button class="btn btn-danger m-1">Down</button>
                            </td>
                        </tr>
                        """

    return render_template("dashboard.html", peers=Markup(peers_html))


# Add a new peer
@app.route("/peer", methods=["POST"])
def route_peer():
    try:
        asn = request.form["asn"]
        name = request.form["name"]
        address = request.form["address"]
        group = request.form["group"]
        max_ipv4 = request.form["max-prefixes-ipv4"]
        max_ipv6 = request.form["max-prefixes-ipv6"]
        filter = request.form["filter"]
    except KeyError:
        return redirect("/")
    else:
        vyos.login()
        vyos.configure()
        vyos.set("protocols bgp 1 neighbor " + address + " remote-as " + str(asn))
        vyos.set("protocols bgp 1 peer-group " + group)
        vyos.set("protocols bgp 1 neighbor " + address + " peer-group " + group)
        vyos.commit()
        vyos.save()
        vyos.exit()
        vyos.logout()

        return redirect("/")

app.run("localhost", port=8000, debug=True)
