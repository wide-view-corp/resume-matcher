import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import ResumeUpload from './components/ResumeUpload';
import Chatbot from './components/Chatbot';
import Layout from './components/Layout';

// const theme = extendTheme({
//   styles: {
//     global: {
//       body: {
//         bg: 'gray.50',
//       },
//     },
//   },
//   components: {
//     Button: {
//       baseStyle: {
//         fontWeight: 'medium',
//       },
//       variants: {
//         solid: {
//           bg: 'blue.500',
//           color: 'white',
//           _hover: {
//             bg: 'blue.600',
//           },
//         },
//       },
//     },
//   },
// });
// App.js


const theme = extendTheme({
  colors: {
    brand: {
      50: '#f5f7ff',
      100: '#e0e7ff',
      200: '#c7d2ff',
      300: '#a5b4fc',
      400: '#818cf8',
      500: '#6366f1',  // primary brand color
      600: '#4f46e5',
      700: '#4338ca',
      800: '#3730a3',
      900: '#312e81',
    },
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    },
  },
  fonts: {
    heading: `'Poppins', sans-serif`,  // modern font for headings
    body: `'Inter', sans-serif`,  // sleek font for body text
  },
  styles: {
    global: {
      body: {
        bg: 'gray.50',
        color: 'gray.800',
      },
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'bold',
        borderRadius: 'full',  // sleek rounded buttons
      },
      variants: {
        solid: {
          bg: 'brand.500',
          color: 'white',
          _hover: {
            bg: 'brand.600',
          },
        },
        outline: {
          borderColor: 'brand.500',
          color: 'brand.500',
          _hover: {
            bg: 'brand.50',
          },
        },
      },
    },
  },
});


const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/login" element={
            isLoggedIn ? <Navigate to="/dashboard" /> : <Login setIsLoggedIn={setIsLoggedIn} />
          } />
          <Route path="/dashboard" element={
            isLoggedIn ? <Layout><Dashboard /></Layout> : <Navigate to="/login" />
          } />
          <Route path="/upload" element={
            isLoggedIn ? <Layout><ResumeUpload /></Layout> : <Navigate to="/login" />
          } />
          <Route path="/chatbot" element={
            isLoggedIn ? <Layout><Chatbot /></Layout> : <Navigate to="/login" />
          } />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
};

export default App;