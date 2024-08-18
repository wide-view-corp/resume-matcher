import React from 'react';
import { Box, Flex, IconButton, VStack, Text, Divider, useDisclosure, useColorModeValue } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { FaHome, FaDatabase, FaRobot, FaBars } from 'react-icons/fa';
import UserProfile from './UserProfile';

const NavItem = ({ to, icon: Icon, children, isCollapsed }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  const activeBg = useColorModeValue('whiteAlpha.300', 'blackAlpha.300');
  const hoverBg = useColorModeValue('whiteAlpha.400', 'blackAlpha.400');
  const color = useColorModeValue('gray.800', 'white');

  return (
    <Flex
      as={RouterLink}
      to={to}
      p={3}
      borderRadius="md"
      bg={isActive ? activeBg : 'transparent'}
      color={color}
      _hover={{ bg: hoverBg }}
      fontWeight="medium"
      alignItems="center"
      justifyContent={isCollapsed ? 'center' : 'flex-start'}
    >
      <Icon fontSize="20px" />
      {!isCollapsed && <Text ml={4}>{children}</Text>}
    </Flex>
  );
};

const Layout = ({ children }) => {
  const { isOpen, onToggle } = useDisclosure({ defaultIsOpen: true });
  const bgColor = useColorModeValue('rgba(255,255,255,0.8)', 'rgba(26,32,44,0.8)');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Flex minHeight="100vh">
      <Box
        width={isOpen ? '250px' : '70px'}
        bg={bgColor}
        backdropFilter="blur(10px)"
        borderRight="1px"
        borderColor={borderColor}
        transition="width 0.3s"
        p={4}
        position="fixed"
        h="100vh"
        overflowY="auto"
      >
        <VStack spacing={6} align="stretch" height="full">
          <Box mb={4}>
            <IconButton
              icon={<FaBars />}
              onClick={onToggle}
              variant="outline"
              size="sm"
              width="full"
              justifyContent={isOpen ? 'flex-start' : 'center'}
              aria-label={isOpen ? "Collapse menu" : "Expand menu"}
            />
          </Box>
          <VStack spacing={4} align="stretch" flex="1">
            <NavItem to="/dashboard" icon={FaHome} isCollapsed={!isOpen}>Dashboard</NavItem>
            <NavItem to="/dataset" icon={FaDatabase} isCollapsed={!isOpen}>Dataset Manager</NavItem>
            <NavItem to="/chatbot" icon={FaRobot} isCollapsed={!isOpen}>Chatbot</NavItem>
          </VStack>
          <Divider />
          <Box mt="auto">
            <UserProfile isCollapsed={!isOpen} />
          </Box>
        </VStack>
      </Box>
      <Box ml={isOpen ? '250px' : '70px'} flex={1} p={8} transition="margin-left 0.3s">
        <Box maxWidth={isOpen ? "1200px" : "1400px"} width="100%" mx="auto">
          {children}
        </Box>
      </Box>
    </Flex>
  );
};

export default Layout;