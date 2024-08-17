import React, { useState, useRef, useEffect } from 'react';
import { Box, Input, Button, VStack, Text, Heading, Flex, Icon, ScaleFade } from '@chakra-ui/react';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

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
      <Heading mb={6} color="white" textAlign="center">Chatbot</Heading>
      <Box
        p={6}
        borderRadius="2xl"
        boxShadow="xl"
        bg="rgba(255, 255, 255, 0.1)"
        backdropFilter="blur(10px)"
        border="1px solid rgba(255, 255, 255, 0.18)"
      >
        <VStack spacing={4} align="stretch" height="500px">
          <Box
            flex={1}
            overflowY="auto"
            borderRadius="xl"
            bg="rgba(255, 255, 255, 0.05)"
            p={4}
            css={{
              '&::-webkit-scrollbar': {
                width: '4px',
              },
              '&::-webkit-scrollbar-track': {
                width: '6px',
              },
              '&::-webkit-scrollbar-thumb': {
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '24px',
              },
            }}
          >
            {messages.map((message, index) => (
              <ScaleFade initialScale={0.9} in={true} key={index}>
                <Flex
                  justifyContent={message.sender === 'user' ? 'flex-end' : 'flex-start'}
                  mb={4}
                >
                  <Box
                    maxWidth="70%"
                    p={3}
                    borderRadius="lg"
                    bg={message.sender === 'user' ? 'blue.500' : 'green.500'}
                    color="white"
                    boxShadow="md"
                  >
                    <Flex alignItems="center">
                      {message.sender === 'user' ? (
                        <>
                          <Text mr={2}>{message.text}</Text>
                          <Icon as={FaUser} />
                        </>
                      ) : (
                        <>
                          <Icon as={FaRobot} mr={2} />
                          <Text>{message.text}</Text>
                        </>
                      )}
                    </Flex>
                  </Box>
                </Flex>
              </ScaleFade>
            ))}
            <div ref={messagesEndRef} />
          </Box>
          <Flex>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              mr={2}
              bg="rgba(255, 255, 255, 0.1)"
              border="1px solid rgba(255, 255, 255, 0.18)"
              _placeholder={{ color: "gray.300" }}
              color="white"
              _focus={{
                boxShadow: "0 0 0 1px rgba(255, 255, 255, 0.4)",
                borderColor: "rgba(255, 255, 255, 0.4)"
              }}
            />
            <Button
              onClick={handleSend}
              colorScheme="blue"
              leftIcon={<Icon as={FaPaperPlane} />}
              bg="rgba(66, 153, 225, 0.6)"
              _hover={{ bg: "rgba(66, 153, 225, 0.8)" }}
            >
              Send
            </Button>
          </Flex>
        </VStack>
      </Box>
    </Box>
  );
};

export default Chatbot;