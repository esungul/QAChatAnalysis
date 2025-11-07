import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import { ExpandMore, Upload, PlayArrow } from '@mui/icons-material';
import { analysisAPI } from '../services/api';
import { KPIMetrics } from '../components/KPIMetrics';
import { ScoreBreakdownChart } from '../components/ScoreBreakdownChart';
import { AnalysisResult } from '../types';

export const AnalyzeChat: React.FC = () => {
  const [transcript, setTranscript] = useState('');
  const [model, setModel] = useState('gpt-4o');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!transcript.trim()) {
      setError('Please enter a transcript to analyze');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await analysisAPI.analyzeTranscript({
        transcript,
        model,
      });
      setResult(response.result);
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setTranscript(e.target?.result as string);
        setError('');
      };
      reader.readAsText(file);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, color: '#1a237e' }}>
        Analyze Chat Transcript
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
              Input Transcript
            </Typography>
            
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <TextField
              multiline
              rows={10}
              fullWidth
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Paste transcript in format: ( 0 s ): Speaker: Message..."
              variant="outlined"
              sx={{ mb: 2 }}
            />

            <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
              <Box display="flex" gap={2} alignItems="center">
                <Button
                  variant="outlined"
                  component="label"
                  startIcon={<Upload />}
                >
                  Upload File
                  <input
                    type="file"
                    accept=".txt"
                    hidden
                    onChange={handleFileUpload}
                  />
                </Button>

                <FormControl sx={{ minWidth: 200 }}>
                  <InputLabel>AI Model</InputLabel>
                  <Select
                    value={model}
                    label="AI Model"
                    onChange={(e) => setModel(e.target.value)}
                  >
                    <MenuItem value="gpt-4o">GPT-4o</MenuItem>
                    <MenuItem value="gpt-4o-mini">GPT-4o Mini</MenuItem>
                  </Select>
                </FormControl>
              </Box>

              <Button
                variant="contained"
                onClick={handleAnalyze}
                disabled={loading || !transcript.trim()}
                size="large"
                startIcon={loading ? <CircularProgress size={20} /> : <PlayArrow />}
                sx={{ 
                  px: 4, 
                  py: 1,
                  background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                  boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
                }}
              >
                {loading ? 'Analyzing...' : 'Analyze Transcript'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        {result && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, mb: 4 }}>
                Analysis Results
              </Typography>

              {/* Overall Score */}
              <Box mb={4}>
                <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ opacity: 0.9 }}>
                      Overall Quality Score
                    </Typography>
                    <Box display="flex" alignItems="center" gap={3}>
                      <Typography variant="h2" sx={{ fontWeight: 'bold', textShadow: '2px 2px 4px rgba(0,0,0,0.3)' }}>
                        {result.overall_scores.percentage_score}%
                      </Typography>
                      <Box flexGrow={1}>
                        <Typography variant="h6" sx={{ mb: 1, opacity: 0.9 }}>
                          {result.overall_scores.total_score}/{result.overall_scores.max_possible_score} Points
                        </Typography>
                        <LinearProgress 
                          variant="determinate" 
                          value={result.overall_scores.percentage_score} 
                          sx={{ 
                            height: 20, 
                            borderRadius: 2,
                            backgroundColor: 'rgba(255,255,255,0.3)',
                            '& .MuiLinearProgress-bar': {
                              borderRadius: 2,
                              backgroundColor: 'white'
                            }
                          }}
                        />
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Box>

              {/* KPI Metrics */}
              <KPIMetrics result={result} />

              {/* Score Breakdown Chart */}
              <ScoreBreakdownChart result={result} />

              {/* Detailed Reasoning */}
              <Typography variant="h6" gutterBottom sx={{ mt: 4, mb: 2, fontWeight: 600 }}>
                Detailed Analysis
              </Typography>
              
              {[
                { key: 'first_response_analysis', title: 'First Response Analysis' },
                { key: 'security_verification_analysis', title: 'Security Verification Analysis' },
                { key: 'customer_needs_analysis', title: 'Customer Expectations and Needs Analysis' },
                { key: 'interaction_analysis', title: 'Customer Interaction and Accepting Responsibility' },
                { key: 'time_respect_analysis', title: 'Respectful of Customer\'s Time' },
                { key: 'needs_identification_analysis', title: 'Identify Contact\'s Needs and Avoid Redundant Asks' },
                { key: 'transfer_analysis', title: 'Voice Services Question Analysis' },
              ].map(({ key, title }) => (
                <Accordion key={key} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{title}</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2" style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                      {result[key]?.reasoning || 'No reasoning provided.'}
                    </Typography>
                    {result[key]?.score !== undefined && (
                      <Box mt={2} p={2} sx={{ backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                        <Typography variant="body2" color="textSecondary">
                          Score: {result[key].score}
                        </Typography>
                      </Box>
                    )}
                  </AccordionDetails>
                </Accordion>
              ))}
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  );
}
export default AnalyzeChat;