from app import app
from app.service.UserService import UserService
from app.service.DepartementService import DepartementService
from app.service.FournisseurService import FournisseurService
from app.service.DemandeAchatService import DemandeAchatService
from app.service.DevisService import DevisService
from app.service.BonCommandeService import BonCommandeService
from app.service.ColisService import ColisService
from app.service.StatutColisService import StatutColisService
from app.service.NotificationService import NotificationService
from app.service.RoleService import RoleService

us = UserService()
ds = DepartementService()
fs = FournisseurService()
das = DemandeAchatService()
devs = DevisService()
bcs = BonCommandeService()
cs = ColisService()
scs = StatutColisService()
ns = NotificationService()
rs = RoleService()

def sep(titre):
    print(f"\n{'='*50}")
    print(f"  {titre}")
    print('='*50)

def get_or_create_user(full_name, email, password, role_id, departement_id):
    try:
        user = us.create_user(full_name, email, password, role_id, departement_id)
        print(f"  [créé] {email}")
        return user
    except ValueError:
        user = us.login(email, password)
        print(f"  [existant] {email}")
        return user

with app.app_context():

    sep("1. DONNÉES DE BASE")
    deps = ds.get_all()
    dep = deps[0] if deps else ds.create("Informatique", "0149403001", 50000)
    print(f"Département : {dep.to_dict()}")

    fournisseurs = fs.get_all()
    fournisseur = fournisseurs[0] if fournisseurs else fs.create("Tech Supplies", "Jean Dupont", "jean@tech.fr", "0123456789")
    print(f"Fournisseur : {fournisseur.to_dict()}")

    statuts = scs.get_all()
    statut = statuts[0] if statuts else scs.create("en_attente")
    print(f"Statut colis : {statut.to_dict()}")

    roles = rs.get_all()
    print(f"Rôles dispo : {[r.to_dict() for r in roles]}")

    # role_id réels depuis la BDD
    role_admin      = next(r.id_role for r in roles if r.libelle == 'admin')
    role_directeur  = next(r.id_role for r in roles if r.libelle == 'directeur')
    role_departement = next(r.id_role for r in roles if r.libelle == 'departement')

    demandeur = get_or_create_user("Alice Martin", "demandeur@sae.fr", "pass123", role_departement, dep.id_departement)
    print(f"Demandeur : {demandeur.to_dict()}")

    directeur = get_or_create_user("Bob Dupont", "directeur@sae.fr", "pass123", role_directeur, dep.id_departement)
    print(f"Directeur : {directeur.to_dict()}")

    admin = get_or_create_user("Admin", "admin@sae.fr", "admin123", role_admin, dep.id_departement)
    print(f"Admin : {admin.to_dict()}")

    sep("2. DEMANDE D'ACHAT")
    demande = das.create(
        objet="Achat de 10 écrans 27 pouces",
        demandeur_id=demandeur.id_utilisateur,
        departement_id=dep.id_departement,
        description="Pour les salles de TP",
        montant_estime=3500.0
    )
    print(f"Demande créée : {demande.to_dict()}")
    notifs = ns.get_by_utilisateur(directeur.id_utilisateur)
    print(f"Notifications directeur : {len(notifs)} notif(s)")

    sep("3. APPROBATION")
    demande_approuvee = das.approuver(demande.id_demande, commentaire="Budget OK")
    print(f"Statut demande : {demande_approuvee.statut}")
    notifs_demandeur = ns.get_by_utilisateur(demandeur.id_utilisateur)
    print(f"Notifications demandeur : {len(notifs_demandeur)} notif(s)")

    sep("4. DEVIS")
    devis = devs.create(
        fournisseur_id=fournisseur.id_fournisseur,
        createur_id=admin.id_utilisateur,
        objet="Devis écrans x10",
        montant_estime=3200.0
    )
    print(f"Devis créé : {devis.to_dict()}")
    devis_accepte = devs.accepter(devis.id_devis)
    print(f"Devis statut : {devis_accepte.statut}")

    sep("5. BON DE COMMANDE")
    bc = bcs.create(
        departement_id=dep.id_departement,
        fournisseur_id=fournisseur.id_fournisseur,
        createur_id=admin.id_utilisateur,
        devis_id=devis.id_devis,
        montant_estime=3200.0
    )
    print(f"BC créé : {bc.to_dict()}")
    bc_envoye = bcs.update_statut(bc.id_bon_commande, "en_cours")
    print(f"BC statut : {bc_envoye.statut}")

    sep("6. COLIS")
    colis = cs.create(
        bon_commande_id=bc.id_bon_commande,
        statut_id=statut.id_statut,
        numero_suivi="SUIVI-TEST-001",
        destinataire_id=demandeur.id_utilisateur
    )
    print(f"Colis créé : {colis.to_dict()}")
    colis_recu = cs.receptionner(colis.id_colis, receptionne_par=admin.id_utilisateur)
    print(f"Réceptionné : {colis_recu.date_reception}")
    bcs.update_statut(bc.id_bon_commande, "livree")
    colis_retire = cs.retirer(colis.id_colis)
    print(f"Retiré : {colis_retire.date_retrait}")

    sep("RÉCAPITULATIF")
    print(f"  Demande : {demande_approuvee.statut}")
    print(f"  Devis   : {devis_accepte.statut}")
    print(f"  BC      : {bc_envoye.statut}")
    print(f"  Colis   : retiré le {colis_retire.date_retrait}")
    print("\n✅ Flux complet OK")