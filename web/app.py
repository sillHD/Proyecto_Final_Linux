from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

state = {
    "is_on": False,
    "duty": 50
}

@app.route("/")
def index():
    return render_template("index.html", state=state)

@app.route("/on", methods=["POST"])
def turn_on_route():
    state["is_on"] = True
    print("[WEB] Simulado: encender luces")
    return redirect(url_for("index"))

@app.route("/off", methods=["POST"])
def turn_off_route():
    state["is_on"] = False
    print("[WEB] Simulado: apagar luces")
    return redirect(url_for("index"))

@app.route("/set_pwm", methods=["POST"])
def set_pwm_route():
    duty = int(request.form.get("duty", 50))
    state["duty"] = duty
    print(f"[WEB] Simulado: PWM = {duty}%")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
