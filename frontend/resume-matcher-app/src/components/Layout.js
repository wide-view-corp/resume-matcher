import React from 'react';
import { Box, Flex, Link as ChakraLink, VStack } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const NavItem = ({ to, children }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <ChakraLink
      as={RouterLink}
      to={to}
      p={2}
      borderRadius="md"
      bg={isActive ? 'blue.500' : 'transparent'}
      color={isActive ? 'white' : 'gray.700'}
      _hover={{ bg: isActive ? 'blue.600' : 'blue.100' }}
      fontWeight="medium"
    >
      {children}
    </ChakraLink>
  );
};

const Layout = ({ children }) => {
  return (
    <Flex minHeight="100vh">
      <Box width="200px" bg="gray.100" p={4}>
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
