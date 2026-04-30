import type { ChurnRiskUser } from '../../api/userBehavior';

interface Props {
  users: ChurnRiskUser[];
  threshold: number;
  onThresholdChange: (value: number) => void;
}

function getRiskColor(score: number): string {
  if (score >= 80) return 'bg-red-600';
  if (score >= 60) return 'bg-orange-600';
  if (score >= 40) return 'bg-yellow-600';
  return 'bg-green-600';
}

function getRiskLabel(score: number): string {
  if (score >= 80) return 'Critical';
  if (score >= 60) return 'High';
  if (score >= 40) return 'Medium';
  return 'Low';
}

export default function ChurnRiskList({ users, threshold }: Props) {
  if (users.length === 0) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 text-center">
        <div className="text-gray-400">No users above {threshold}% risk threshold</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden">
      <div className="px-4 py-3 bg-gray-700 text-sm">
        {users.length} users at risk (threshold: {threshold}%)
      </div>
      <table className="w-full">
        <thead>
          <tr className="bg-gray-700 border-t border-gray-600">
            <th className="px-4 py-3 text-left">User</th>
            <th className="px-4 py-3 text-left">Email</th>
            <th className="px-4 py-3 text-center">Risk Score</th>
            <th className="px-4 py-3 text-center">Level</th>
            <th className="px-4 py-3 text-center">Last Login</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.user_id} className="border-t border-gray-700 hover:bg-gray-700">
              <td className="px-4 py-3 font-medium">{user.user_id}</td>
              <td className="px-4 py-3 text-gray-300">{user.email}</td>
              <td className="px-4 py-3 text-center">
                <span className={`inline-block px-3 py-1 rounded text-sm font-bold ${getRiskColor(user.risk_score)}`}>
                  {user.risk_score.toFixed(0)}
                </span>
              </td>
              <td className="px-4 py-3 text-center text-sm">{getRiskLabel(user.risk_score)}</td>
              <td className="px-4 py-3 text-center text-gray-400">
                {user.last_login_days !== null ? `${user.last_login_days} days ago` : 'Never'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
