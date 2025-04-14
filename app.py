# Je NUTNÉ nainštalovať alíček: do konzoly napíšte "pip install flask"
from flask import Flask, request
import sqlite3
import hashlib
app = Flask(__name__)

# Pripojenie k databáze
def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')  # API endpoint
def index():
    # Úvodná stránka s dvoma tlačidami ako ODKAZMI na svoje stránky - volanie API nedpointu
    return '''
        <h1>Výber z databázy</h1>
        <a href="/kurzy"><button>Zobraz všetky kurzy</button></a>
        <a href="/treneri"><button>Zobraz všetkých trénerov</button></a>
        <a href="/miesta"><button>Zobraz všetky miesta</button></a>
        <a href="/maxkapacity"><button>Zobraz maximálnu kapacitu</button></a>
        <a href="/registracia"><button>Registruj</button></a>
        <hr>
        
    '''
@app.route('/maxkapacity') 
def zobraz_kapacity():
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sum(Max_pocet_ucastnikov) FROM Kurzy where Nazov_kurzu LIKE 'p%'")
    maxkapacity = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    vystup = "<h2>Zobraz maximálne kapacity:</h2>"
    for max_kapacita in maxkapacity:
        vystup += f"<p>{max_kapacita}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup


@app.route('/kurzy')  # API endpoint
def zobraz_kurzy():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    vystup = "<h2>Zoznam kurzov:</h2>"
    for kurz in kurzy:
        vystup += f"<p>{kurz}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup




@app.route('/treneri')  # API endpoint
def zobraz_trenerov():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis trénerov a ich kurzov
    vystup = "<h2>Zoznam trénerov a kurzov:</h2>"
    for trener in treneri:
        vystup += f"<p>{trener}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup


@app.route('/miesta') 
def zobraz_miesta():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT Nazov_miesta FROM Miesta")
    miesta = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    vystup = "<h2>Zoznam miest:</h2>"
    for miesto in miesta:
        vystup += f"<p>{miesto}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup


# STRÁNKA S FORMULÁROM NA REGISTRÁCIU TRÉNERA. Vráti HTML formulár s elementami
# Metóda je GET. (Predtým sme metódu nedefinovali. Ak žiadnu neuvedieme, automaticky je aj tak GET)
@app.route('/registracia', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''


# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hashovanie hesla
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)


