-- SQLite sae_colis
PRAGMA foreign_keys = ON;

-- Table Role
CREATE TABLE IF NOT EXISTS role (
    id_role INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle TEXT NOT NULL UNIQUE
);

-- Table Departement
CREATE TABLE IF NOT EXISTS departement (
    id_departement INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    telephone TEXT,
    budget_total INTEGER DEFAULT 0,
    budget_utilise INTEGER DEFAULT 0
);

-- Table Utilisateur
CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    uid_cas TEXT UNIQUE,
    access_token_api_cas TEXT,
    fullName TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT,
    role_id INTEGER NOT NULL,
    departement_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id_role),
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement) 
);

-- Table Fournisseur
CREATE TABLE IF NOT EXISTS fournisseur (
    id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    contact_nom TEXT,
    contact_email TEXT,
    contact_telephone TEXT
);

-- Table Devis
CREATE TABLE IF NOT EXISTS devis (
    id_devis INTEGER PRIMARY KEY AUTOINCREMENT,
    date_demande TEXT NOT NULL,
    objet TEXT,
    montant_estime REAL,
    fichier_pdf BLOB,
    statut TEXT DEFAULT 'en_attente',
    fournisseur_id INTEGER NOT NULL,
    createur_id INTEGER NOT NULL,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    FOREIGN KEY (createur_id) REFERENCES utilisateur(id_utilisateur)
);

-- Table Bon de Commande
CREATE TABLE IF NOT EXISTS bon_commande (
    id_bon_commande INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_commande TEXT NOT NULL UNIQUE,
    date_commande TEXT NOT NULL,
    date_estimee_livraison TEXT,
    montant_estime REAL DEFAULT 0,
    statut TEXT DEFAULT 'en_preparation',
    departement_id INTEGER NOT NULL,
    fournisseur_id INTEGER NOT NULL,
    createur_id INTEGER NOT NULL,
    devis_id INTEGER NOT NULL,
    commentaire TEXT,
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement),
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    FOREIGN KEY (createur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (devis_id) REFERENCES devis(id_devis)
);

-- Table Statut Colis
CREATE TABLE IF NOT EXISTS statut_colis (
    id_statut INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle TEXT NOT NULL UNIQUE
);

-- Table Colis
CREATE TABLE IF NOT EXISTS colis (
    id_colis INTEGER PRIMARY KEY AUTOINCREMENT,
    bon_commande_id INTEGER NOT NULL,
    statut_id INTEGER NOT NULL,
    numero_suivi TEXT NOT NULL UNIQUE,
    code_barres TEXT,
    destinataire_id INTEGER,
    date_reception TEXT,
    date_retrait TEXT,
    commentaire TEXT,
    receptionne_par INTEGER,
    FOREIGN KEY (bon_commande_id) REFERENCES bon_commande(id_bon_commande),
    FOREIGN KEY (statut_id) REFERENCES statut_colis(id_statut),
    FOREIGN KEY (destinataire_id) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL,
    FOREIGN KEY (receptionne_par) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL
);

-- Table Notification
CREATE TABLE IF NOT EXISTS notification (
    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    message_notification TEXT NOT NULL,
    date_envoi TEXT DEFAULT (datetime('now')),
    lu INTEGER DEFAULT 0,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

-- Table Historique Colis
CREATE TABLE IF NOT EXISTS historique_colis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_colis INTEGER NOT NULL,
    action TEXT NOT NULL,
    date_action TEXT DEFAULT (datetime('now')),
    utilisateur_id INTEGER,
    FOREIGN KEY (id_colis) REFERENCES colis(id_colis),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_utilisateur_departement ON utilisateur (departement_id);
CREATE INDEX IF NOT EXISTS idx_bc_numero ON bon_commande (numero_commande);
CREATE INDEX IF NOT EXISTS idx_colis_suivi ON colis (numero_suivi);
CREATE INDEX IF NOT EXISTS idx_utilisateur_email ON utilisateur(email);
CREATE INDEX IF NOT EXISTS idx_utilisateur_cas ON utilisateur(uid_cas);
CREATE INDEX IF NOT EXISTS idx_colis_bon_commande ON colis(bon_commande_id);
CREATE INDEX IF NOT EXISTS idx_colis_statut ON colis(statut_id);
CREATE INDEX IF NOT EXISTS idx_notification_user ON notification(id_utilisateur);
-- -- Statuts obligatoires (données de référence)
 INSERT OR IGNORE INTO statut_colis (libelle) VALUES
('recu_universite'),
('transfere_iut'),
('en_attente'),
('livre'),
('probleme');

INSERT OR IGNORE INTO role (libelle) VALUES
('admin'),
('postal_iut'),
('postal_univ'),
('finance'),
('directeur'),
('departement'),
('lecteur');

-- INSERT OR IGNORE INTO departement (nom, telephone, budget_total, budget_utilise) VALUES
-- ('Informatique', '01 49 40 30 01', 50000, 12000),
-- ('Genie Civil', '01 49 40 30 02', 35000, 8000),
-- ('GEA', '01 49 40 30 03', 40000, 15000),
-- ('TC', '01 49 40 30 04', 30000, 5000),
-- ('MMI', '01 49 40 30 05', 45000, 20000);

CREATE TABLE IF NOT EXISTS demande_achat (
    id_demande INTEGER PRIMARY KEY AUTOINCREMENT,
    objet TEXT NOT NULL,
    description TEXT,
    montant_estime REAL,
    statut TEXT DEFAULT 'en_attente',
    date_demande TEXT DEFAULT (datetime('now')),
    date_traitement TEXT,
    commentaire_responsable TEXT,
    demandeur_id INTEGER NOT NULL,
    departement_id INTEGER NOT NULL,
    FOREIGN KEY (demandeur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (departement_id) REFERENCES departement(id_departement)
);