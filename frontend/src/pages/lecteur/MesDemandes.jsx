import { useEffect, useState } from "react"
import { demandeAchatService } from "../../services/demandeAchatService"

export default function MesDemandes() {
  const [demandes, setDemandes]         = useState([])
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState(null)
  const [statutFilter, setStatutFilter] = useState("all")
  const [form, setForm] = useState({ objet: "", description: "", montant_estime: "" })
  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    setError(null)
    const data = await demandeAchatService.getMesDemandes()
    if (!Array.isArray(data)) {
      setError("Impossible de charger vos demandes")
    } else {
      setDemandes(data)
    }
    setLoading(false)
  }

  async function handleDelete(id) {
    if (!window.confirm("Supprimer cette demande ?")) return
    const res = await demandeAchatService.delete(id)
    if (res?.error) { alert(res.error); return }
    setDemandes(prev => prev.filter(d => d.id_demande !== id))
  }

  function handleChange(e) {
  setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
}

  async function handleCreate(e) {
    e.preventDefault()
    const res = await demandeAchatService.create(form)
    if (res?.error) { alert(res.error); return }
    setDemandes(prev => [res, ...prev])
    setForm({ objet: "", description: "", montant_estime: "" })
  }

  if (loading) return <p className="text-gray-500 p-6">Chargement...</p>
  if (error)   return <p className="text-red-500 p-6">{error}</p>

  const filtered = demandes.filter(d => {
    if (statutFilter === "all") return true
    return d.statut === statutFilter
  })

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Mes demandes</h1>
        <form onSubmit={handleCreate} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 mb-6">
        <h2 className="font-semibold text-gray-800 mb-4">Nouvelle demande</h2>
        <input name="objet" value={form.objet} onChange={handleChange} placeholder="Objet *" required className="border px-3 py-2 rounded-md text-sm w-full mb-3" />
        <input name="description" value={form.description} onChange={handleChange} placeholder="Description" className="border px-3 py-2 rounded-md text-sm w-full mb-3" />
        <input name="montant_estime" value={form.montant_estime} onChange={handleChange} placeholder="Montant estimé (€)" type="number" className="border px-3 py-2 rounded-md text-sm w-full mb-3" />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm hover:bg-indigo-700">
          Envoyer
        </button>
      </form>
      <div className="flex gap-3 mb-4">
        <select
          value={statutFilter}
          onChange={e => setStatutFilter(e.target.value)}
          className="border px-3 py-2 rounded-md text-sm"
        >
          <option value="all">Tous les statuts</option>
          <option value="en_attente">En attente</option>
          <option value="approuvee">Approuvée</option>
          <option value="refusee">Refusée</option>
        </select>
        <span className="ml-auto text-sm text-gray-400 self-center">
          {filtered.length} demande{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-100 p-12 text-center">
          <p className="text-4xl mb-3">📝</p>
          <p className="text-gray-500 text-sm">Aucune demande trouvée</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(d => (
            <div key={d.id_demande} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-medium text-gray-900">{d.objet}</p>
                  <p className="text-xs text-gray-400 mt-0.5">{d.date_demande}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  d.statut === "en_attente" ? "bg-yellow-100 text-yellow-700" :
                  d.statut === "approuvee"  ? "bg-green-100 text-green-700"  :
                  "bg-red-100 text-red-700"
                }`}>
                  {d.statut.replace(/_/g, " ")}
                </span>
              </div>

              <div className="mt-3 flex items-center justify-between">
                <p className="text-sm text-gray-500">
                  {d.montant_estime ? `${d.montant_estime} €` : "Montant non renseigné"}
                </p>
                {d.statut === "en_attente" && (
                  <button
                    onClick={() => handleDelete(d.id_demande)}
                    className="text-xs bg-red-100 text-red-600 hover:bg-red-200 px-2 py-1 rounded"
                  >
                    🗑 Supprimer
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}