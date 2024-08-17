import React, { useState } from 'react';
import { Box, Input, Button, VStack, Text, Heading } from '@chakra-ui/react';

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
      <Heading mb={6}>Chatbot</Heading>
      <Box p={6} borderRadius="lg" boxShadow="md" bg="white">
        <VStack spacing={4} align="stretch" height="400px">
          <Box flex={1} overflowY="auto" borderRadius="md" bg="gray.50" p={4}>
            {messages.map((message, index) => (
              <Text
                key={index}
                alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'}
                bg={message.sender === 'user' ? 'blue.100' : 'gray.200'}
                color={message.sender === 'user' ? 'blue.800' : 'gray.800'}
                p={2}
                borderRadius="md"
                maxWidth="70%"
                mb={2}
              >
                {message.text}
              </Text>
            ))}
          </Box>
          <Box display="flex">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              mr={2}
            />
            <Button onClick={handleSend} colorScheme="blue">
              Send
            </Button>
          </Box>
        </VStack>
      </Box>
    </Box>
  );
};

export default Chatbot;