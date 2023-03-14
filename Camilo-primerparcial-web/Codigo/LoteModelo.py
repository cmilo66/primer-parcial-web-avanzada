from PersonaModelo import *

class LoteModelo:
    NumeroLote = None
    NIT = None
    Responsable = None
    Cultivo = None
    Inventario = None

    __conn = None
    __cursor = None

    def __init__(self, conn):
        self.__conn = conn
        self.__cursor = conn.cursor()

    
    def Vender(self, unidades_venta):
        if self.Inventario < unidades_venta:
            return False

        inventario = self.Inventario - unidades_venta

        self.__cursor.execute("UPDATE Lote SET ExistenciasCultivo=? WHERE NumeroLote=?", (inventario, self.NumeroLote))
        self.__conn.commit()

        #actualiza al final en caso de error
        self.Inventario = inventario
        return True


def CreateLote(conn, data):
    lote = LoteModelo(conn)

    lote.NumeroLote = data[0]
    lote.NIT = data[1]
    lote.Responsable = GetFromCedula(conn, data[2])
    lote.Cultivo = data[3]
    lote.Inventario = data[4]

    return lote

def GetFromNumeroLote(conn, lote):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Lote WHERE NumeroLote=?", (lote,))
    lote = cursor.fetchall()
    if lote == None or len(lote) <= 0:
        return None

    return CreateLote(conn, lote[0])