"use client";

/**
 * RolePermissionMatrix
 *
 * Renders the static JUDGE_ATLASX role-permission matrix as a readable table.
 * This is a documentation/transparency component — it does not mutate any state.
 * Actual enforcement lives in backend/app/auth/permission_matrix.py.
 */

const ROLES = [
  "public",
  "data_entry",
  "reviewer",
  "senior_reviewer",
  "admin",
] as const;

type Role = (typeof ROLES)[number];

interface PermissionGroup {
  group: string;
  permissions: {
    key: string;
    label: string;
    roles: Partial<Record<Role, boolean>>;
  }[];
}

const PERMISSION_GROUPS: PermissionGroup[] = [
  {
    group: "Public Read",
    permissions: [
      {
        key: "read_published_incidents",
        label: "Read published incidents",
        roles: { public: true, data_entry: true, reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "read_published_statutes",
        label: "Read published statutes",
        roles: { public: true, data_entry: true, reviewer: true, senior_reviewer: true, admin: true },
      },
    ],
  },
  {
    group: "Internal Read",
    permissions: [
      {
        key: "read_all_incidents",
        label: "Read all incidents (incl. drafts)",
        roles: { data_entry: true, reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "read_quarantined_runs",
        label: "Read quarantined runs",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "read_audit_log",
        label: "Read audit log",
        roles: { senior_reviewer: true, admin: true },
      },
    ],
  },
  {
    group: "Ingestion",
    permissions: [
      {
        key: "trigger_ingestion",
        label: "Trigger ingestion",
        roles: { data_entry: true, admin: true },
      },
      {
        key: "trigger_dry_run",
        label: "Trigger dry-run",
        roles: { data_entry: true, senior_reviewer: true, admin: true },
      },
      {
        key: "release_quarantine",
        label: "Release quarantined run",
        roles: { senior_reviewer: true, admin: true },
      },
    ],
  },
  {
    group: "Review",
    permissions: [
      {
        key: "approve_record",
        label: "Approve record",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "reject_record",
        label: "Reject record",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "approve_high_risk_record",
        label: "Approve high-risk record",
        roles: { senior_reviewer: true, admin: true },
      },
      {
        key: "dispute_record",
        label: "Dispute record",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
    ],
  },
  {
    group: "Publishing",
    permissions: [
      {
        key: "publish_record",
        label: "Publish record",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "suppress_record",
        label: "Suppress record",
        roles: { reviewer: true, senior_reviewer: true, admin: true },
      },
      {
        key: "mark_record_stale",
        label: "Mark record stale",
        roles: { senior_reviewer: true, admin: true },
      },
    ],
  },
  {
    group: "Administration",
    permissions: [
      {
        key: "manage_users",
        label: "Manage users",
        roles: { admin: true },
      },
      {
        key: "manage_feature_flags",
        label: "Manage feature flags",
        roles: { admin: true },
      },
      {
        key: "view_alpha_status",
        label: "View alpha status",
        roles: { senior_reviewer: true, admin: true },
      },
    ],
  },
];

const ROLE_LABELS: Record<Role, string> = {
  public: "Public",
  data_entry: "Data Entry",
  reviewer: "Reviewer",
  senior_reviewer: "Sr. Reviewer",
  admin: "Admin",
};

function Cell({ granted }: { granted?: boolean }) {
  if (granted) {
    return (
      <td className="text-center py-2 px-3">
        <span
          aria-label="Allowed"
          className="inline-block w-4 h-4 rounded-full bg-emerald-500"
        />
      </td>
    );
  }
  return (
    <td className="text-center py-2 px-3">
      <span
        aria-label="Not allowed"
        className="inline-block w-4 h-4 rounded-full bg-slate-200"
      />
    </td>
  );
}

export default function RolePermissionMatrix() {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200">
            <th className="text-left py-3 px-4 font-semibold text-slate-700 min-w-[200px]">
              Permission
            </th>
            {ROLES.map((role) => (
              <th
                key={role}
                className="text-center py-3 px-3 font-semibold text-slate-700 min-w-[80px]"
              >
                {ROLE_LABELS[role]}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {PERMISSION_GROUPS.map((group) => (
            <>
              <tr key={`group-${group.group}`} className="bg-slate-50/50">
                <td
                  colSpan={ROLES.length + 1}
                  className="py-2 px-4 text-xs font-semibold uppercase tracking-wider text-slate-500"
                >
                  {group.group}
                </td>
              </tr>
              {group.permissions.map((perm, i) => (
                <tr
                  key={perm.key}
                  className={
                    i % 2 === 0
                      ? "border-b border-slate-100"
                      : "border-b border-slate-100 bg-slate-50/30"
                  }
                >
                  <td className="py-2 px-4 text-slate-700">{perm.label}</td>
                  {ROLES.map((role) => (
                    <Cell key={role} granted={perm.roles[role]} />
                  ))}
                </tr>
              ))}
            </>
          ))}
        </tbody>
      </table>
      <div className="px-4 py-3 border-t border-slate-200 bg-slate-50 text-xs text-slate-500 flex items-center gap-4">
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-3 h-3 rounded-full bg-emerald-500" />
          Allowed
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-3 h-3 rounded-full bg-slate-200" />
          Not allowed
        </span>
        <span className="ml-auto">
          Authoritative source: <code className="font-mono">backend/app/auth/permission_matrix.py</code>
        </span>
      </div>
    </div>
  );
}
