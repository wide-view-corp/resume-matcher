import React from 'react';
import { Box, Text, Avatar, IconButton, Tooltip, VStack, Divider, useColorModeValue } from '@chakra-ui/react';
import { FaSignOutAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

const getAvatarColor = (name) => {
  const colors = [
    'teal.400', 'orange.400', 'purple.400', 
    'pink.400', 'blue.400', 'green.400'
  ];
  const index = name.length % colors.length;
  return colors[index];
};

const UserProfile = ({ isCollapsed, user, setIsLoggedIn, setUser }) => {
  const navigate = useNavigate();
  const separatorColor = useColorModeValue('gray.300', 'gray.600');
  const bgColor = useColorModeValue('white', 'gray.800');

  const handleLogout = () => {
    authService.logout();
    setIsLoggedIn(false);
    setUser(null);
    navigate('/login');
  };

  const initials = getInitials(user.name);
  const avatarColor = getAvatarColor(user.name);

  return (
    <VStack spacing={4} align="center" width="full">
      <VStack spacing={2}>
        <Avatar 
          size="md" 
          name={user.name} 
          bg={avatarColor}
          color="white"
          fontWeight="bold"
        >
          {initials}
        </Avatar>
        {!isCollapsed && (
          <Text fontSize="sm" fontWeight="medium" textAlign="center" isTruncated>
            {user.name}
          </Text>
        )}
      </VStack>
      
      <Box width="full" position="relative" py={2}>
        <Divider borderColor={separatorColor} />
        <Box 
          position="absolute" 
          top="50%" 
          left="50%" 
          transform="translate(-50%, -50%)" 
          bg={bgColor}
          px={2}
        >
          <Box w={1} h={1} borderRadius="full" bg={separatorColor} />
        </Box>
      </Box>
      
      <Tooltip label={isCollapsed ? "Logout" : ""} placement="right">
        <IconButton
          icon={<FaSignOutAlt />}
          onClick={handleLogout}
          aria-label="Logout"
          size="sm"
          variant="ghost"
          width="full"
        >
          {!isCollapsed && <Text ml={2}>Logout</Text>}
        </IconButton>
      </Tooltip>
    </VStack>
  );
};

export default UserProfile;