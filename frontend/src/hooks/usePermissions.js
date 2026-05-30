import { useAuth } from "../context/AuthContext"
import { getPermissions } from "../utils/permissions"

export function usePermissions() {
  const { user } = useAuth()
  return getPermissions(user?.role)
}