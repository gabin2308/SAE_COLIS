import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userService } from "../../services/UtilisateurService";
import { ArrowLeft, Save, Loader2 } from "lucide-react";
import Header from "../../components/ui/Header";

export default function AjouterUtilisateur() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    role_id: "",
    password: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await userService.create(formData);
      navigate("/utilisateurs"); // Retour à la liste après succès
    } catch (err) {
      alert("Erreur lors de la création : " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f7f9fc]">
      <Header />
      <main className="max-w-2xl mx-auto px-4 py-8">
        <button onClick={() => navigate(-1)} className="text-slate-400 mb-6 flex items-center gap-1 hover:text-[#0d2a4a]">
          <ArrowLeft size={16} /> Retour
        </button>

        <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
          <h2 className="text-xl font-bold text-[#0d2a4a] mb-6">Nouvel utilisateur</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Nom complet</label>
              <input 
                required
                className="w-full px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20"
                onChange={e => setFormData({...formData, fullName: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input 
                required type="email"
                className="w-full px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20"
                onChange={e => setFormData({...formData, email: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Mot de passe provisoire</label>
              <input 
                required type="password"
                className="w-full px-4 py-2 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-[#0d4f8a]/20"
                onChange={e => setFormData({...formData, password: e.target.value})}
              />
            </div>

            <button 
              disabled={loading}
              className="w-full flex justify-center items-center gap-2 bg-[#0d4f8a] text-white py-3 rounded-xl font-semibold hover:bg-[#0a3d6b] transition-colors"
            >
              {loading ? <Loader2 className="animate-spin" size={20} /> : <><Save size={20} /> Créer l'utilisateur</>}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}