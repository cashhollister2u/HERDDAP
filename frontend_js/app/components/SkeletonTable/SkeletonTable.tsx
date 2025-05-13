import './style.css';

export default function SkeletonTable() {
    return (
      <table className="skeleton-table">
        <thead>
          <tr>
            {Array.from({ length: 13 }).map((_, i) => (
              <th key={i}><div></div></th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: 10 }).map((_, i) => (
            <tr key={i}>
              {Array.from({ length: 13 }).map((_, j) => (
                <td key={j}>
                  <div></div>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }