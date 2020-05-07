import vymgmt
import re

class Router:
    def __init__(self):

vyos = vymgmt.Router("10.0.10.2", "vyos", "vyos", port=22)
vyos.login()
output = vyos.run_op_mode_command("show ip bgp summary")
vyos.logout()

output = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', output)

for chr in ("\r", "\x1b=", "\x1b>", " \x08"):
    output = output.replace(chr, "")

output = output.split("\n\n")[2]

for peer in output.split("\n")[1:]:
    elements = peer.split(" ")
    while "" in elements:
        elements.remove("")

    print(elements)