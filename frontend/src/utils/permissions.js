export const PERMISSIONS = {
  admin:       { canViewAll: true,  canCreate: true,  canEdit: true,  canDelete: true,  canApprove: true  },
  postal_iut:  { canViewAll: true,  canCreate: false, canEdit: true,  canDelete: false, canApprove: false },
  postal_univ: { canViewAll: true,  canCreate: false, canEdit: true,  canDelete: false, canApprove: false },
  finance:     { canViewAll: true,  canCreate: false, canEdit: false, canDelete: false, canApprove: true  },
  directeur:   { canViewAll: true,  canCreate: false, canEdit: false, canDelete: false, canApprove: true  },
  departement: { canViewAll: false, canCreate: true,  canEdit: true,  canDelete: false, canApprove: false },
  lecteur:     { canViewAll: false, canCreate: false, canEdit: false, canDelete: false, canApprove: false },
}

export function getPermissions(role) {
  return PERMISSIONS[role] ?? PERMISSIONS.lecteur
}