import React, { useState } from 'react';
import { Box, Input, Button, VStack, Text, Heading, Icon } from '@chakra-ui/react';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: 'This is a sample response from the chatbot.', sender: 'bot' },
        ]);
      }, 1000);
      setInput('');
    }
  };

  return (
    <Box>
      <Heading mb={6} color="white">Chatbot</Heading>
      <Box p={6} borderRadius="lg" boxShadow="md" bg="white" backdropFilter="blur(10px)" backgroundColor="rgba(255,255,255,0.8)">
        <VStack spacing={4} align="stretch" height="400px">
          <Box flex={1} overflowY="auto" borderRadius="md" bg="gray.50" p={4}>
            {messages.map((message, index) => (
              <Box
                key={index}
                alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'}
                bg={message.sender === 'user' ? 'blue.100' : 'gray.200'}
                color={message.sender === 'user' ? 'blue.800' : 'gray.800'}
                p={2}
                borderRadius="md"
                maxWidth="70%"
                mb={2}
                display="flex"
                alignItems="center"
              >
                <Icon as={message.sender === 'user' ? FaUser : FaRobot} mr={2} />
                <Text>{message.text}</Text>
              </Box>
            ))}
          </Box>
          <Box display="flex">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              mr={2}
            />
            <Button onClick={handleSend} colorScheme="blue" leftIcon={<Icon as={FaPaperPlane} />}>
              Send
            </Button>
          </Box>
        </VStack>
      </Box>
    </Box>
  );
};

export default Chatbot;