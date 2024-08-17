import React, { useState } from 'react';
import { Box, Button, Input, VStack, Heading, useToast } from '@chakra-ui/react';
import { FaUser, FaLock } from 'react-icons/fa';

const Login = ({ setIsLoggedIn }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleLogin = (e) => {
    e.preventDefault();
    if (email && password) {
      setIsLoggedIn(true);
      toast({
        title: 'Login successful',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box height="100vh" display="flex" alignItems="center" justifyContent="center">
      <Box width="400px" p={8} borderRadius="lg" boxShadow="xl" bg="white" backdropFilter="blur(10px)" backgroundColor="rgba(255,255,255,0.8)">
        <VStack spacing={4}>
          <Heading size="lg">Login</Heading>
          <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            leftElement={<Box as={FaUser} color="gray.500" ml={2} />}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            leftElement={<Box as={FaLock} color="gray.500" ml={2} />}
          />
          <Button onClick={handleLogin} colorScheme="blue" width="full">
            Log In
          </Button>
        </VStack>
      </Box>
    </Box>
  );
};

export default Login;
