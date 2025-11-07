import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Chip,
  Fade,
  Zoom,
  Slide,
  Grow,
} from '@mui/material';
import {
  CloudDownload,
  Storage,
  Analytics,
  Dashboard,
  CheckCircle,
  PlayArrow,
  Pause,
  Replay,
} from '@mui/icons-material';

interface PipelineStage {
  label: string;
  description: string;
  icon: React.ReactNode;
  status: 'idle' | 'processing' | 'completed' | 'error';
  duration: number;
}

export const DataPipeline: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [isRunning, setIsRunning] = useState(true);
  const [completed, setCompleted] = useState<boolean[]>([]);

  const pipelineStages: PipelineStage[] = [
    {
      label: 'Salesforce Data Fetch',
      description: 'Retrieving customer interaction data from Salesforce CRM',
      icon: <CloudDownload />,
      status: 'idle',
      duration: 2000,
    },
    {
      label: 'Data Processing',
      description: 'Cleaning, transforming, and preparing data for analysis',
      icon: <Storage />,
      status: 'idle',
      duration: 3000,
    },
    {
      label: 'AI Analysis',
      description: 'Analyzing transcripts using GPT models for quality assessment',
      icon: <Analytics />,
      status: 'idle',
      duration: 4000,
    },
    {
      label: 'KPI Calculation',
      description: 'Computing performance metrics and generating insights',
      icon: <Dashboard />,
      status: 'idle',
      duration: 2000,
    },
    {
      label: 'Report Generation',
      description: 'Creating comprehensive quality reports and dashboards',
      icon: <CheckCircle />,
      status: 'idle',
      duration: 3000,
    },
  ];

  useEffect(() => {
    if (!isRunning) return;

    const timer = setTimeout(() => {
      if (activeStep < pipelineStages.length) {
        setActiveStep((prev) => prev + 1);
        setCompleted((prev) => [...prev, true]);
      } else {
        // Reset after completion
        setTimeout(() => {
          setActiveStep(0);
          setCompleted([]);
        }, 3000);
      }
    }, pipelineStages[activeStep]?.duration || 2000);

    return () => clearTimeout(timer);
  }, [activeStep, isRunning, pipelineStages]);

  const getStatusColor = (stepIndex: number) => {
    if (stepIndex < activeStep) return 'success';
    if (stepIndex === activeStep) return 'primary';
    return 'default';
  };

  const getStatusIcon = (stepIndex: number): React.ReactElement | undefined => {
    if (stepIndex < activeStep) return <CheckCircle color="success" />;
    if (stepIndex === activeStep) return <PlayArrow color="primary" />;
    return undefined;
  };

  const getStatusLabel = (stepIndex: number): string => {
    if (stepIndex < activeStep) return 'Completed';
    if (stepIndex === activeStep) return 'Processing';
    return 'Pending';
  };

  return (
    <Paper sx={{ p: 4, mb: 4 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Box>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: '#1d1d1f' }}>
            Data Pipeline
          </Typography>
          <Typography variant="body2" sx={{ color: '#86868b' }}>
            Real-time data flow from Salesforce to insights
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <Chip
            icon={isRunning ? <Pause /> : <PlayArrow />}
            label={isRunning ? 'Running' : 'Paused'}
            onClick={() => setIsRunning(!isRunning)}
            variant={isRunning ? 'filled' : 'outlined'}
            color={isRunning ? 'primary' : 'default'}
          />
          <Chip
            icon={<Replay />}
            label="Reset"
            onClick={() => {
              setActiveStep(0);
              setCompleted([]);
              setIsRunning(true);
            }}
            variant="outlined"
          />
        </Box>
      </Box>

      {/* Animated Pipeline Visualization */}
      <Box sx={{ position: 'relative', mb: 4 }}>
        {/* Connection Lines */}
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: 0,
            right: 0,
            height: 2,
            backgroundColor: '#e8e8ed',
            zIndex: 1,
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: 0,
            width: `${(activeStep / pipelineStages.length) * 100}%`,
            height: 2,
            backgroundColor: '#0071e3',
            zIndex: 2,
            transition: 'width 0.5s ease-in-out',
          }}
        />

        {/* Pipeline Nodes */}
        <Box display="flex" justifyContent="space-between" position="relative" zIndex={3}>
          {pipelineStages.map((stage, index) => (
            <Grow in={true} timeout={index * 500} key={index}>
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  position: 'relative',
                }}
              >
                {/* Animated Node */}
                <Fade in={true} timeout={1000}>
                  <Box
                    sx={{
                      width: 60,
                      height: 60,
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: index <= activeStep ? '#0071e3' : '#f5f5f7',
                      color: index <= activeStep ? 'white' : '#86868b',
                      border: `2px solid ${index <= activeStep ? '#0071e3' : '#e8e8ed'}`,
                      transition: 'all 0.3s ease',
                      transform: index === activeStep ? 'scale(1.1)' : 'scale(1)',
                      boxShadow: index === activeStep ? '0 0 20px rgba(0, 113, 227, 0.3)' : 'none',
                    }}
                  >
                    {stage.icon}
                  </Box>
                </Fade>

                {/* Active Pulse Animation */}
                {index === activeStep && isRunning && (
                  <Box
                    sx={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      width: 80,
                      height: 80,
                      borderRadius: '50%',
                      backgroundColor: 'rgba(0, 113, 227, 0.1)',
                      transform: 'translate(-50%, -50%)',
                      animation: 'pulse 2s infinite',
                      '@keyframes pulse': {
                        '0%': {
                          transform: 'translate(-50%, -50%) scale(1)',
                          opacity: 1,
                        },
                        '100%': {
                          transform: 'translate(-50%, -50%) scale(1.5)',
                          opacity: 0,
                        },
                      },
                    }}
                  />
                )}

                {/* Stage Label */}
                <Typography
                  variant="body2"
                  sx={{
                    mt: 2,
                    fontWeight: 600,
                    textAlign: 'center',
                    color: index <= activeStep ? '#1d1d1f' : '#86868b',
                    maxWidth: 120,
                  }}
                >
                  {stage.label}
                </Typography>

                {/* Status Indicator */}
                <Chip
                  label={getStatusLabel(index)}
                  size="small"
                  color={getStatusColor(index)}
                  sx={{ mt: 1, fontSize: '0.7rem' }}
                  icon={getStatusIcon(index)}
                />
              </Box>
            </Grow>
          ))}
        </Box>
      </Box>

      {/* Current Stage Details */}
      {pipelineStages[activeStep] && (
        <Slide direction="up" in={true} mountOnEnter unmountOnExit>
          <Paper
            sx={{
              p: 3,
              backgroundColor: '#f8f9fa',
              borderLeft: `4px solid #0071e3`,
              borderRadius: 2,
            }}
          >
            <Box display="flex" alignItems="center" gap={2}>
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: '#0071e3',
                  color: 'white',
                }}
              >
                {pipelineStages[activeStep].icon}
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600, color: '#1d1d1f' }}>
                  {pipelineStages[activeStep].label}
                </Typography>
                <Typography variant="body2" sx={{ color: '#86868b', mt: 0.5 }}>
                  {pipelineStages[activeStep].description}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Slide>
      )}
    </Paper>
  );
};