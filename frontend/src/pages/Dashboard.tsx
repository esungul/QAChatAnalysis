import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  CircularProgress,
  Alert,
  Chip,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Analytics,
  TrendingUp,
  Assessment,
  CheckCircle,
  Warning,
  Error,
  Timeline,
  Storage,
  ShowChart,
} from '@mui/icons-material';
import { analysisAPI } from '../services/api';
import type { DashboardStats } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { DataPipeline } from '../components/DataPipeline';

// Simple TabPanel component
function TabPanel(props: { children?: React.ReactNode; value: number; index: number }) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        const data = await analysisAPI.getDashboardStats();
        setStats(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const StatCard = ({ title, value, subtitle, trend }: any) => (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="overline" sx={{ fontSize: '0.75rem', fontWeight: 600, color: '#86868b', letterSpacing: '0.5px' }}>
          {title}
        </Typography>
        <Typography variant="h3" component="div" sx={{ fontWeight: 700, mt: 1, mb: 1, color: '#1d1d1f' }}>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" sx={{ color: '#86868b', mb: 2 }}>
            {subtitle}
          </Typography>
        )}
        {trend && (
          <Chip 
            label={trend} 
            size="small" 
            sx={{ 
              backgroundColor: trend === 'Excellent' ? '#34c759' : trend === 'Good' ? '#ff9500' : '#ff3b30',
              color: 'white',
              fontWeight: 500,
              fontSize: '0.75rem',
            }}
          />
        )}
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 8, mb: 8, display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress sx={{ color: '#0071e3' }} />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
        <Alert severity="error" sx={{ borderRadius: 2 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  if (!stats) {
    return (
      <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
        <Alert severity="info" sx={{ borderRadius: 2 }}>
          No data available
        </Alert>
      </Container>
    );
  }

  const scoreDistributionData = [
    { name: 'Excellent', value: stats.score_distribution.excellent, color: '#34c759' },
    { name: 'Good', value: stats.score_distribution.good, color: '#ff9500' },
    { name: 'Average', value: stats.score_distribution.average, color: '#ffcc00' },
    { name: 'Poor', value: stats.score_distribution.poor, color: '#ff3b30' },
  ];

  const qualityTrend = stats.average_score >= 80 ? 'Excellent' : stats.average_score >= 60 ? 'Good' : 'Needs Improvement';

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, color: '#1d1d1f' }}>
          Quality Analysis Dashboard
        </Typography>
        <Typography variant="body1" sx={{ color: '#86868b', fontSize: '1.125rem' }}>
          Comprehensive monitoring of customer service quality metrics
        </Typography>
      </Box>

      {/* Tabs Navigation */}
      <Paper sx={{ mb: 3, borderRadius: 2 }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange}
          sx={{
            px: 2,
            '& .MuiTab-root': {
              fontWeight: 500,
              textTransform: 'none',
              fontSize: '0.9rem',
              minHeight: 60,
            }
          }}
        >
          <Tab icon={<Analytics />} label="Overview" />
          <Tab icon={<Storage />} label="Data Pipeline" />
          <Tab icon={<ShowChart />} label="Analytics" />
        </Tabs>
      </Paper>

      {/* Overview Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Key Metrics */}
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Total Analyses"
              value={stats.total_analyses}
              trend={stats.total_analyses > 10 ? 'Growing' : undefined}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Average Score"
              value={`${stats.average_score}%`}
              trend={qualityTrend}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Recent Activity"
              value={stats.recent_analyses}
              subtitle="Last 7 days"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="High Performers"
              value={stats.score_distribution.excellent}
              subtitle="≥ 80% score"
            />
          </Grid>

          {/* Charts */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  Score Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={scoreDistributionData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={2}
                      dataKey="value"
                    >
                      {scoreDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  Performance Overview
                </Typography>
                <Box display="flex" flexDirection="column" gap={2} mt={2}>
                  {scoreDistributionData.map((item, index) => (
                    <Box key={index} display="flex" alignItems="center" justifyContent="space-between" p={2} sx={{ 
                      backgroundColor: 'grey.50',
                      borderRadius: 2,
                      border: `1px solid #e8e8ed`
                    }}>
                      <Box display="flex" alignItems="center">
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            backgroundColor: item.color,
                            borderRadius: '50%',
                            mr: 2,
                          }}
                        />
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          {item.name}
                        </Typography>
                      </Box>
                      <Typography variant="body1" sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                        {item.value}
                      </Typography>
                    </Box>
                  ))}
                </Box>
                <Box mt={3} p={2} sx={{ 
                  backgroundColor: qualityTrend === 'Excellent' ? 'rgba(52, 199, 89, 0.1)' : 
                                  qualityTrend === 'Good' ? 'rgba(255, 149, 0, 0.1)' : 
                                  'rgba(255, 59, 48, 0.1)',
                  borderRadius: 2,
                  borderLeft: `4px solid ${qualityTrend === 'Excellent' ? '#34c759' : qualityTrend === 'Good' ? '#ff9500' : '#ff3b30'}`
                }}>
                  <Typography variant="body2" sx={{ fontWeight: 500, color: '#1d1d1f' }}>
                    Overall Quality: {qualityTrend}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#86868b', display: 'block', mt: 0.5 }}>
                    Based on {stats.total_analyses} analyses with {stats.average_score}% average score
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Data Pipeline Tab */}
      <TabPanel value={tabValue} index={1}>
        <DataPipeline />
        
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  Salesforce Integration
                </Typography>
                <Typography variant="body2" sx={{ color: '#86868b', mb: 3 }}>
                  Real-time data synchronization with Salesforce CRM
                </Typography>
                <Box display="flex" flexDirection="column" gap={2}>
                  {['Cases', 'Contacts', 'Accounts', 'Service History'].map((item, index) => (
                    <Box key={index} display="flex" alignItems="center" gap={2}>
                      <CheckCircle sx={{ color: '#34c759', fontSize: 20 }} />
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {item}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  AI Analysis Features
                </Typography>
                <Typography variant="body2" sx={{ color: '#86868b', mb: 3 }}>
                  Advanced natural language processing for quality assessment
                </Typography>
                <Box display="flex" flexDirection="column" gap={2}>
                  {['Sentiment Analysis', 'Intent Recognition', 'Compliance Checking', 'Quality Scoring'].map((item, index) => (
                    <Box key={index} display="flex" alignItems="center" gap={2}>
                      <CheckCircle sx={{ color: '#34c759', fontSize: 20 }} />
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {item}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Analytics Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  Performance Trends
                </Typography>
                <Typography variant="body2" sx={{ color: '#86868b', mb: 3 }}>
                  Weekly performance metrics and analysis trends
                </Typography>
                <Box sx={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'grey.50', borderRadius: 2 }}>
                  <Typography variant="body2" sx={{ color: '#86868b' }}>
                    Performance chart visualization coming soon...
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* KPI Metrics */}
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  Quality Metrics
                </Typography>
                <Grid container spacing={2}>
                  {[
                    { name: 'First Response', criteria: 'Within 2 minutes + CBR', maxScore: 5 },
                    { name: 'Security Verification', criteria: '3+ elements + customer provided', maxScore: 10 },
                    { name: 'Customer Needs', criteria: 'Identified + confirmed', maxScore: 5 },
                    { name: 'Interaction Quality', criteria: 'Language + ownership', maxScore: 5 },
                    { name: 'Time Efficiency', criteria: 'Check-ins + no delays', maxScore: 10 },
                    { name: 'Needs Identification', criteria: 'No redundant questions', maxScore: 5 },
                    { name: 'Service Discovery', criteria: 'Voice services asked', maxScore: 10 },
                  ].map((kpi, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Box sx={{ 
                        p: 2, 
                        border: '1px solid #e8e8ed',
                        borderRadius: 2,
                        height: '100%',
                      }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#1d1d1f' }}>
                          {kpi.name}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#86868b', mb: 2, fontSize: '0.8rem' }}>
                          {kpi.criteria}
                        </Typography>
                        <Chip 
                          label={`${kpi.maxScore} pts`} 
                          size="small" 
                          variant="outlined"
                          sx={{ 
                            borderColor: '#e8e8ed',
                            color: 'grey.700',
                            fontWeight: 500,
                          }}
                        />
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Container>
  );
};