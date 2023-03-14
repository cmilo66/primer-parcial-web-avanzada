import sqlite3

class PersonaModelo:
    conn = None
    Cedula = None
    Nombre = None
    Apellido = None
    Telefono = None

    def __init__(self, conn):
        self.conn = conn




def CreatePersona(conn, data):
    persona = PersonaModelo(conn)

    persona.Cedula = data[0]
    persona.Nombre = data[1]
    persona.Apellido = data[2]
    persona.Telefono = data[3]
    
    return persona

def GetFromCedula(conn, cedula):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Persona WHERE Cedula=?", (cedula,))
    persona = cursor.fetchall()
    if persona == None or len(persona) <= 0:
        return None

    return CreatePersona(conn, persona[0])