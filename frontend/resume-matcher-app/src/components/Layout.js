import React from 'react';
import { Box, Flex, IconButton, VStack, Text, useDisclosure, Divider } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { FaHome, FaFileUpload, FaRobot, FaBars } from 'react-icons/fa';
import UserProfile from './UserProfile';

const NavItem = ({ to, icon, children, isCollapsed }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Flex
      as={RouterLink}
      to={to}
      p={3}
      borderRadius="md"
      bg={isActive ? 'whiteAlpha.300' : 'transparent'}
      color="white"
      _hover={{ bg: 'whiteAlpha.400' }}
      fontWeight="medium"
      alignItems="center"
      justifyContent={isCollapsed ? 'center' : 'flex-start'}
    >
      <Box as={icon} fontSize="20px" />
      {!isCollapsed && <Text ml={4}>{children}</Text>}
    </Flex>
  );
};

const Layout = ({ children }) => {
  const { isOpen, onToggle } = useDisclosure({ defaultIsOpen: true });

  return (
    <Flex minHeight="100vh">
      <Box
        width={isOpen ? '250px' : '70px'}
        bg="rgba(0,0,0,0.7)"
        backdropFilter="blur(10px)"
        transition="width 0.3s"
        display="flex"
        flexDirection="column"
      >
        <Flex p={4} justifyContent="space-between" alignItems="center" mb={2}>
          <UserProfile isCollapsed={!isOpen} />
          <IconButton
            icon={<FaBars />}
            onClick={onToggle}
            variant="outline"
            colorScheme="whiteAlpha"
            size="sm"
          />
        </Flex>
        <Divider borderColor="whiteAlpha.400" />
        <VStack spacing={6} align="stretch" mt={4} px={4}>
          <NavItem to="/dashboard" icon={FaHome} isCollapsed={!isOpen}>Dashboard</NavItem>
          <NavItem to="/upload" icon={FaFileUpload} isCollapsed={!isOpen}>Resume Upload</NavItem>
          <NavItem to="/chatbot" icon={FaRobot} isCollapsed={!isOpen}>Chatbot</NavItem>
        </VStack>
      </Box>
      <Box flex={1} p={8}>
        {children}
      </Box>
    </Flex>
  );
};

export default Layout;
