from datetime import datetime
from app.dao.ColisDAO import ColisDAO
import uuid
import qrcode
import os

QR_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr')

class ColisService:
    def __init__(self):
        self.dao = ColisDAO()

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
               destinataire_id=None, code_barres=None, commentaire=None):
        if not bon_commande_id:
            raise ValueError("bon_commande_id est requis")
        if not numero_suivi:
            numero_suivi = self.generate_numero_suivi()

        # Créer le colis en base
        colis = self.dao.create(
            bon_commande_id, numero_suivi, statut_libelle,
            destinataire_id, code_barres, commentaire
        )
        if not colis:
            raise ValueError("Erreur création colis")

        # Générer le QR code
        qr_image_path, qr_payload = self._generer_qr(colis.id_colis, numero_suivi)

        # Mettre à jour en base
        self.dao.update_qr(colis.id_colis,
                        qr_payload=qr_payload,
                        qr_image_path=qr_image_path)

        return self.dao.get_by_id(colis.id_colis)

    def receptionner(self, id_colis, agent_id):
        self.get_by_id(id_colis)
        return self.dao.receptionner(id_colis, agent_id)

    def retirer(self, id_colis):
        self.get_by_id(id_colis)
        return self.dao.remettre_destinataire(id_colis)

    def signaler_incident(self, id_colis, commentaire=None):
        self.get_by_id(id_colis)
        return self.dao.signaler_incident(id_colis, commentaire)

    def transferer_iut(self, id_colis):
        self.get_by_id(id_colis)
        return self.dao.transferer_iut(id_colis)

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

        qr_payload = numero_suivi  # ce qui est encodé dans le QR

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

        # Chemin relatif stocké en base — accessible via /static/qr/<id>.png
        qr_image_path = f"static/qr/{filename}"

        return qr_image_path, qr_payload
    
    def get_by_qr_payload(self, qr_payload):
        colis = self.dao.get_by_qr_payload(qr_payload)
        if not colis:
            raise ValueError(f"QR payload '{qr_payload}' introuvable")
        return colis