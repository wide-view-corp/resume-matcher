import React, { useState } from 'react';
import {
  Box,
  Button,
  VStack,
  Heading,
  Text,
  useToast,
  Icon,
  Input,
  List,
  ListItem,
  Flex,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  useColorModeValue
} from '@chakra-ui/react';
import { FaFileUpload, FaTrash, FaEye } from 'react-icons/fa';

const DatasetManager = () => {
  const [documents, setDocuments] = useState([]);
  const [newFile, setNewFile] = useState(null);
  const [previewContent, setPreviewContent] = useState('');
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();

  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.600");

  const handleFileChange = (e) => {
    setNewFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (newFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const newDoc = {
          id: Date.now(),
          name: newFile.name,
          content: e.target.result
        };
        setDocuments([...documents, newDoc]);
        setNewFile(null);
        toast({
          title: 'Document uploaded successfully',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      };
      reader.readAsText(newFile);
    }
  };

  const handleDelete = (id) => {
    setDocuments(documents.filter(doc => doc.id !== id));
    toast({
      title: 'Document deleted',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  };

  const handlePreview = (content) => {
    setPreviewContent(content);
    onOpen();
  };

  return (
    <Box>
      <Heading mb={6} color={useColorModeValue("gray.800", "white")}>Dataset Manager</Heading>
      <Box p={6} borderRadius="lg" boxShadow="xl" bg={bgColor} backdropFilter="blur(10px)">
        <VStack spacing={4} align="stretch">
          <Flex>
            <Input
              type="file"
              accept=".txt,.pdf,.doc,.docx"
              onChange={handleFileChange}
              display="none"
              id="file-upload"
            />
            <label htmlFor="file-upload">
              <Button as="span" colorScheme="blue" leftIcon={<Icon as={FaFileUpload} />}>
                Select File
              </Button>
            </label>
            {newFile && (
              <Text ml={2} alignSelf="center">
                {newFile.name}
              </Text>
            )}
          </Flex>
          <Button onClick={handleUpload} colorScheme="green" isDisabled={!newFile}>
            Upload Document
          </Button>
          
          <Heading size="md" mt={4}>Your Documents</Heading>
          <List spacing={3}>
            {documents.map((doc) => (
              <ListItem key={doc.id} p={2} borderWidth={1} borderRadius="md" borderColor={borderColor}>
                <Flex justify="space-between" align="center">
                  <Text>{doc.name}</Text>
                  <Flex>
                    <Button size="sm" onClick={() => handlePreview(doc.content)} mr={2}>
                      <Icon as={FaEye} />
                    </Button>
                    <Button size="sm" colorScheme="red" onClick={() => handleDelete(doc.id)}>
                      <Icon as={FaTrash} />
                    </Button>
                  </Flex>
                </Flex>
              </ListItem>
            ))}
          </List>
        </VStack>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Document Preview</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box maxHeight="60vh" overflowY="auto">
              <Text whiteSpace="pre-wrap">{previewContent}</Text>
            </Box>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default DatasetManager;