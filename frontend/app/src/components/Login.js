import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  useToast,
  useColorModeValue,
  Image,
  Text,
  InputGroup,
  InputLeftElement,
  Flex,
  keyframes
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import authService from '../services/authService';
import logoSvg from '../assets/logo.svg'; 

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const Login = ({ setIsLoggedIn, setUser }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const bgColor = useColorModeValue("white", "gray.800");
  const textColor = useColorModeValue("gray.800", "white");
  const inputBgColor = useColorModeValue("gray.100", "gray.700");

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const userData = await authService.login(email, password);
      setIsLoggedIn(true);
      setUser(userData);
      toast({
        title: `Welcome back, ${userData.name}!`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      navigate('/dashboard');
    } catch (error) {
      toast({
        title: 'Login failed',
        description: error.message || 'An error occurred during login',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Flex minHeight="100vh" width="full" align="center" justifyContent="center">
      <Box
        borderWidth={1}
        px={4}
        width="full"
        maxWidth="500px"
        borderRadius="lg"
        textAlign="center"
        boxShadow="lg"
        bg={bgColor}
        animation={`${fadeIn} 0.5s ease-out`}
      >
        <Box p={4}>
          <VStack spacing={8} align="stretch">
            <Image src={logoSvg} alt="App Logo" boxSize="100px" mx="auto" />
            <Heading size="xl" color={textColor}>Welcome Back</Heading>
            <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.400")}>
              Log in to access your account
            </Text>
            <form onSubmit={handleLogin}>
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none" children={<FaEnvelope color="gray.300" />} />
                    <Input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email"
                      bg={inputBgColor}
                    />
                  </InputGroup>
                </FormControl>
                <FormControl>
                  <FormLabel>Password</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none" children={<FaLock color="gray.300" />} />
                    <Input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      bg={inputBgColor}
                    />
                  </InputGroup>
                </FormControl>
                <Button
                  type="submit"
                  colorScheme="blue"
                  width="full"
                  mt={4}
                  isLoading={isLoading}
                  loadingText="Logging in..."
                >
                  Log In
                </Button>
              </VStack>
            </form>
          </VStack>
        </Box>
      </Box>
    </Flex>
  );
};

export default Login;