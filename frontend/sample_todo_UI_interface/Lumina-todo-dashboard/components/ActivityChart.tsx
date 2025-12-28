
import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell, Tooltip } from 'recharts';
import { Task } from '../types';
import { COLORS } from '../constants';

interface Props {
  tasks: Task[];
}

const ActivityChart: React.FC<Props> = ({ tasks }) => {
  const data = useMemo(() => {
    // Generate next 7 days data
    const days = [];
    const today = new Date();
    for (let i = 0; i < 7; i++) {
      const d = new Date(today);
      d.setDate(today.getDate() + i);
      const dateStr = d.toISOString().split('T')[0];
      const count = tasks.filter(t => t.dueDate === dateStr).length;
      days.push({
        name: d.toLocaleDateString('en-US', { weekday: 'short' }),
        count: count,
        fullDate: dateStr
      });
    }
    return days;
  }, [tasks]);

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <XAxis 
          dataKey="name" 
          axisLine={false} 
          tickLine={false} 
          tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 10 }}
          dy={10}
        />
        <Tooltip 
          cursor={{ fill: 'rgba(255,255,255,0.05)' }}
          content={({ active, payload }) => {
            if (active && payload && payload.length) {
              return (
                <div className="bg-[#1e293b]/90 border border-white/10 p-2 rounded-lg text-[10px] text-white backdrop-blur-md">
                  {payload[0].value} Tasks
                </div>
              );
            }
            return null;
          }}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]} barSize={20}>
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={entry.count > 0 ? COLORS.secondary : 'rgba(255,255,255,0.05)'} 
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default ActivityChart;
