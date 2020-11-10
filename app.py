from karaoke_online_hakaton import create_app
from flask import url_for
from flask_security import roles_required

app = create_app(debug=True)

@app.before_first_request
def restrict_admin_url():
    endpoint = "admin.index"
    url = url_for(endpoint)
    admin_index = app.view_functions.pop(endpoint)

    @app.route(url, endpoint=endpoint)
    @roles_required('admin')
    def secure_admin_index():
        return admin_index()



if __name__ == "__main__":
    app.run()