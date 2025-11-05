from flask import Flask, render_template, request, redirect, url_for, jsonify
from connection import *
from controllers import *


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def records():

    # Obtener datos de la tabla "Record"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Record ORDER BY id_record DESC")
        records = cursor.fetchall()

    # Chequear si se presionó boton de eliminar (delete) o editar (edit) en cualquier registro
    if request.method == "POST":
        action = request.form["action"]
        idRecord = int(request.form["action_idRecord"])

        if action == "Delete":
            with get_connection() as conn:
                cursor = conn.cursor()

                PATH_QRCODE = os.path.join(
                    "static", "img", "QR_Codes", f"qr_{idRecord}.png"
                )
                os.remove(PATH_QRCODE)

                cursor.execute("DELETE FROM Record WHERE id_record = ?", (idRecord,))
            conn.commit()
            return redirect("/")

        elif action == "Edit":
            return redirect(f"/editRecord/{idRecord}")

    return render_template("records.html", records=records)


@app.route("/editRecord/<int:id_record>", methods=["POST", "GET"])
def edit_record(id_record: int):
    with get_connection() as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            chemical_name = request.form["chemical_name"]
            chemical_formula = request.form["chemical_formula"]
            chemical_description = request.form["chemical_description"]

            cursor.execute(
                """UPDATE Record
                            SET name_chemical = ?, formule = ?, description = ?
                            WHERE id_record = ?""",
                (chemical_name, chemical_formula, chemical_description, id_record),
            )
            conn.commit()

            return redirect(f"/#record-{id_record}")
    return render_template("editRecord.html", id_record=id_record)


@app.route("/addRecord", methods=["GET", "POST"])
def addRecord():
    if request.method == "POST":

        chemical_name = request.form["chemical_name"]
        chemical_formula = request.form["chemical_formula"]
        chemical_description = request.form["chemical_description"]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT INTO Record (name_chemical, formule, description) VALUES (
                                (?),
                                (?),
                                (?)
                            );""",
                (chemical_name, chemical_formula, chemical_description),
            )
            conn.commit()

            id_record = cursor.lastrowid
            qr_link = generate_qr(id_record)

            cursor.execute(
                "UPDATE Record SET qr_link = ? WHERE id_record = ?",
                (qr_link, id_record),
            )
            conn.commit()

        return redirect("/")
    return render_template("addRecord.html")


@app.route("/scanner", methods=["POST"])
def scanner():
    if request.method == "POST":
        data = request.get_json()
        qr_text = data.get("qr_text")
        print(qr_text)
        return redirect(qr_text)

    return render_template("scanner.html")


if __name__ == "__main__":
    app.run(debug=True)
