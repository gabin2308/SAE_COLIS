#!/bin/bash
# ==============================================
# SCRIPT DE TEST COMPLET SAE_COLIS
# ==============================================

BASE="http://localhost:5000/api"
DB=$(find . -name "*.db" | head -1)
PASS=0
FAIL=0

check() {
  local label=$1
  local response=$2
  local expected=$3
  if echo "$response" | grep -q "$expected"; then
    echo "✅ $label"
    ((PASS++))
  else
    echo "❌ $label"
    echo "   Réponse: $response"
    ((FAIL++))
  fi
}

echo ""
echo "======================================"
echo "  TESTS SAE_COLIS — $(date)"
echo "======================================"

# ==============================================
# 0. RESET BASE
# ==============================================
echo ""
echo "── 0. RESET BASE ──"
sqlite3 $DB "DELETE FROM notification;"
sqlite3 $DB "DELETE FROM evenement_colis;"
sqlite3 $DB "DELETE FROM colis;"
sqlite3 $DB "DELETE FROM bon_commande;"
sqlite3 $DB "DELETE FROM devis;"
sqlite3 $DB "DELETE FROM fournisseur;"
sqlite3 $DB "DELETE FROM demande_achat;"
sqlite3 $DB "DELETE FROM departement WHERE id_departement > 1;"
echo "✅ Base nettoyée"

# ==============================================
# 1. AUTH
# ==============================================
echo ""
echo "── 1. AUTH ──"

# Login admin
TOKEN=$(curl -s -X POST $BASE/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"gabin@gmail.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
check "Login admin" "$TOKEN" "eyJ"

# Login directeur
TOKEN_DIR=$(curl -s -X POST $BASE/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"directeur@test.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
check "Login directeur" "$TOKEN_DIR" "eyJ"

# Login finance
TOKEN_FIN=$(curl -s -X POST $BASE/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"finance@test.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
check "Login responsable_financier" "$TOKEN_FIN" "eyJ"

# Login postal IUT
TOKEN_IUT=$(curl -s -X POST $BASE/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"postal_iut@test.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
check "Login agent_postal_iut" "$TOKEN_IUT" "eyJ"

# Login lecteur
TOKEN_LEC=$(curl -s -X POST $BASE/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"lecteur@test.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
check "Login lecteur" "$TOKEN_LEC" "eyJ"

# /me
R=$(curl -s $BASE/auth/me -H "Authorization: Bearer $TOKEN")
check "GET /auth/me" "$R" "administrateur"

# Accès refusé sans token
R=$(curl -s $BASE/colis/)
check "Accès refusé sans token" "$R" "Missing Authorization"

# ==============================================
# 2. DÉPARTEMENT
# ==============================================
echo ""
echo "── 2. DÉPARTEMENT ──"

R=$(curl -s -X POST $BASE/departement/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Sciences","budget_total":40000}')
check "Créer département" "$R" "Sciences"

R=$(curl -s $BASE/departement/ -H "Authorization: Bearer $TOKEN")
check "Lister départements" "$R" "Informatique"

R=$(curl -s $BASE/departement/1 -H "Authorization: Bearer $TOKEN")
check "GET département par id" "$R" "Informatique"

# Lecteur ne peut pas créer
R=$(curl -s -X POST $BASE/departement/ \
  -H "Authorization: Bearer $TOKEN_LEC" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test","budget_total":1000}')
check "Lecteur ne peut pas créer département" "$R" "refus"

# ==============================================
# 3. FOURNISSEUR
# ==============================================
echo ""
echo "── 3. FOURNISSEUR ──"

R=$(curl -s -X POST $BASE/fournisseur/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Dell France","contact_email":"contact@dell.fr","siret":"12345678901234"}')
check "Créer fournisseur" "$R" "Dell France"

R=$(curl -s $BASE/fournisseur/ -H "Authorization: Bearer $TOKEN")
check "Lister fournisseurs" "$R" "Dell France"

# Unicité SIRET
R=$(curl -s -X POST $BASE/fournisseur/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Dell Copie","siret":"12345678901234"}')
check "SIRET unique" "$R" "existe"

# Désactiver
R=$(curl -s -X PATCH $BASE/fournisseur/1/desactiver \
  -H "Authorization: Bearer $TOKEN")
check "Désactiver fournisseur" "$R" "actif"

# Réactiver
R=$(curl -s -X PATCH $BASE/fournisseur/1/reactiver \
  -H "Authorization: Bearer $TOKEN")
check "Réactiver fournisseur" "$R" "actif"

# Recherche
R=$(curl -s "$BASE/fournisseur/search?q=Dell" -H "Authorization: Bearer $TOKEN")
check "Recherche fournisseur" "$R" "Dell"

# ==============================================
# 4. DEVIS
# ==============================================
echo ""
echo "── 4. DEVIS ──"

R=$(curl -s -X POST $BASE/devis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fournisseur_id":1,"objet":"Achat laptops","montant_estime":3000}')
check "Créer devis" "$R" "en_attente"

R=$(curl -s $BASE/devis/1 -H "Authorization: Bearer $TOKEN")
check "GET devis par id" "$R" "Achat laptops"

R=$(curl -s -X PATCH $BASE/devis/1/accepter \
  -H "Authorization: Bearer $TOKEN")
check "Accepter devis" "$R" "accepte"

# Refuser un 2ème devis
curl -s -X POST $BASE/devis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fournisseur_id":1,"objet":"Devis alternatif","montant_estime":500}' > /dev/null

R=$(curl -s -X PATCH $BASE/devis/2/refuser \
  -H "Authorization: Bearer $TOKEN")
check "Refuser devis" "$R" "refuse"

R=$(curl -s "$BASE/devis/statut/accepte" -H "Authorization: Bearer $TOKEN")
check "Filtrer devis par statut" "$R" "accepte"

# ==============================================
# 5. BON DE COMMANDE
# ==============================================
echo ""
echo "── 5. BON DE COMMANDE ──"

R=$(curl -s -X POST $BASE/bon_commande/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"departement_id":1,"fournisseur_id":1,"devis_id":1,"montant_estime":3000}')
check "Créer bon de commande" "$R" "en_preparation"

R=$(curl -s -X PATCH $BASE/bon_commande/1/valider \
  -H "Authorization: Bearer $TOKEN")
check "Valider bon de commande" "$R" "valide_finance"

R=$(curl -s -X PATCH $BASE/bon_commande/1/expedier \
  -H "Authorization: Bearer $TOKEN")
check "Expédier bon de commande" "$R" "expedie"

# Devis déjà utilisé
R=$(curl -s -X POST $BASE/bon_commande/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"departement_id":1,"fournisseur_id":1,"devis_id":1,"montant_estime":3000}')
check "Devis déjà utilisé → erreur" "$R" "existe"

R=$(curl -s "$BASE/bon_commande/statut/expedie" \
  -H "Authorization: Bearer $TOKEN")
check "Filtrer BC par statut" "$R" "expedie"

# ==============================================
# 6. COLIS
# ==============================================
echo ""
echo "── 6. COLIS ──"

R=$(curl -s -X POST $BASE/colis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bon_commande_id":1,"destinataire_id":1}')
COLIS_ID=$(echo $R | python3 -c "import sys,json; print(json.load(sys.stdin).get('id_colis',''))" 2>/dev/null)
check "Créer colis" "$R" "recu_universite"

R=$(curl -s -X PATCH $BASE/colis/$COLIS_ID/receptionner \
  -H "Authorization: Bearer $TOKEN")
check "Réceptionner colis" "$R" "en_attente_retrait"

R=$(curl -s -X PATCH $BASE/colis/$COLIS_ID/transferer \
  -H "Authorization: Bearer $TOKEN")
check "Transférer colis IUT" "$R" "transfere_iut"

R=$(curl -s -X PATCH $BASE/colis/$COLIS_ID/retirer \
  -H "Authorization: Bearer $TOKEN")
check "Retirer colis" "$R" "remis_destinataire"

R=$(curl -s $BASE/colis/mes-colis -H "Authorization: Bearer $TOKEN")
check "Mes colis" "$R" "remis_destinataire"

R=$(curl -s -X PATCH $BASE/bon_commande/1/confirmer \
  -H "Authorization: Bearer $TOKEN")
check "Confirmer livraison BC" "$R" "livre_confirme"

# Incident sur nouveau colis
curl -s -X POST $BASE/colis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bon_commande_id":1,"destinataire_id":1}' > /dev/null

R=$(curl -s -X PATCH "$BASE/colis/2/incident" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commentaire":"Colis endommagé"}')
check "Signaler incident" "$R" "incident"

# ==============================================
# 7. DEMANDE D'ACHAT
# ==============================================
echo ""
echo "── 7. DEMANDE D'ACHAT ──"

R=$(curl -s -X POST $BASE/demande_achat/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"objet":"Achat écrans","description":"3 écrans 4K","montant_estime":1500}')
check "Créer demande achat" "$R" "en_attente"

R=$(curl -s $BASE/demande_achat/mes-demandes \
  -H "Authorization: Bearer $TOKEN")
check "Mes demandes" "$R" "en_attente"

R=$(curl -s -X PATCH $BASE/demande_achat/1/approuver \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commentaire":"OK budget"}')
check "Approuver demande" "$R" "approuvee"

# Refuser une 2ème demande
curl -s -X POST $BASE/demande_achat/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"objet":"Achat imprimante","montant_estime":400}' > /dev/null

R=$(curl -s -X PATCH $BASE/demande_achat/2/refuser \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commentaire":"Hors budget"}')
check "Refuser demande" "$R" "refusee"

# ==============================================
# 8. NOTIFICATIONS
# ==============================================
echo ""
echo "── 8. NOTIFICATIONS ──"

# Directeur doit avoir reçu une notif pour la demande
R=$(curl -s $BASE/notification/ -H "Authorization: Bearer $TOKEN_DIR")
check "Directeur reçoit notif demande" "$R" "Achat"

R=$(curl -s $BASE/notification/count -H "Authorization: Bearer $TOKEN_DIR")
check "Count notifs directeur > 0" "$R" "count"

# Gabin doit avoir reçu notif approbation
R=$(curl -s $BASE/notification/ -H "Authorization: Bearer $TOKEN")
check "Admin reçoit notif approbation" "$R" "approuv"

# Envoyer notif manuelle
R=$(curl -s -X POST $BASE/notification/envoyer \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id_utilisateur":1,"message":"Test notification manuelle"}')
check "Envoyer notification manuelle" "$R" "manuelle"

# Marquer lue
NOTIF_ID=$(curl -s $BASE/notification/ \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id_notification'] if d else '')" 2>/dev/null)

R=$(curl -s -X PATCH $BASE/notification/$NOTIF_ID/lire \
  -H "Authorization: Bearer $TOKEN")
check "Marquer notification lue" "$R" "lu"

# Marquer toutes lues
R=$(curl -s -X PATCH $BASE/notification/lire-toutes \
  -H "Authorization: Bearer $TOKEN")
check "Marquer toutes lues" "$R" "lues"

# ==============================================
# 9. CONTRÔLE D'ACCÈS PAR RÔLE
# ==============================================
echo ""
echo "── 9. CONTRÔLE D'ACCÈS ──"

# Lecteur ne peut pas créer de colis
R=$(curl -s -X POST $BASE/colis/ \
  -H "Authorization: Bearer $TOKEN_LEC" \
  -H "Content-Type: application/json" \
  -d '{"bon_commande_id":1,"destinataire_id":1}')
check "Lecteur ne peut pas créer colis" "$R" "refus"

# Lecteur ne peut pas approuver demande
R=$(curl -s -X PATCH $BASE/demande_achat/1/approuver \
  -H "Authorization: Bearer $TOKEN_LEC" \
  -H "Content-Type: application/json" \
  -d '{"commentaire":"test"}')
check "Lecteur ne peut pas approuver" "$R" "refus"

# Directeur peut voir les demandes de son département
R=$(curl -s "$BASE/demande_achat/departement/1" \
  -H "Authorization: Bearer $TOKEN_DIR")
check "Directeur voit demandes département" "$R" "Achat"

# ==============================================
# BILAN
# ==============================================
echo ""
echo "======================================"
echo "  BILAN : ✅ $PASS réussis  ❌ $FAIL échoués"
echo "======================================"
# Nouveau token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"gabin@gmail.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Créer un colis
curl -s -X POST http://localhost:5000/api/colis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bon_commande_id":1,"destinataire_id":1}' | python3 -m json.tool
  TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"gabin@gmail.com","password":"12345678"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Créer un colis
curl -s -X POST http://localhost:5000/api/colis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bon_commande_id":1,"destinataire_id":1}' | python3 -m json.tool