import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminUsersApi, UserAdminView, UserListResponse } from '../api/adminUsers';

export default function AdminUsers() {
  const navigate = useNavigate();
  const [users, setUsers] = useState<UserAdminView[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [selectedUser, setSelectedUser] = useState<UserAdminView | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await adminUsersApi.getUsers(page, 20, search || undefined);
      setUsers(response.users);
      setTotalPages(response.total_pages);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [page, search]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearch(searchInput);
    setPage(1);
  };

  const handleSuspend = async (user: UserAdminView) => {
    if (!confirm(`${user.is_suspended ? 'Unsuspend' : 'Suspend'} user ${user.email}?`)) {
      return;
    }
    try {
      setActionLoading(true);
      await adminUsersApi.suspendUser(user.id, !user.is_suspended);
      fetchUsers();
      setSelectedUser(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update user');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async (user: UserAdminView) => {
    if (!confirm(`Delete user ${user.email}? This action cannot be undone.`)) {
      return;
    }
    try {
      setActionLoading(true);
      await adminUsersApi.deleteUser(user.id);
      fetchUsers();
      setSelectedUser(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete user');
    } finally {
      setActionLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading && users.length === 0) {
    return <div className="p-8 text-center">Loading users...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">User Management</h1>
        <button
          onClick={() => navigate('/admin/movies')}
          className="text-blue-600 hover:underline"
        >
          Back to Movies
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search by email or name..."
            className="flex-1 border rounded px-4 py-2"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Search
          </button>
          {search && (
            <button
              type="button"
              onClick={() => {
                setSearch('');
                setSearchInput('');
                setPage(1);
              }}
              className="border px-4 py-2 rounded hover:bg-gray-100"
            >
              Clear
            </button>
          )}
        </div>
      </form>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {user.display_name || 'No name'}
                    </div>
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      user.role === 'admin'
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {user.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {user.is_suspended ? (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                      Suspended
                    </span>
                  ) : user.is_active ? (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Active
                    </span>
                  ) : (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      Disabled
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatDate(user.created_at)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    onClick={() => setSelectedUser(user)}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    View
                  </button>
                  <button
                    onClick={() => handleSuspend(user)}
                    disabled={actionLoading}
                    className={`${
                      user.is_suspended
                        ? 'text-green-600 hover:text-green-900'
                        : 'text-yellow-600 hover:text-yellow-900'
                    } mr-3 disabled:opacity-50`}
                  >
                    {user.is_suspended ? 'Unsuspend' : 'Suspend'}
                  </button>
                  <button
                    onClick={() => handleDelete(user)}
                    disabled={actionLoading}
                    className="text-red-600 hover:text-red-900 disabled:opacity-50"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {users.length === 0 && (
          <div className="text-center py-8 text-gray-500">No users found</div>
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center mt-6 gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-100"
          >
            Previous
          </button>
          <span className="px-4 py-2">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-100"
          >
            Next
          </button>
        </div>
      )}

      {/* User Detail Modal */}
      {selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-bold mb-4">User Details</h2>
            <div className="space-y-3">
              <div>
                <span className="font-medium">Email:</span> {selectedUser.email}
              </div>
              <div>
                <span className="font-medium">Display Name:</span>{' '}
                {selectedUser.display_name || 'Not set'}
              </div>
              <div>
                <span className="font-medium">Role:</span> {selectedUser.role}
              </div>
              <div>
                <span className="font-medium">Status:</span>{' '}
                {selectedUser.is_suspended
                  ? 'Suspended'
                  : selectedUser.is_active
                  ? 'Active'
                  : 'Disabled'}
              </div>
              <div>
                <span className="font-medium">Created:</span>{' '}
                {formatDate(selectedUser.created_at)}
              </div>
            </div>
            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={() => setSelectedUser(null)}
                className="px-4 py-2 border rounded hover:bg-gray-100"
              >
                Close
              </button>
              <button
                onClick={() => handleSuspend(selectedUser)}
                disabled={actionLoading}
                className={`px-4 py-2 rounded text-white ${
                  selectedUser.is_suspended
                    ? 'bg-green-600 hover:bg-green-700'
                    : 'bg-yellow-600 hover:bg-yellow-700'
                } disabled:opacity-50`}
              >
                {selectedUser.is_suspended ? 'Unsuspend' : 'Suspend'}
              </button>
              <button
                onClick={() => handleDelete(selectedUser)}
                disabled={actionLoading}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
