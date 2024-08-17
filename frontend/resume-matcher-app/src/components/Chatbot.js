import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Input,
  Button,
  useColorModeValue,
  Flex,
  Spinner,
  useToast,
  Icon
} from '@chakra-ui/react';
import { FaPaperPlane } from 'react-icons/fa';
import { RiRobotFill } from 'react-icons/ri';  // Import a robot icon
import chatbotService from '../services/chatbotService';

// Custom Chatbot Icon
const ChatbotIcon = (props) => (
  <Icon as={RiRobotFill} boxSize="30px" color="blue.500" {...props} />
);

const Message = ({ message, isUser }) => {
  const bgColor = useColorModeValue(
    isUser ? 'blue.100' : 'rgba(255, 255, 255, 0.5)',
    isUser ? 'blue.700' : 'rgba(45, 55, 72, 0.6)'  // Dimmed in dark mode
  );
  const textColor = useColorModeValue(
    isUser ? 'blue.800' : 'gray.800',
    isUser ? 'blue.100' : 'gray.100'
  );
  const boxShadow = useColorModeValue(
    '0 2px 4px rgba(0, 0, 0, 0.1)',
    'none'
  );

  return (
    <Flex justify={isUser ? 'flex-end' : 'flex-start'} mb={4} opacity={0.9}>
      {!isUser && <ChatbotIcon mr={2} />}
      <Box
        maxW="70%"
        bg={bgColor}
        color={textColor}
        p={3}
        borderRadius="lg"
        fontSize="sm"
        boxShadow={boxShadow}
        backdropFilter={isUser ? 'none' : 'blur(5px)'}
        border={isUser ? 'none' : '1px solid rgba(255, 255, 255, 0.2)'}
      >
        <Text>{message.content}</Text>
      </Box>
      {isUser && <Icon as={FaPaperPlane} boxSize="20px" ml={2} color="blue.500" />}
    </Flex>
  );
};

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const endOfMessagesRef = useRef(null);
  const toast = useToast();

  const bgColor = useColorModeValue('rgba(255, 255, 255, 0.8)', 'rgba(26, 32, 44, 0.8)');
  const borderColor = useColorModeValue('rgba(255, 255, 255, 0.3)', 'rgba(255, 255, 255, 0.1)');

  useEffect(() => {
    fetchConversationHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchConversationHistory = async () => {
    try {
      const history = await chatbotService.getConversationHistory();
      setMessages(history);
    } catch (error) {
      toast({
        title: 'Error fetching conversation history',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { content: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatbotService.sendMessage(input);
      const botMessage = { content: response.message, isUser: false };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      toast({
        title: 'Error sending message',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <Box height="calc(100vh - 100px)" display="flex" flexDirection="column">
      <Flex align="center" mb={4}>
        <ChatbotIcon mr={2} />
        <Text fontSize="2xl" fontWeight="bold">AI Assistant</Text>
      </Flex>
      <Box
        flex={1}
        p={4}
        borderWidth={1}
        borderRadius="lg"
        borderColor={borderColor}
        bg={bgColor}
        overflowY="auto"
        mb={4}
        boxShadow="xl"
        backdropFilter="blur(10px)"
        css={{
          '&::-webkit-scrollbar': {
            width: '4px',
          },
          '&::-webkit-scrollbar-track': {
            width: '6px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: useColorModeValue('blue.300', 'gray.500'),
            borderRadius: '24px',
          },
        }}
      >
        <VStack spacing={4} align="stretch">
          {messages.map((message, index) => (
            <Message key={index} message={message} isUser={message.isUser} />
          ))}
          {isLoading && (
            <Flex justify="flex-start" mb={4}>
              <Spinner size="sm" mr={2} color="blue.500" />
              <Text fontSize="sm">AI is thinking...</Text>
            </Flex>
          )}
          <div ref={endOfMessagesRef} />
        </VStack>
      </Box>
      <HStack as="form" onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
          size="md"
          bg={useColorModeValue('white', 'gray.700')}
          borderColor={useColorModeValue('gray.300', 'gray.600')}
          _focus={{
            borderColor: 'blue.500',
            boxShadow: '0 0 0 1px blue.500',
          }}
        />
        <Button
          colorScheme="blue"
          onClick={handleSendMessage}
          isLoading={isLoading}
          loadingText="Sending"
          leftIcon={<FaPaperPlane />}
        >
          Send
        </Button>
      </HStack>
    </Box>
  );
};

export default Chatbot;