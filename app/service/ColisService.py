from datetime import datetime
import os
import uuid
import qrcode
from app.dao.ColisDAO import ColisDAO
from app.dao.EvenementColisDAO import EvenementColisDAO
from app.service.EvenementColisService import EvenementColisService

QR_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr')

class ColisService:

    def __init__(self, evenement_service=None):
        self.dao = ColisDAO()
        # Injection du service d'événements pour l'historisation automatique
        self.evenement_service = evenement_service or EvenementColisService()

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id_colis):
        colis = self.dao.get_by_id(id_colis)
        if not colis:
            raise ValueError(f"Colis {id_colis} introuvable")
        return colis

    def get_by_numero_suivi(self, numero_suivi):
        colis = self.dao.get_by_numero_suivi(numero_suivi)
        if not colis:
            raise ValueError(f"Numéro de suivi '{numero_suivi}' introuvable")
        return colis

    def get_by_destinataire(self, destinataire_id):
        return self.dao.get_by_destinataire(destinataire_id)

    def get_by_bon_commande(self, bon_commande_id):
        return self.dao.get_by_bon_commande(bon_commande_id)

    def create(self, bon_commande_id, numero_suivi=None, statut_libelle='recu_universite',
               destinataire_id=None, code_barres=None, commentaire=None, agent_id=None):
        if not bon_commande_id:
            raise ValueError("bon_commande_id est requis")
        if not numero_suivi:
            numero_suivi = self.generate_numero_suivi()

        # 1. Création initiale du colis
        colis = self.dao.create(
            bon_commande_id, numero_suivi, statut_libelle,
            destinataire_id, code_barres, commentaire
        )
        if not colis:
            raise ValueError("Erreur création colis")

        # 2. Génération du QR Code conforme à la nomenclature "COL:{id}:{suivi}"
        qr_image_path, qr_payload = self._generer_qr(colis.id_colis, numero_suivi)

        # 3. Mise à jour des informations QR
        self.dao.update_qr(colis.id_colis, qr_payload=qr_payload, qr_image_path=qr_image_path)

        # 4. Historisation de la création / première réception
        self.evenement_service.create(
            colis_id=colis.id_colis,
            action='scan_reception',
            statut_libelle=statut_libelle,
            utilisateur_id=agent_id,
            commentaire="Création et enregistrement initial du colis"
        )

        return self.dao.get_by_id(colis.id_colis)

    def receptionner(self, id_colis, agent_id):
        self.get_by_id(id_colis) # Validation de l'existence
        result = self.dao.receptionner(id_colis, agent_id)
        
        # Tracer le scan de réception
        self.evenement_service.create(
            colis_id=id_colis,
            action='scan_reception',
            statut_libelle='recu_universite',
            utilisateur_id=agent_id,
            localisation='Bureau Central Université'
        )
        return result

    def transferer_iut(self, id_colis, agent_id=None):
        self.get_by_id(id_colis)
        result = self.dao.transferer_iut(id_colis)
        
        # Tracer le transfert logistique
        self.evenement_service.create(
            colis_id=id_colis,
            action='transfert_iut',
            statut_libelle='transfere_iut',
            utilisateur_id=agent_id,
            localisation='Transit vers Bureau Postal IUT'
        )
        return result

    def retirer(self, id_colis, agent_id=None):
        self.get_by_id(id_colis)
        result = self.dao.remettre_destinataire(id_colis)
        
        # Tracer la remise finale en main propre
        self.evenement_service.create(
            colis_id=id_colis,
            action='remise_destinataire',
            statut_libelle='remis_destinataire',
            utilisateur_id=agent_id,
            commentaire='Remis en main propre au destinataire'
        )
        return result

    def signaler_incident(self, id_colis, commentaire=None, agent_id=None):
        # Correction du nom de la méthode : signaling_incident -> signaler_incident
        self.get_by_id(id_colis)
        result = self.dao.signaler_incident(id_colis, commentaire)
        
        # Tracer l'incident technique ou logistique
        self.evenement_service.create(
            colis_id=id_colis,
            action='incident',
            statut_libelle='incident',
            utilisateur_id=agent_id,
            commentaire=commentaire or "Incident signalé sur le colis"
        )
        return result

    def update(self, id_colis, **kwargs):
        self.get_by_id(id_colis)
        return self.dao.update(id_colis, **kwargs)

    def delete(self, id_colis):
        self.get_by_id(id_colis)
        return self.dao.delete(id_colis)

    def generate_numero_suivi(self):
        return f"COLIS-{uuid.uuid4().hex[:10].upper()}"

    def _generer_qr(self, id_colis, numero_suivi):
        os.makedirs(QR_DIR, exist_ok=True)

        # Alignement strict avec la nomenclature métier du schéma SQL
        qr_payload = f"COL:{id_colis}:{numero_suivi}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )
        qr.add_data(qr_payload)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"{id_colis}.png"
        filepath = os.path.join(QR_DIR, filename)
        img.save(filepath)

        qr_image_path = f"static/qr/{filename}"
        return qr_image_path, qr_payload
    
    def get_by_qr_payload(self, qr_payload):
        colis = self.dao.get_by_qr_payload(qr_payload)
        if not colis:
            raise ValueError(f"QR payload '{qr_payload}' introuvable")
        return colis