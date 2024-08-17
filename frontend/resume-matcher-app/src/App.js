import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ChakraProvider, extendTheme, Box, useColorMode, useColorModeValue, IconButton } from '@chakra-ui/react';
import { FaMoon, FaSun } from 'react-icons/fa';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import DatasetManager from './components/DatasetManager';
import Chatbot from './components/Chatbot';
import Layout from './components/Layout';

const theme = extendTheme({
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === 'light' ? 'gray.50' : 'gray.900',
        color: props.colorMode === 'light' ? 'gray.800' : 'white',
      },
    }),
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'medium',
      },
      variants: {
        solid: (props) => ({
          bg: props.colorMode === 'light' ? 'blue.500' : 'blue.200',
          color: props.colorMode === 'light' ? 'white' : 'gray.800',
          _hover: {
            bg: props.colorMode === 'light' ? 'blue.600' : 'blue.300',
          },
        }),
      },
    },
  },
});

const ColorModeToggle = () => {
  const { toggleColorMode } = useColorMode();
  const Icon = useColorModeValue(FaMoon, FaSun);

  return (
    <IconButton
      icon={<Icon />}
      onClick={toggleColorMode}
      position="fixed"
      top={4}
      right={4}
      zIndex="docked"
      aria-label="Toggle color mode"
    />
  );
};

const AnimatedBackground = () => {
  const gradientStart = useColorModeValue('teal.400', 'teal.900');
  const gradientEnd = useColorModeValue('blue.500', 'blue.800');
  const shapeColor = useColorModeValue('white', 'gray.700');

  return (
    <Box
      position="fixed"
      top="0"
      left="0"
      right="0"
      bottom="0"
      zIndex="-1"
      overflow="hidden"
    >
      <Box
        position="absolute"
        top="0"
        left="0"
        right="0"
        bottom="0"
        bgGradient={`linear(to-br, ${gradientStart}, ${gradientEnd})`}
      />
      <Box
        position="absolute"
        top="10%"
        left="10%"
        width="80%"
        height="80%"
        opacity="0.1"
        borderRadius="full"
        bg={shapeColor}
        filter="blur(60px)"
        animation="float 15s ease-in-out infinite alternate"
      />
      <Box
        position="absolute"
        top="20%"
        right="15%"
        width="40%"
        height="40%"
        opacity="0.1"
        borderRadius="full"
        bg={shapeColor}
        filter="blur(40px)"
        animation="float 20s ease-in-out infinite alternate-reverse"
      />
      <style>
        {`
          @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-20px) rotate(10deg); }
          }
        `}
      </style>
    </Box>
  );
};

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Box minHeight="100vh" position="relative">
          <AnimatedBackground />
          <ColorModeToggle />
          <Routes>
            <Route path="/login" element={
              isLoggedIn ? <Navigate to="/dashboard" /> : <Login setIsLoggedIn={setIsLoggedIn} />
            } />
            <Route path="/dashboard" element={
              isLoggedIn ? <Layout><Dashboard /></Layout> : <Navigate to="/login" />
            } />
            <Route path="/dataset" element={
              isLoggedIn ? <Layout><DatasetManager /></Layout> : <Navigate to="/login" />
            } />
            <Route path="/chatbot" element={
              isLoggedIn ? <Layout><Chatbot /></Layout> : <Navigate to="/login" />
            } />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </Box>
      </Router>
    </ChakraProvider>
  );
};

export default App;