import { createBrowserRouter } from 'react-router-dom'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Dashboard from './pages/lecteur/Dashboard'

export default createBrowserRouter([
  { path: '/', element: <Login /> },
  {path:'/register', element: <Register/>},
  {path:'/dashboard', element:<Dashboard/>},
])