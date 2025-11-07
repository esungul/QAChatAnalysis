import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, CssBaseline, ThemeProvider, createTheme, Button, Box } from '@mui/material';
import { Dashboard } from './pages/Dashboard';
import { AnalyzeChat } from './pages/AnalyzeChat';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1d1d1f', // Apple's dark gray
      light: '#424245',
      dark: '#000000',
    },
    secondary: {
      main: '#0071e3', // Apple's blue
      light: '#2997ff',
      dark: '#0077ed',
    },
    background: {
      default: '#fbfbfd', // Apple's light background
      paper: '#ffffff',
    },
    text: {
      primary: '#1d1d1f',
      secondary: '#86868b',
    },
    grey: {
      50: '#f5f5f7',
      100: '#e8e8ed',
      200: '#d2d2d7',
      300: '#c8c8c8',
    },
  },
  typography: {
    fontFamily: '"SF Pro Display", "SF Pro", "Helvetica Neue", Helvetica, Arial, sans-serif',
    h4: {
      fontWeight: 700,
      fontSize: '2rem',
      letterSpacing: '-0.5px',
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.5rem',
      letterSpacing: '-0.3px',
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.25rem',
      letterSpacing: '-0.2px',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.4,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.4,
      color: '#86868b',
    },
    button: {
      fontWeight: 500,
      textTransform: 'none',
      letterSpacing: '-0.1px',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: '0 8px 40px rgba(0,0,0,0.12)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(251, 251, 253, 0.8)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid #f0f0f0',
          color: '#1d1d1f',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 16px',
          fontWeight: 500,
        },
        outlined: {
          borderColor: '#d2d2d7',
          '&:hover': {
            borderColor: '#1d1d1f',
            backgroundColor: 'rgba(29, 29, 31, 0.04)',
          },
        },
        contained: {
          backgroundColor: '#0071e3',
          '&:hover': {
            backgroundColor: '#0077ed',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600, fontSize: '1.25rem' }}>
              QA Analyzer
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button color="inherit" component={Link} to="/" sx={{ color: '#1d1d1f' }}>
                Dashboard
              </Button>
              <Button color="inherit" component={Link} to="/analyze" sx={{ color: '#1d1d1f' }}>
                Analyze
              </Button>
            </Box>
          </Toolbar>
        </AppBar>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analyze" element={<AnalyzeChat />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;