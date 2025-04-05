from installrequirements import install_requirements

# Instala os requisitos necessários para a aplicação
install_requirements()

from ui import MapApp

if __name__ == '__main__':
    app = MapApp()
    app.run()