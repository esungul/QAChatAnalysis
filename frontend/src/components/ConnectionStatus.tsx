import React, { useState, useEffect } from 'react';
import { Alert, Snackbar, Chip } from '@mui/material';
import { analysisAPI } from '../services/api';

export const ConnectionStatus: React.FC = () => {
  const [connected, setConnected] = useState<boolean | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        await analysisAPI.getDashboardStats();
        setConnected(true);
      } catch (error) {
        setConnected(false);
        setOpen(true);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (connected === null) return null;

  return (
    <>
      <Chip 
        label={connected ? "Connected to Backend" : "Backend Disconnected"} 
        color={connected ? "success" : "error"}
        variant="outlined"
        size="small"
      />
      <Snackbar 
        open={open && !connected} 
        autoHideDuration={6000} 
        onClose={() => setOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert severity="error" onClose={() => setOpen(false)}>
          Cannot connect to backend server. Make sure the backend is running on http://localhost:8000
        </Alert>
      </Snackbar>
    </>
  );
};