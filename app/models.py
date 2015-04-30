# -*- coding: utf-8 -*-
from datetime import datetime
from app.extensions import db
from app.messages import USR_NOTACTIVE


class Bruker(db.Model):
    __tablename__ = 'bruker'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True)
    passord = db.Column(db.String(30))
    fornavn = db.Column(db.String(30))
    etternavn = db.Column(db.String(30))
    telefon = db.Column(db.Integer)
    status = db.Column(db.String(30))
    registrert = db.Column(db.DateTime)

    def __init__(self, email, passord, fornavn, etternavn, status, telefon):
        self.email = email
        self.passord = passord
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.telefon = telefon
        self.status = status
        self.registrert = datetime.now()

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.status == USR_NOTACTIVE:
            return False
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Bruker %r>' % self.email


class Ordre(db.Model):
    __tablename__ = 'ordre'
    id = db.Column(db.Integer, primary_key=True)
    bruker_id = db.Column(db.Integer, db.ForeignKey('bruker.id'))
    dato = db.Column(db.DateTime, default=datetime.now())
    sum = db.Column(db.Float)

    def __init__(self, bruker_id, sum):
        self.bruker_id = bruker_id
        self.sum = sum

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Ordre %r>' % self.id


class Ski(db.Model):
    __tablename__ = 'ski'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(30))
    beskrivelse = db.Column(db.String(200))
    storrelse = db.Column(db.Integer)
    minalder = db.Column(db.Integer)
    maksalder = db.Column(db.Integer)
    pris = db.Column(db.Integer)

    def __init__(self, navn, beskrivelse, storrelse, minalder, maksalder, pris):

        self.navn = navn
        self.beskrivelse = beskrivelse
        self.storrelse = storrelse
        self.minalder = minalder
        self.maksalder = maksalder
        self.pris = pris

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Ski %r>' % self.id


class Heiskort(db.Model):
    __tablename__ = 'heiskort'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(30))
    beskrivelse = db.Column(db.String(200))
    pris = db.Column(db.Integer)

    def __init__(self, navn, beskrivelse, pris):
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.pris = pris

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Heiskort %r>' % self.id


class Ordre_Heiskort(db.Model):
    __tablename__ = 'ordre_heiskort'
    id = db.Column(db.Integer, primary_key=True)
    ordre_id = db.Column(db.Integer, db.ForeignKey('ordre.id'))
    heis_id = db.Column(db.Integer, db.ForeignKey('heiskort.id'))

    def __init__(self, ordre_id, heis_id):
        self.ordre_id = ordre_id
        self.heis_id = heis_id

    def __repr__(self):
        return '<Ordre_Heiskort %s - %r>' % (self.ordre_id, self.heis_id)


class Ordre_Ski(db.Model):
    __tablename__ = 'ordre_ski'
    id = db.Column(db.Integer, primary_key=True)
    ordre_id = db.Column(db.Integer, db.ForeignKey('ordre.id'))
    ski_id = db.Column(db.Integer, db.ForeignKey('ski.id'))

    def __init__(self, ordre_id, ski_id):
        self.ordre_id = ordre_id
        self.ski_id = ski_id

    def __repr__(self):
        return '<Ordre_Ski %s - %r>' % (self.ordre_id, self.ski_id)


class Handleliste():
    id = None
    navn = None
    beskrivelse = None
    pris = None
    periode = None

    def __init__(self, id=None, navn=None, beskrivelse=None, pris=None, periode=None):
        self.id = id
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.pris = pris
        self.periode = periode


# en funksjon for å sett inn data når d ikke eksisterer en DB fra førr
def sett_data():
    ski = [Ski('Dynastar 300', 'Perfekt for den som liker litt fart.', 170, 12, 15, 50),
           Ski('GoPro 1337', 'For den litt mer vant aakeren, godt engnet for dem som liker snowparken.', 200, 18, 25, 80),
           Ski('NoGoPro', 'Ikke aakt ski tidliger? Da er dette pakken for deg.', 120, 14, 18, 65),
           Ski('MuchGo SuchShow 15', 'Aakt ski siden barnsbein sa du? Da er dette pakken for deg.', 160, 15, 20, 70),
           Ski('2fast 2furious', 'Styrtlopp? Kjappere enn lyset? Jajamensan, dette er den perfekte pakken for deg.', 110, 4, 7, 45)]

    heiskort = [Heiskort('Dagskort', 'Gjelder fra aapning- til stengningstid.', 170),
                Heiskort('Ukeskort', 'Gjelder fra Mandag til Fredag.,', 1275),
                Heiskort('Sesongkort', 'Gjelder fra Desember til April.', 6550)]

    for s in ski:
        db.session.add(s)

    for h in heiskort:
        db.session.add(h)

    db.session.commit()
    return True