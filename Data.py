from flask import Flask, render_template, request
from google_play_scraper import app as gp_app, reviews, permissions, search, Sort

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None

    if request.method == "POST":
        app_id = request.form.get("app_id").strip()
        if not app_id:
            error = "Please enter an App ID!"
        else:
            try:
                result1 = gp_app(app_id)  # Fixed conflict
                result2, _ = reviews(app_id, lang="en", country="us", sort=Sort.NEWEST, count=5)
                app_permissions = permissions(app_id)
                search_results = search(result1['title'], lang="en", country="us")

                data = {
                    "title": result1["title"],
                    "score": result1["score"],
                    "installs": result1["installs"],
                    "url": result1["url"],
                    "reviews": result2[:5],
                    "permissions": list(app_permissions.keys())[:5],
                    "related_apps": search_results[:5]
                }
            except Exception as e:
                error = f"Error fetching data: {e}"

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
