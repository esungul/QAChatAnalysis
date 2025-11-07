import React from 'react';
import { Card, CardContent, Typography, LinearProgress, Box, Tooltip } from '@mui/material';

interface ScoreCardProps {
  title: string;
  score: number;
  maxScore: number;
  helpText?: string;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({ title, score, maxScore, helpText }) => {
  const percentage = maxScore > 0 ? (score / maxScore) * 100 : 0;
  
  return (
    <Card sx={{ height: '100%', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)' } }}>
      <CardContent>
        <Tooltip title={helpText} placement="top">
          <Typography variant="h6" component="h3" gutterBottom sx={{ fontWeight: 600 }}>
            {title}
          </Typography>
        </Tooltip>
        <Box display="flex" alignItems="center" mb={2}>
          <Typography variant="h4" component="div" color="primary" fontWeight="bold">
            {score}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1, fontSize: '1.1rem' }}>
            / {maxScore}
          </Typography>
        </Box>
        <LinearProgress 
          variant="determinate" 
          value={percentage} 
          sx={{ 
            height: 10, 
            borderRadius: 5,
            backgroundColor: '#f0f0f0',
            '& .MuiLinearProgress-bar': {
              borderRadius: 5,
              backgroundColor: percentage >= 80 ? '#4caf50' : percentage >= 60 ? '#ff9800' : '#f44336'
            }
          }}
        />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1, fontWeight: 500 }}>
          {percentage.toFixed(1)}%
        </Typography>
      </CardContent>
    </Card>
  );
};