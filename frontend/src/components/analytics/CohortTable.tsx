import type { Cohort } from '../../api/userBehavior';

interface Props {
  cohorts: Cohort[];
  onCohortClick?: (cohortKey: string) => void;
}

function getRetentionColor(retention: number | null): string {
  if (retention === null) return 'bg-gray-700';
  if (retention >= 70) return 'bg-green-600';
  if (retention >= 50) return 'bg-yellow-600';
  if (retention >= 30) return 'bg-orange-600';
  return 'bg-red-600';
}

export default function CohortTable({ cohorts, onCohortClick }: Props) {
  if (cohorts.length === 0) {
    return <div className="text-gray-400">No cohort data available</div>;
  }

  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="bg-gray-700">
            <th className="px-4 py-3 text-left">Cohort</th>
            <th className="px-4 py-3 text-right">Signups</th>
            <th className="px-4 py-3 text-center">D1</th>
            <th className="px-4 py-3 text-center">D7</th>
            <th className="px-4 py-3 text-center">D14</th>
            <th className="px-4 py-3 text-center">D30</th>
          </tr>
        </thead>
        <tbody>
          {cohorts.map((cohort) => (
            <tr
              key={cohort.cohort_key}
              onClick={() => onCohortClick?.(cohort.cohort_key)}
              className={`border-t border-gray-700 ${onCohortClick ? 'cursor-pointer hover:bg-gray-700' : ''}`}
            >
              <td className="px-4 py-3 font-medium">{cohort.cohort_key}</td>
              <td className="px-4 py-3 text-right">{cohort.signup_count}</td>
              <td className="px-4 py-3">
                <div className={`inline-block px-3 py-1 rounded text-center text-sm ${getRetentionColor(cohort.d1_retention)}`}>
                  {cohort.d1_retention !== null ? `${cohort.d1_retention.toFixed(0)}%` : '-'}
                </div>
              </td>
              <td className="px-4 py-3">
                <div className={`inline-block px-3 py-1 rounded text-center text-sm ${getRetentionColor(cohort.d7_retention)}`}>
                  {cohort.d7_retention !== null ? `${cohort.d7_retention.toFixed(0)}%` : '-'}
                </div>
              </td>
              <td className="px-4 py-3">
                <div className={`inline-block px-3 py-1 rounded text-center text-sm ${getRetentionColor(cohort.d14_retention)}`}>
                  {cohort.d14_retention !== null ? `${cohort.d14_retention.toFixed(0)}%` : '-'}
                </div>
              </td>
              <td className="px-4 py-3">
                <div className={`inline-block px-3 py-1 rounded text-center text-sm ${getRetentionColor(cohort.d30_retention)}`}>
                  {cohort.d30_retention !== null ? `${cohort.d30_retention.toFixed(0)}%` : '-'}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
