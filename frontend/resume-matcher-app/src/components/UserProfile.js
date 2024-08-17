import React from 'react';
import { Box, Flex, Text, Avatar, Menu, MenuButton, MenuList, MenuItem } from '@chakra-ui/react';
import { FaChevronDown } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const UserProfile = ({ isCollapsed }) => {
  const navigate = useNavigate();
  const userName = "John Doe"; // Replace with actual user name from your auth system

  const handleLogout = () => {
    // Implement logout logic here
    // For now, we'll just redirect to the login page
    navigate('/login');
  };

  return (
    <Box>
      <Menu>
        <MenuButton>
          <Flex alignItems="center" color="white">
            <Avatar size="sm" name={userName} mr={isCollapsed ? 0 : 2} />
            {!isCollapsed && (
              <>
                <Text mr={2}>{userName}</Text>
                <FaChevronDown size="12px" />
              </>
            )}
          </Flex>
        </MenuButton>
        <MenuList>
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </MenuList>
      </Menu>
    </Box>
  );
};

export default UserProfile;