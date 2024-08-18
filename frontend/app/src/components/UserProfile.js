import React from 'react';
import { Box, Flex, Text, Avatar, Menu, MenuButton, MenuList, MenuItem, IconButton } from '@chakra-ui/react';
import { FaChevronDown, FaSignOutAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const UserProfile = ({ isCollapsed }) => {
  const navigate = useNavigate();
  const userName = "John Doe"; // Replace with actual user name from your auth system

  const handleLogout = () => {
    // Implement logout logic here
    navigate('/login');
  };

  if (isCollapsed) {
    return (
      <Menu>
        <MenuButton
          as={IconButton}
          icon={<Avatar size="sm" name={userName} />}
          variant="ghost"
        />
        <MenuList>
          <MenuItem onClick={handleLogout} icon={<FaSignOutAlt />}>
            Logout
          </MenuItem>
        </MenuList>
      </Menu>
    );
  }

  return (
    <Box>
      <Menu>
        <MenuButton
          py={2}
          transition="all 0.3s"
          _focus={{ boxShadow: 'none' }}
        >
          <Flex align="center">
            <Avatar size="sm" name={userName} mr="2" />
            <Text fontSize="sm" fontWeight="medium">
              {userName}
            </Text>
            <Box ml="2" display="inline-block">
              <FaChevronDown />
            </Box>
          </Flex>
        </MenuButton>
        <MenuList>
          <MenuItem onClick={handleLogout} icon={<FaSignOutAlt />}>
            Logout
          </MenuItem>
        </MenuList>
      </Menu>
    </Box>
  );
};

export default UserProfile;