from app import app
from app.dao.DemandeAchatDAO import DemandeAchatDAO

with app.app_context():

    dao = DemandeAchatDAO()

    print("\n ===== Test DemandeDAO =====\n")

    ## CREATE DEMANDE 

    print("1. CREATE DEMANDE")

    try:
        dm = dao.create(
            objet="achat ecran",
            demandeur_id=2,
            departement_id=1,
            description=" besoin de 10 ecran pour tp",
            montant_estime=15000
        )

        print("Demande créé")
        print(dm.to_dict())
    except Exception as e:
        print("Erreur :", e)
        
    id_demande = dm.id_demande if dm else None
    
    ## Approuver 

    try:
        approuvee = dao.approuver(
            id_demande,
            commentaire="Validé par le responsable"
        )

        print(approuvee.to_dict())

    except Exception as e:
        print("Erreur approbation :", e)