from flask import Blueprint, request, jsonify
from models import db, Voiture, Locataire

# Create Blueprints
voitures_bp = Blueprint('voitures', __name__)
locataires_bp = Blueprint('locataires', __name__)
locations_bp = Blueprint('locations', __name__)

# ==================== VOITURES ROUTES ====================

# GET all voitures
@voitures_bp.route('/api/voitures', methods=['GET'])
def get_voitures():
    """Get all voitures"""
    try:
        voitures = Voiture.query.all()
        return jsonify([v.to_dict() for v in voitures]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET voiture by ID
@voitures_bp.route('/api/voitures/<int:num_imma>', methods=['GET'])
def get_voiture(num_imma):
    """Get a single voiture by ID"""
    try:
        voiture = Voiture.query.get_or_404(num_imma)
        return jsonify(voiture.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Voiture not found'}), 404

# POST create voiture
@voitures_bp.route('/api/voitures', methods=['POST'])
def create_voiture():
    """Create a new voiture"""
    try:
        data = request.json
        
        # Validation
        if not data.get('num_imma') or not data.get('marque') or not data.get('modele') or not data.get('prix_location'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if voiture already exists
        existing = Voiture.query.get(data['num_imma'])
        if existing:
            return jsonify({'error': 'Voiture already exists'}), 400
        
        # Create new voiture
        nouvelle_voiture = Voiture(
            num_imma=data['num_imma'],
            marque=data['marque'],
            modele=data['modele'],
            kilometrage=data.get('kilometrage', 0),
            prix_location=data['prix_location'],
            etat='disponible'
        )
        
        db.session.add(nouvelle_voiture)
        db.session.commit()
        
        return jsonify(nouvelle_voiture.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# PUT update voiture
@voitures_bp.route('/api/voitures/<int:num_imma>', methods=['PUT'])
def update_voiture(num_imma):
    """Update a voiture"""
    try:
        voiture = Voiture.query.get_or_404(num_imma)
        data = request.json
        
        # Update fields
        if 'marque' in data:
            voiture.marque = data['marque']
        if 'modele' in data:
            voiture.modele = data['modele']
        if 'kilometrage' in data:
            voiture.kilometrage = data['kilometrage']
        if 'prix_location' in data:
            voiture.prix_location = data['prix_location']
        
        db.session.commit()
        return jsonify(voiture.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE voiture
@voitures_bp.route('/api/voitures/<int:num_imma>', methods=['DELETE'])
def delete_voiture(num_imma):
    """Delete a voiture"""
    try:
        voiture = Voiture.query.get_or_404(num_imma)
        
        # Check if voiture is currently rented
        if voiture.etat == 'louée':
            return jsonify({'error': 'Cannot delete a rented voiture'}), 400
        
        db.session.delete(voiture)
        db.session.commit()
        return jsonify({'message': 'Voiture deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== LOCATAIRES ROUTES ====================

# GET all locataires
@locataires_bp.route('/api/locataires', methods=['GET'])
def get_locataires():
    """Get all locataires"""
    try:
        locataires = Locataire.query.all()
        return jsonify([l.to_dict() for l in locataires]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET locataire by ID
@locataires_bp.route('/api/locataires/<int:id_loc>', methods=['GET'])
def get_locataire(id_loc):
    """Get a single locataire by ID"""
    try:
        locataire = Locataire.query.get_or_404(id_loc)
        return jsonify(locataire.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Locataire not found'}), 404

# POST create locataire
@locataires_bp.route('/api/locataires', methods=['POST'])
def create_locataire():
    """Create a new locataire"""
    try:
        data = request.json
        
        # Validation
        if not data.get('nom') or not data.get('prenom') or not data.get('adresse'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create new locataire
        nouveau_locataire = Locataire(
            nom=data['nom'],
            prenom=data['prenom'],
            adresse=data['adresse']
        )
        
        db.session.add(nouveau_locataire)
        db.session.commit()
        
        return jsonify(nouveau_locataire.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# PUT update locataire
@locataires_bp.route('/api/locataires/<int:id_loc>', methods=['PUT'])
def update_locataire(id_loc):
    """Update a locataire"""
    try:
        locataire = Locataire.query.get_or_404(id_loc)
        data = request.json
        
        # Update fields
        if 'nom' in data:
            locataire.nom = data['nom']
        if 'prenom' in data:
            locataire.prenom = data['prenom']
        if 'adresse' in data:
            locataire.adresse = data['adresse']
        
        db.session.commit()
        return jsonify(locataire.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE locataire
@locataires_bp.route('/api/locataires/<int:id_loc>', methods=['DELETE'])
def delete_locataire(id_loc):
    """Delete a locataire"""
    try:
        locataire = Locataire.query.get_or_404(id_loc)
        
        # Check if locataire has rented voitures
        voitures_louees = Voiture.query.filter_by(id_locataire=id_loc).all()
        if voitures_louees:
            return jsonify({'error': 'Cannot delete locataire with rented voitures'}), 400
        
        db.session.delete(locataire)
        db.session.commit()
        return jsonify({'message': 'Locataire deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== LOCATIONS ROUTES ====================

# POST louer une voiture
@locations_bp.route('/api/locations/louer', methods=['POST'])
def louer_voiture():
    """Louer une voiture à un locataire"""
    try:
        data = request.json
        
        # Validation
        if not data.get('num_imma') or not data.get('id_locataire'):
            return jsonify({'error': 'Missing num_imma or id_locataire'}), 400
        
        num_imma = data['num_imma']
        id_locataire = data['id_locataire']
        
        # Check if voiture exists
        voiture = Voiture.query.get(num_imma)
        if not voiture:
            return jsonify({'error': 'Voiture not found'}), 404
        
        # Check if voiture is available
        if voiture.etat == 'louée':
            return jsonify({'error': 'Voiture is already rented'}), 400
        
        # Check if locataire exists
        locataire = Locataire.query.get(id_locataire)
        if not locataire:
            return jsonify({'error': 'Locataire not found'}), 404
        
        # Louer la voiture
        voiture.etat = 'louée'
        voiture.id_locataire = id_locataire
        
        db.session.commit()
        
        return jsonify({
            'message': 'Voiture louée avec succès!',
            'voiture': voiture.to_dict(),
            'locataire': locataire.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# POST rendre une voiture
@locations_bp.route('/api/locations/rendre', methods=['POST'])
def rendre_voiture():
    """Rendre une voiture (fin de location)"""
    try:
        data = request.json
        
        # Validation
        if not data.get('num_imma'):
            return jsonify({'error': 'Missing num_imma'}), 400
        
        num_imma = data['num_imma']
        
        # Check if voiture exists
        voiture = Voiture.query.get(num_imma)
        if not voiture:
            return jsonify({'error': 'Voiture not found'}), 404
        
        # Check if voiture is rented
        if voiture.etat == 'disponible':
            return jsonify({'error': 'Voiture is not rented'}), 400
        
        # Save locataire info before clearing
        locataire = Locataire.query.get(voiture.id_locataire)
        
        # Rendre la voiture
        voiture.etat = 'disponible'
        voiture.id_locataire = None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Voiture rendue avec succès!',
            'voiture': voiture.to_dict(),
            'ancien_locataire': locataire.to_dict() if locataire else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET statistics
@locations_bp.route('/api/locations/stats', methods=['GET'])
def get_stats():
    """Get statistics about voitures and locations"""
    try:
        # Count voitures
        total_voitures = Voiture.query.count()
        voitures_disponibles = Voiture.query.filter_by(etat='disponible').count()
        voitures_louees = Voiture.query.filter_by(etat='louée').count()
        
        # Count locataires
        total_locataires = Locataire.query.count()
        locataires_actifs = Locataire.query.join(Voiture, Voiture.id_locataire == Locataire.id_loc).count()
        
        # Get all rented voitures with locataires
        locations_actives = []
        voitures_louees_list = Voiture.query.filter_by(etat='louée').all()
        
        for voiture in voitures_louees_list:
            locataire = Locataire.query.get(voiture.id_locataire)
            locations_actives.append({
                'voiture': voiture.to_dict(),
                'locataire': locataire.to_dict() if locataire else None
            })
        
        stats = {
            'voitures': {
                'total': total_voitures,
                'disponibles': voitures_disponibles,
                'louees': voitures_louees
            },
            'locataires': {
                'total': total_locataires,
                'actifs': locataires_actifs
            },
            'locations_actives': locations_actives
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
