PRAGMA foreign_keys = ON;

-- ═════════════════════════════════════════════════════════════════════
-- TABLES DE RÉFÉRENCE
-- ═════════════════════════════════════════════════════════════════════

-- Rôles utilisateur
-- Nomenclature : préfixe métier + fonction (ex: agent_postal_iut)
-- Évite les noms d'entités (ex: "departement") comme rôle
CREATE TABLE IF NOT EXISTS role (
    id_role   INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle   TEXT    NOT NULL UNIQUE
);

-- Adresse partagée entre fournisseur, departement, etc.
-- latitude/longitude optionnels pour géolocalisation future
CREATE TABLE IF NOT EXISTS adresse (
    id_adresse  INTEGER PRIMARY KEY AUTOINCREMENT,
    rue         TEXT,
    complement  TEXT,                           -- bât, étage, BP…
    code_postal TEXT,
    ville       TEXT    NOT NULL,
    pays        TEXT    NOT NULL DEFAULT 'France',
    latitude    REAL,                           -- optionnel, géolocalisation
    longitude   REAL,
    CHECK (latitude  IS NULL OR (latitude  BETWEEN -90  AND 90)),
    CHECK (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
);

-- Département de l'IUT
-- adresse_id NULL jusqu'à insertion des adresses correspondantes
CREATE TABLE IF NOT EXISTS departement (
    id_departement INTEGER PRIMARY KEY AUTOINCREMENT,
    nom            TEXT    NOT NULL UNIQUE,
    telephone      TEXT,
    email          TEXT    NOT NULL,
    budget_total   INTEGER NOT NULL DEFAULT 0 CHECK (budget_total   >= 0),
    budget_utilise INTEGER NOT NULL DEFAULT 0 CHECK (budget_utilise >= 0),
    adresse_id     INTEGER REFERENCES adresse(id_adresse) ON DELETE SET NULL,
    CHECK (budget_utilise <= budget_total)
);

-- Statuts du cycle de vie d'un colis
-- Renommés pour plus de clarté métier :
--   en_attente       → en_attente_retrait  (précise l'étape)
--   livre            → remis_destinataire  (évite ambiguïté avec le nom "livre")
--   probleme         → incident            (terme technique standard)
CREATE TABLE IF NOT EXISTS statut_colis (
    id_statut INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle   TEXT    NOT NULL UNIQUE
);

-- Statuts du cycle de vie d'un bon de commande
-- Renommés pour plus de clarté métier :
--   valide  → valide_finance   (précise qui valide)
--   envoye  → expedie          (terme logistique standard)
--   livre   → livre_confirme   (distingue de la livraison colis)
CREATE TABLE IF NOT EXISTS statut_bon_commande (
    id_statut INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle   TEXT    NOT NULL UNIQUE
);


-- ═════════════════════════════════════════════════════════════════════
-- UTILISATEUR & FOURNISSEUR
-- ═════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur       INTEGER PRIMARY KEY AUTOINCREMENT,
    uid_cas              TEXT    UNIQUE,
    access_token_api_cas TEXT,
    fullName             TEXT    NOT NULL,
    email                TEXT    NOT NULL UNIQUE,
    password             TEXT,
    role_id              INTEGER NOT NULL,
    departement_id       INTEGER NOT NULL,
    password_must_change INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (role_id)        REFERENCES role(id_role),
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement)
);

-- Fournisseur avec champs enrichis :
--   siret              : unicité légale (plus fiable que le nom)
--   actif              : soft delete (désactivation sans suppression)
--   conditions_paiement: suivi financier
--   adresse_id         : adresse de livraison/facturation
CREATE TABLE IF NOT EXISTS fournisseur (
    id_fournisseur    INTEGER PRIMARY KEY AUTOINCREMENT,
    nom               TEXT    NOT NULL,
    siret             TEXT    UNIQUE,           -- identifiant légal France
    site_web          TEXT,
    -- Contact principal
    contact_nom       TEXT,
    contact_email     TEXT    CHECK (contact_email IS NULL OR contact_email LIKE '%@%'),
    contact_telephone TEXT,
    -- Statut & traçabilité
    actif             INTEGER NOT NULL DEFAULT 1 CHECK (actif IN (0, 1)),
    date_creation     TEXT    NOT NULL DEFAULT (datetime('now')),
    date_modification TEXT,                     -- à mettre à jour via trigger applicatif
    -- Conditions commerciales
    delai_livraison_jours INTEGER CHECK (delai_livraison_jours IS NULL OR delai_livraison_jours > 0),
    conditions_paiement   TEXT   CHECK (conditions_paiement IS NULL OR conditions_paiement IN
                              ('30_jours', '60_jours', 'comptant', 'autre')),
    -- Adresse
    adresse_id        INTEGER REFERENCES adresse(id_adresse) ON DELETE SET NULL
);


-- ═════════════════════════════════════════════════════════════════════
-- FLUX ACHAT : demande → devis → bon de commande
-- ═════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS demande_achat (
    id_demande              INTEGER PRIMARY KEY AUTOINCREMENT,
    objet                   TEXT    NOT NULL,
    description             TEXT,
    montant_estime          REAL    CHECK (montant_estime >= 0),
    statut                  TEXT    NOT NULL DEFAULT 'en_attente'
                                CHECK (statut IN ('en_attente','approuvee','refusee','annulee')),
    date_demande            TEXT    NOT NULL DEFAULT (datetime('now')),
    date_traitement         TEXT,
    commentaire_responsable TEXT,
    demandeur_id            INTEGER NOT NULL,
    departement_id          INTEGER NOT NULL,
    FOREIGN KEY (demandeur_id)   REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement)
);

-- fichier_pdf stocké en BLOB ou chemin fichier selon l'implémentation
CREATE TABLE IF NOT EXISTS devis (
    id_devis       INTEGER PRIMARY KEY AUTOINCREMENT,
    date_demande   TEXT    NOT NULL DEFAULT (datetime('now')),
    objet          TEXT,
    montant_estime REAL    CHECK (montant_estime >= 0),
    fichier_pdf    BLOB,
    statut         TEXT    NOT NULL DEFAULT 'en_attente'
                               CHECK (statut IN ('en_attente','accepte','refuse')),
    fournisseur_id INTEGER NOT NULL,
    createur_id    INTEGER NOT NULL,
    -- Lien optionnel vers la demande d'achat à l'origine du devis
    demande_id     INTEGER,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    FOREIGN KEY (createur_id)    REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (demande_id)     REFERENCES demande_achat(id_demande)
);

-- Contrainte UNIQUE sur devis_id : 1 devis → 1 bon de commande maximum
CREATE TABLE IF NOT EXISTS bon_commande (
    id_bon_commande        INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_commande        TEXT    NOT NULL UNIQUE,
    date_commande          TEXT    NOT NULL DEFAULT (datetime('now')),
    date_estimee_livraison TEXT,
    montant_estime         REAL    NOT NULL DEFAULT 0 CHECK (montant_estime >= 0),
    statut_id              INTEGER NOT NULL DEFAULT 1,
    departement_id         INTEGER NOT NULL,
    fournisseur_id         INTEGER NOT NULL,
    createur_id            INTEGER NOT NULL,
    devis_id               INTEGER NOT NULL UNIQUE,  -- 1 devis → 1 bon de commande
    commentaire            TEXT,
    FOREIGN KEY (statut_id)      REFERENCES statut_bon_commande(id_statut),
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement),
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    FOREIGN KEY (createur_id)    REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (devis_id)       REFERENCES devis(id_devis)
);


-- ═════════════════════════════════════════════════════════════════════
-- COLIS & TRAÇABILITÉ UNIFIÉE
-- ═════════════════════════════════════════════════════════════════════

-- Table principale des colis
--
-- Champs QR code (option A — QR généré par l'application) :
--   qr_payload    : données encodées dans le QR, format "COL:{id_colis}:{numero_suivi}"
--                   Généré côté serveur immédiatement après l'INSERT (pour avoir l'id réel)
--   qr_image_path : chemin vers le fichier PNG du QR sur le serveur
--                   Ex: "static/qrcodes/colis_123.png"
--
-- Workflow réception par scan :
--   1. Agent scane le QR avec la caméra (page web ou app mobile)
--   2. L'app décode le payload → extrait id_colis
--   3. Affiche la fiche du colis (destinataire, bon de commande…)
--   4. Agent confirme → UPDATE statut + date_reception + receptionne_par
--                     + INSERT dans evenement_colis
--                     + INSERT notification pour le destinataire
--
-- Contrainte : date_retrait ne peut pas précéder date_reception
CREATE TABLE IF NOT EXISTS colis (
    id_colis        INTEGER PRIMARY KEY AUTOINCREMENT,
    bon_commande_id INTEGER NOT NULL,
    statut_id       INTEGER NOT NULL,
    numero_suivi    TEXT    NOT NULL UNIQUE,    -- numéro transporteur ou interne
    code_barres     TEXT,                       -- code-barres 1D si différent du QR
    -- Champs QR code (option A : QR généré par l'application)
    qr_payload      TEXT,                       -- payload brut encodé : "COL:{id}:{suivi}"
    qr_image_path   TEXT,                       -- chemin vers le PNG généré côté serveur
    -- Destinataire & réception
    destinataire_id INTEGER,
    date_reception  TEXT,                       -- rempli lors du scan de réception
    date_retrait    TEXT,                       -- rempli lors du retrait par le destinataire
    commentaire     TEXT,
    receptionne_par INTEGER,                    -- agent qui a scanné/réceptionné
    CHECK (date_retrait IS NULL OR date_reception IS NULL OR date_retrait >= date_reception),
    FOREIGN KEY (bon_commande_id) REFERENCES bon_commande(id_bon_commande),
    FOREIGN KEY (statut_id)       REFERENCES statut_colis(id_statut),
    FOREIGN KEY (destinataire_id) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL,
    FOREIGN KEY (receptionne_par) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL
);

-- Table unifiée des événements sur un colis
-- Remplace : suivi_colis + historique_colis + livraison
-- Chaque ligne = un événement daté (scan, transfert, livraison…)
--
-- Actions types : 'scan_reception', 'transfert_iut', 'remise_destinataire', 'incident'
-- Les champs de livraison (transporteur, numero_livraison…) sont remplis
-- uniquement si l'événement concerne un transport externe
CREATE TABLE IF NOT EXISTS evenement_colis (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    colis_id       INTEGER NOT NULL,
    statut_id      INTEGER,                     -- nouveau statut après l'événement
    action         TEXT,                        -- ex: 'scan_reception', 'transfert_iut'
    date_evenement TEXT    NOT NULL DEFAULT (datetime('now')),
    commentaire    TEXT,
    utilisateur_id INTEGER,                     -- agent ayant effectué l'action
    localisation   TEXT,                        -- lieu : 'Bureau postal IUT', 'Université'…
    -- Champs transport (remplis si événement lié à un transporteur externe)
    transporteur         TEXT,                  -- ex: 'Colissimo', 'DHL'
    numero_livraison     TEXT,
    date_expedition      TEXT,
    date_estimee_arrivee TEXT,
    FOREIGN KEY (colis_id)       REFERENCES colis(id_colis),
    FOREIGN KEY (statut_id)      REFERENCES statut_colis(id_statut),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);


-- ═════════════════════════════════════════════════════════════════════
-- NOTIFICATIONS
-- ═════════════════════════════════════════════════════════════════════

-- Notifications en temps réel pour les utilisateurs
-- reference_id : id de l'entité concernée (colis, bon de commande, devis…)
-- type         : permet de filtrer côté application et d'afficher la bonne icône
CREATE TABLE IF NOT EXISTS notification (
    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur  INTEGER NOT NULL,
    message         TEXT    NOT NULL,
    date_envoi      TEXT    NOT NULL DEFAULT (datetime('now')),
    lu              INTEGER NOT NULL DEFAULT 0 CHECK (lu IN (0, 1)),
    type            TEXT    CHECK (type IN (
                        'colis_recu',       -- colis arrivé au bureau postal
                        'colis_livre',      -- colis remis au destinataire
                        'bc_valide',        -- bon de commande validé
                        'bc_refuse',        -- bon de commande refusé
                        'devis_accepte',    -- devis accepté
                        'devis_refuse',     -- devis refusé
                        'autre'
                    )),
    reference_id    INTEGER,                -- id du colis, bc ou devis concerné
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);


-- ═════════════════════════════════════════════════════════════════════
-- INDEX
-- ═════════════════════════════════════════════════════════════════════

-- Utilisateur
CREATE INDEX IF NOT EXISTS idx_utilisateur_departement ON utilisateur(departement_id);
CREATE INDEX IF NOT EXISTS idx_utilisateur_email       ON utilisateur(email);
CREATE INDEX IF NOT EXISTS idx_utilisateur_cas         ON utilisateur(uid_cas);

-- Bon de commande
CREATE INDEX IF NOT EXISTS idx_bc_numero              ON bon_commande(numero_commande);
CREATE INDEX IF NOT EXISTS idx_bc_departement         ON bon_commande(departement_id);
CREATE INDEX IF NOT EXISTS idx_bc_statut              ON bon_commande(statut_id);

-- Colis
CREATE INDEX IF NOT EXISTS idx_colis_suivi            ON colis(numero_suivi);
CREATE INDEX IF NOT EXISTS idx_colis_bon_commande     ON colis(bon_commande_id);
CREATE INDEX IF NOT EXISTS idx_colis_statut           ON colis(statut_id);
CREATE INDEX IF NOT EXISTS idx_colis_destinataire     ON colis(destinataire_id);
-- Index sur qr_payload pour retrouver un colis rapidement après scan
CREATE INDEX IF NOT EXISTS idx_colis_qr_payload       ON colis(qr_payload);

-- Événements
CREATE INDEX IF NOT EXISTS idx_evenement_colis        ON evenement_colis(colis_id);
CREATE INDEX IF NOT EXISTS idx_evenement_date         ON evenement_colis(date_evenement);

-- Devis
CREATE INDEX IF NOT EXISTS idx_devis_demande          ON devis(demande_id);
CREATE INDEX IF NOT EXISTS idx_devis_fournisseur      ON devis(fournisseur_id);

-- Demande d'achat
CREATE INDEX IF NOT EXISTS idx_demande_demandeur      ON demande_achat(demandeur_id);
CREATE INDEX IF NOT EXISTS idx_demande_departement    ON demande_achat(departement_id);

-- Notifications
CREATE INDEX IF NOT EXISTS idx_notification_user      ON notification(id_utilisateur);
CREATE INDEX IF NOT EXISTS idx_notification_lu        ON notification(id_utilisateur, lu);

-- Adresse & fournisseur
CREATE INDEX IF NOT EXISTS idx_adresse_ville          ON adresse(ville);
CREATE INDEX IF NOT EXISTS idx_adresse_code_postal    ON adresse(code_postal);
CREATE INDEX IF NOT EXISTS idx_fournisseur_actif      ON fournisseur(actif);


-- ═════════════════════════════════════════════════════════════════════
-- DONNÉES DE RÉFÉRENCE
-- ═════════════════════════════════════════════════════════════════════

-- Rôles — nomenclature : préfixe métier + fonction
-- administrateur       : accès total
-- agent_postal_iut     : réception et gestion colis côté IUT
-- agent_postal_universite : réception côté université centrale
-- responsable_financier: validation budgétaire, bons de commande
-- directeur            : validation haute hiérarchie
-- responsable_departement : gestion des demandes de son département
-- lecteur              : consultation seule, sans action
INSERT OR IGNORE INTO role (libelle) VALUES
    ('administrateur'),
    ('agent_postal_iut'),
    ('agent_postal_universite'),
    ('responsable_financier'),
    ('directeur'),
    ('responsable_departement'),
    ('lecteur');

-- Statuts colis — cycle de vie complet d'un colis
-- recu_universite  : arrivé au bureau postal de l'université
-- transfere_iut    : transféré vers le bureau postal de l'IUT
-- en_attente_retrait: disponible, en attente que le destinataire vienne chercher
-- remis_destinataire: remis physiquement au destinataire (fin du cycle)
-- incident         : problème constaté (colis endommagé, introuvable…)
INSERT OR IGNORE INTO statut_colis (libelle) VALUES
    ('recu_universite'),
    ('transfere_iut'),
    ('en_attente_retrait'),
    ('remis_destinataire'),
    ('incident');

-- Statuts bon de commande — cycle de validation et livraison
-- en_preparation  : BC en cours de rédaction
-- valide_finance  : validé par le responsable financier
-- expedie         : envoyé au fournisseur / en transit
-- livre_confirme  : réception physique confirmée par le bureau postal
-- annule          : BC annulé (avant ou après validation)
INSERT OR IGNORE INTO statut_bon_commande (libelle) VALUES
    ('en_preparation'),
    ('valide_finance'),
    ('expedie'),
    ('livre_confirme'),
    ('annule');

-- Départements — email ajouté (champ obligatoire)
-- adresse_id laissé NULL : à renseigner après insertion des adresses
INSERT OR IGNORE INTO departement (nom, telephone, email, budget_total, budget_utilise) VALUES
    ('Informatique', '01 49 40 30 01', 'info@iut.fr',  50000, 12000),
    ('Genie Civil',  '01 49 40 30 02', 'gc@iut.fr',    35000,  8000),
    ('GEA',          '01 49 40 30 03', 'gea@iut.fr',   40000, 15000),
    ('TC',           '01 49 40 30 04', 'tc@iut.fr',    30000,  5000),
    ('MMI',          '01 49 40 30 05', 'mmi@iut.fr',   45000, 20000);