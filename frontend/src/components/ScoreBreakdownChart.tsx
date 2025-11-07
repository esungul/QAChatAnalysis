import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Paper, Typography } from '@mui/material';
import { AnalysisResult } from '../types';

interface ScoreBreakdownChartProps {
  result: AnalysisResult;
}

export const ScoreBreakdownChart: React.FC<ScoreBreakdownChartProps> = ({ result }) => {
  const data = [
    { name: 'First Response', score: result.first_response_analysis?.score || 0, max: 5 },
    { name: 'Security Verification', score: result.security_verification_analysis?.score || 0, max: 10 },
    { name: 'Customer Needs', score: result.customer_needs_analysis?.score || 0, max: 5 },
    { name: 'Interaction', score: result.interaction_analysis?.score || 0, max: 5 },
    { name: 'Time Respect', score: result.time_respect_analysis?.score || 0, max: 10 },
    { name: 'Needs Identification', score: result.needs_identification_analysis?.score || 0, max: 5 },
    { name: 'Voice Services', score: result.transfer_analysis?.score || 0, max: 10 },
  ].map(item => ({
    ...item,
    percentage: item.max > 0 ? (item.score / item.max) * 100 : 0
  }));

  const getColor = (percentage: number) => {
    if (percentage >= 80) return '#4caf50';
    if (percentage >= 60) return '#ff9800';
    return '#f44336';
  };

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Score Breakdown
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="name" 
            angle={-45} 
            textAnchor="end" 
            height={80}
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            domain={[0, 100]}
            tickFormatter={(value) => `${value}%`}
          />
          <Tooltip 
            formatter={(value: number, name: string) => {
              if (name === 'percentage') return [`${value.toFixed(1)}%`, 'Percentage'];
              return [value, name];
            }}
            labelFormatter={(label) => `KPI: ${label}`}
          />
          <Bar dataKey="percentage" name="percentage">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.percentage)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Paper>
  );
};