import React from 'react';
import { Box, Flex, VStack } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const NavItem = ({ to, children }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Box
      as={RouterLink}
      to={to}
      p={2}
      borderRadius="md"
      bg={isActive ? 'brand.500' : 'transparent'}
      color={isActive ? 'white' : 'gray.700'}
      _hover={{ bg: isActive ? 'brand.600' : 'gray.100' }}
      fontWeight="medium"
      transition="background-color 0.2s, color 0.2s"
    >
      {children}
    </Box>
  );
};

const Layout = ({ children }) => {
  return (
    <Flex minHeight="100vh" bg="gray.50">
      <Box width="240px" bg="white" boxShadow="lg" p={4}>
        <VStack spacing={4} align="stretch">
          <NavItem to="/dashboard">Dashboard</NavItem>
          <NavItem to="/upload">Resume Upload</NavItem>
          <NavItem to="/chatbot">Chatbot</NavItem>
        </VStack>
      </Box>
      <Box flex={1} p={8}>
        {children}
      </Box>
    </Flex>
  );
};

export default Layout;
