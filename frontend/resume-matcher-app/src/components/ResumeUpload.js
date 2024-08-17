import React, { useState } from 'react';
import { Box, Button, VStack, Heading, Text, useToast, Icon } from '@chakra-ui/react';
import { FaFileUpload, FaCheck } from 'react-icons/fa';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const toast = useToast();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (file) {
      toast({
        title: 'Resume uploaded successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <Heading mb={6} color="white">Upload Your Resume</Heading>
      <Box p={6} borderRadius="lg" boxShadow="md" bg="white" backdropFilter="blur(10px)" backgroundColor="rgba(255,255,255,0.8)">
        <VStack spacing={4} align="stretch">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            style={{ display: 'none' }}
            id="resume-upload"
          />
          <label htmlFor="resume-upload">
            <Button as="span" colorScheme="blue" width="full" leftIcon={<Icon as={FaFileUpload} />}>
              Select File
            </Button>
          </label>
          {file && <Text>{file.name}</Text>}
          <Button onClick={handleUpload} colorScheme="green" isDisabled={!file} width="full" leftIcon={<Icon as={FaCheck} />}>
            Upload
          </Button>
        </VStack>
      </Box>
    </Box>
  );
};

export default ResumeUpload;