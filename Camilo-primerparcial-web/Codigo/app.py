from flask import Flask, request, jsonify
import sqlite3
from os import path

from PersonaModelo import *
from LoteModelo import *

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)

    return connection


app = Flask(__name__)

conn = create_connection(path.join("database.db"))
cursor = conn.cursor()

#Rutas
@app.route('/venta',methods=['POST'])
def RegistrarVenta():
    request_json = request.get_json()
    cedula_responsable = request_json.get('responsable')
    numero_lote = request_json.get('lote')
    unidades_vendidas = request_json.get('unidadesVendidas')

    persona = GetFromCedula(conn, cedula_responsable)
    if persona == None:
        return 'Error'

    lote = GetFromNumeroLote(conn, numero_lote)
    if lote == None:
        return 'Error'

    if(lote.Responsable.Cedula != persona.Cedula):
        return 'Error'

    if not lote.Vender(unidades_vendidas):
        return 'Error'

    return 'OK'

@app.route('/cultivo/<lote>')
def GetCultivoLote(lote):
    lote = int(lote)

    cursor.execute("SELECT * FROM Lote WHERE NumeroLote=?", (lote,))
    lote = cursor.fetchall()
    if lote == None or len(lote) <= 0:
        return 'Error'

    lote = CreateLote(conn, lote[0])

    return jsonify(
        cultivo = lote.Cultivo,
        inventario = lote.Inventario
    )

@app.route('/responsable/<lote>')
def GetResponsableLote(lote):
    lote = int(lote)

    cursor.execute("SELECT * FROM Lote WHERE NumeroLote=?", (lote,))
    lote = cursor.fetchall()
    if lote == None or len(lote) <= 0:
        return 'Error'

    lote = CreateLote(conn, lote[0])
    responsable = lote.Responsable

    return jsonify(
        cedula=responsable.Cedula,
        nombre=responsable.Nombre,
        apellido=responsable.Apellido,
        telefono = responsable.Telefono
    )
    
