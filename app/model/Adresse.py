class Adresse:
    def __init__(self, dico):
        self.id_adresse  = dico.get('id_adresse')
        self.rue         = dico.get('rue')
        self.complement  = dico.get('complement')
        self.code_postal = dico.get('code_postal')
        self.ville       = dico.get('ville')
        self.pays        = dico.get('pays', 'France')
        self.latitude    = dico.get('latitude')
        self.longitude   = dico.get('longitude')
 
    def to_dict(self):
        return {
            'id_adresse':  self.id_adresse,
            'rue':         self.rue,
            'complement':  self.complement,
            'code_postal': self.code_postal,
            'ville':       self.ville,
            'pays':        self.pays,
            'latitude':    self.latitude,
            'longitude':   self.longitude,
        }
