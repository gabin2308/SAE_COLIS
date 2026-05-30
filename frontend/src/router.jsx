import { createBrowserRouter, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Utilisateurs from './pages/admin/Utilisateurs'
import Departements from './pages/admin/Departements'
import Fournisseurs from './pages/admin/Fournisseurs'
import Colis from './pages/admin/Colis'
import BonsCommande from './pages/admin/BonsCommande'
import Devis from './pages/admin/Devis'
import Demandes from './pages/admin/Demandes'
import Notifications from './pages/admin/Notifications'
import ProtectedRoute from './components/ProtectedRoute'
import AdminLayout from './components/AdminLayout'
import MesColis from "./pages/lecteur/MesColis"
import MesDemandesLecteur from "./pages/lecteur/MesDemandes"
import NotificationsLecteur from "./pages/lecteur/Notifications"
import LecteurLayout from "./components/LecteurLayout"

export const router = createBrowserRouter([
  { path: '/', element: <Login /> },
  { path: '/register', element: <Register /> },

  {
    path: '/dashboard',
    element: (
      <ProtectedRoute roles={["admin"]}>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Dashboard /> }
    ]
  },

  {
    path: '/admin',
    element: (
      <ProtectedRoute roles={["admin"]}>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      { path: 'utilisateurs',  element: <Utilisateurs /> },
      { path: 'departements',  element: <Departements /> },
      { path: 'fournisseurs',  element: <Fournisseurs /> },
      { path: 'colis',         element: <Colis /> },
      { path: 'bons-commande', element: <BonsCommande /> },
      { path: 'devis',         element: <Devis /> },
      { path: 'demandes',      element: <Demandes /> },
      { path: 'notifications', element: <Notifications /> },
    ]
  },

  {
  path: '/lecteur',
  element: (
    <ProtectedRoute roles={["lecteur"]}>
      <LecteurLayout />
    </ProtectedRoute>
  ),
  children: [
    { index: true,          element: <MesColis /> },
    { path: 'demandes',     element: <MesDemandesLecteur /> },
    // { path: 'notifications',element: <NotificationsLecteur /> },
  ]
},

  { path: '*', element: <Navigate to="/" replace /> }
])