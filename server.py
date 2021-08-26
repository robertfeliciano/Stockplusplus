from dashboard.app import app

unicorn = app.server

if __name__ == '__main__':
    app.run_server(debug = True)