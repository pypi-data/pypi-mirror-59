import click
from .app import commands as app
from .sandbox import commands as sandbox
from .user import commands as user
from .report import commands as report

# import logging
# logger = logging.getLogger('veracode')

@click.group()
def main():
    pass

main.add_command(app.app)
main.add_command(sandbox.sandbox)
main.add_command(user.user)
main.add_command(report.report)

if __name__ == '__main__':
    main()
