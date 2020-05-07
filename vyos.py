import re
import vymgmt


class Router:
    def __init__(self, host, user="vyos", pswd="vyos", port=22):
        self.router = vymgmt.Router(host, user, pswd, port)
        self.router.login()

    def __del__(self):
        self.router.exit()
        self.router.logout()

    @staticmethod
    def _sanitize(output):
        output = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', output)

        for chr in ("\r", "\x1b=", "\x1b>", " \x08"):
            output = output.replace(chr, "")

        return "\n".join(output.split("\n")[1:]).strip()

    def op(self, command):
        return self._sanitize(self.router.run_op_mode_command(command))

    def set(self, args):
        self.router.configure()
        output = self.router.set(args)
        self.router.commit()
        self.router.save()
        self.router.exit()
        return output

    def delete(self, args):
        self.router.configure()
        output = self.router.delete(args)
        self.router.commit()
        self.router.save()
        self.router.exit()
        return output
