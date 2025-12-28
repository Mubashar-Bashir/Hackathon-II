
import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Task } from '../types';
import { COLORS } from '../constants';

interface Props {
  tasks: Task[];
}

const PriorityDistribution: React.FC<Props> = ({ tasks }) => {
  const data = useMemo(() => {
    const counts = { low: 0, medium: 0, high: 0 };
    tasks.forEach(t => counts[t.priority]++);
    return [
      { name: 'Low', value: counts.low, color: COLORS.priority.low },
      { name: 'Medium', value: counts.medium, color: COLORS.priority.medium },
      { name: 'High', value: counts.high, color: COLORS.priority.high },
    ].filter(d => d.value > 0);
  }, [tasks]);

  if (data.length === 0) return (
    <div className="text-center py-10 text-white/20 text-sm">No data to display</div>
  );

  return (
    <div className="h-full flex flex-col items-center">
      <div className="w-full h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={70}
              paddingAngle={8}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.color} 
                  className="filter drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]"
                />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '12px',
                fontSize: '12px',
                color: '#fff'
              }}
              itemStyle={{ color: '#fff' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="w-full mt-4 space-y-2">
        {data.map((item, i) => (
          <div key={i} className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-2 h-2 rounded-full mr-3" style={{ backgroundColor: item.color }} />
              <span className="text-xs text-white/60">{item.name}</span>
            </div>
            <span className="text-xs font-bold text-white">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PriorityDistribution;
