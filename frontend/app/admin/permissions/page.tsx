import RolePermissionMatrix from "@/components/admin/RolePermissionMatrix";

export default function PermissionsPage() {
  return (
    <main className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Role Permission Matrix</h1>
        <p className="text-sm text-slate-500 mt-1">
          Read-only reference for what each role can do. Enforcement is in the backend.
          Contact an admin to adjust role assignments.
        </p>
      </div>
      <RolePermissionMatrix />
    </main>
  );
}
