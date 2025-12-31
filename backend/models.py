from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ========== Model 1: Voiture ==========
class Voiture(db.Model):
    __tablename__ = 'voitures'
    
    # Columns
    num_imma = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    kilometrage = db.Column(db.Integer, default=0)
    etat = db.Column(db.String(20), default='disponible')
    prix_location = db.Column(db.Float, nullable=False)
    id_locataire = db.Column(db.Integer, db.ForeignKey('locataires.id_loc'), nullable=True)
    
    # Convert to dict (للـ JSON)
    def to_dict(self):
        return {
            'num_imma': self.num_imma,
            'marque': self.marque,
            'modele': self.modele,
            'kilometrage': self.kilometrage,
            'etat': self.etat,
            'prix_location': self.prix_location,
            'id_locataire': self.id_locataire
        }

# ========== Model 2: Locataire ==========
class Locataire(db.Model):
    __tablename__ = 'locataires'
    
    # Columns
    id_loc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    
    # Relationship
    voitures = db.relationship('Voiture', backref='locataire_obj', lazy=True)
    
    # Convert to dict
    def to_dict(self):
        return {
            'id_loc': self.id_loc,
            'nom': self.nom,
            'prenom': self.prenom,
            'adresse': self.adresse
        }
