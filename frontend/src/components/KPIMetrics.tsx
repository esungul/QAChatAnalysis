import React from 'react';
import { Grid, Typography } from '@mui/material';
import { ScoreCard } from './ScoreCard';
import { AnalysisResult } from '../types';

interface KPIMetricsProps {
  result: AnalysisResult;
}

export const KPIMetrics: React.FC<KPIMetricsProps> = ({ result }) => {
  const metrics = [
    {
      title: 'First Response',
      score: result.first_response_analysis?.score || 0,
      maxScore: 5,
      helpText: 'Within 2 min + CBR request'
    },
    {
      title: 'Security Verification',
      score: result.security_verification_analysis?.score || 0,
      maxScore: 10,
      helpText: 'Asked combo + provided all + aligned'
    },
    {
      title: 'Customer Needs',
      score: result.customer_needs_analysis?.score || 0,
      maxScore: 5,
      helpText: 'Identified reason + restated with confirmation'
    },
    {
      title: 'Interaction Responsibility',
      score: result.interaction_analysis?.score || 0,
      maxScore: 5,
      helpText: 'Proper language + responsibility + expectation'
    },
    {
      title: 'Time Respect',
      score: result.time_respect_analysis?.score || 0,
      maxScore: 10,
      helpText: 'Check-ins + no idle'
    },
    {
      title: 'Needs Identification',
      score: result.needs_identification_analysis?.score || 0,
      maxScore: 5,
      helpText: 'No redundant asks'
    },
    {
      title: 'Voice Services Question',
      score: result.transfer_analysis?.score || 0,
      maxScore: 10,
      helpText: 'Asked about voice services'
    }
  ];

  return (
    <div>
      <Typography variant="h6" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Key Performance Indicators
      </Typography>
      <Grid container spacing={3}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <ScoreCard {...metric} />
          </Grid>
        ))}
      </Grid>
    </div>
  );
};