// components/ErddapTable.tsx
import React from 'react';

type ColumnRenderConfig = {
  label: string;
  className?: string;
  render?: (value: string) => React.ReactNode;
};

interface ErddapTableProps {
  columns: string[] | undefined;
  rows: string[][] | undefined;
  columnRenderMap: Record<string, ColumnRenderConfig>;
}

export default function ErddapTable({ columns, rows, columnRenderMap }: ErddapTableProps) {
  return (
    <table>
      <thead>
        <tr>
          {columns?.map((column, colIndex) => (
            <th key={colIndex}>
              {columnRenderMap[column]?.label ?? column}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {columns && rows?.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((value, colIndex) => {
              const columnName = columns[colIndex];
              const config = columnRenderMap[columnName] || {};
              return (
                <td key={colIndex} className={config.className ?? ""}>
                  {config.render ? config.render(value) : value}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}