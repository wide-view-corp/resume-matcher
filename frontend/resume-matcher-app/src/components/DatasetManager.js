import React, { useState, useRef } from 'react';
import {
  Box, Button, VStack, Heading, Text, useToast, List, ListItem, IconButton,
  Flex, Progress, useColorModeValue, Modal, ModalOverlay, ModalContent,
  ModalHeader, ModalFooter, ModalBody, ModalCloseButton, useDisclosure,
  Grid, GridItem, Icon, Divider
} from '@chakra-ui/react';
import { FaFileUpload, FaTrash, FaEye, FaListUl, FaTh } from 'react-icons/fa';
import FileIcon from './FileIcon';  // Make sure this path is correct

const ListView = ({ documents, handlePreview, handleDelete, borderColor, hoverBg }) => (
  <List spacing={3}>
    {documents.map((doc) => (
      <ListItem key={doc.id} p={3} borderWidth={1} borderRadius="md" borderColor={borderColor} _hover={{ bg: hoverBg }}>
        <Flex justify="space-between" align="center">
          <Flex align="center" flex={1}>
            <FileIcon type={doc.type} size="1.5em" />
            <Text ml={3} fontWeight="medium">{doc.name}</Text>
          </Flex>
          <Flex>
            <IconButton
              icon={<FaEye />}
              onClick={() => handlePreview(doc)}
              aria-label="Preview"
              size="sm"
              mr={2}
              variant="ghost"
            />
            <IconButton
              icon={<FaTrash />}
              onClick={() => handleDelete(doc.id)}
              aria-label="Delete"
              size="sm"
              colorScheme="red"
              variant="ghost"
            />
          </Flex>
        </Flex>
      </ListItem>
    ))}
  </List>
);

const GridView = ({ documents, handlePreview, handleDelete, borderColor, hoverBg }) => (
  <Grid templateColumns="repeat(auto-fill, minmax(120px, 1fr))" gap={6}>
    {documents.map((doc) => (
      <GridItem key={doc.id} w="100%" textAlign="center">
        <VStack spacing={2} p={3} borderWidth={1} borderRadius="md" borderColor={borderColor} _hover={{ bg: hoverBg }}>
          <FileIcon type={doc.type} size="3em" />
          <Text fontSize="sm" fontWeight="medium" noOfLines={2}>{doc.name}</Text>
          <Flex mt={2}>
            <IconButton
              icon={<FaEye />}
              onClick={() => handlePreview(doc)}
              aria-label="Preview"
              size="sm"
              mr={1}
              variant="ghost"
            />
            <IconButton
              icon={<FaTrash />}
              onClick={() => handleDelete(doc.id)}
              aria-label="Delete"
              size="sm"
              colorScheme="red"
              variant="ghost"
            />
          </Flex>
        </VStack>
      </GridItem>
    ))}
  </Grid>
);

const DatasetManager = () => {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [previewContent, setPreviewContent] = useState({ name: '', content: '', type: '' });
  const [isGridView, setIsGridView] = useState(false);
  const fileInputRef = useRef(null);
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.600");
  const hoverBg = useColorModeValue("gray.50", "gray.700");
  const textColor = useColorModeValue("gray.800", "white");
  const subTextColor = useColorModeValue("gray.600", "gray.400");
  const uploadIconColor = useColorModeValue("blue.500", "blue.300");

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    setUploading(true);
    setUploadProgress(0);

    const newDocuments = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const document = await readFile(file);
      newDocuments.push(document);
      setUploadProgress(((i + 1) / files.length) * 100);
    }

    setDocuments(prev => [...prev, ...newDocuments]);
    setUploading(false);
    
    toast({
      title: `${files.length} document${files.length > 1 ? 's' : ''} uploaded successfully`,
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  const readFile = (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve({
          id: Date.now() + Math.random(),
          name: file.name,
          content: e.target.result,
          type: file.type
        });
      };
      if (file.type === 'application/pdf') {
        reader.readAsDataURL(file);
      } else {
        reader.readAsText(file);
      }
    });
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

  const handlePreview = (doc) => {
    setPreviewContent(doc);
    onOpen();
  };

  return (
    <Box>
      <Heading mb={6} color={textColor}>Dataset Manager</Heading>
      <Box p={6} borderRadius="lg" boxShadow="xl" bg={bgColor}>
        <VStack spacing={6} align="stretch">
          {/* Upload Section */}
          <Box p={5} borderWidth={2} borderRadius="md" borderStyle="dashed" borderColor={borderColor} textAlign="center">
            <input
              type="file"
              multiple
              accept=".txt,.pdf,.doc,.docx"
              onChange={handleFileChange}
              ref={fileInputRef}
              style={{ display: 'none' }}
            />
            <VStack spacing={3}>
              <Icon as={FaFileUpload} fontSize="3xl" color={uploadIconColor} />
              <Button
                onClick={() => fileInputRef.current.click()}
                colorScheme="blue"
                isLoading={uploading}
                loadingText="Uploading..."
              >
                Upload Documents
              </Button>
              <Text fontSize="sm" color={subTextColor}>
                Drag and drop files here or click to select
              </Text>
            </VStack>
          </Box>
          
          {uploading && (
            <Progress value={uploadProgress} size="sm" colorScheme="blue" />
          )}
          
          <Divider />
          
          {/* Document List Section */}
          <Flex justify="space-between" align="center">
            <Heading size="md">Your Documents</Heading>
            <Flex align="center">
              <IconButton
                icon={<FaListUl />}
                aria-label="List View"
                size="sm"
                mr={2}
                variant={!isGridView ? "solid" : "outline"}
                onClick={() => setIsGridView(false)}
              />
              <IconButton
                icon={<FaTh />}
                aria-label="Grid View"
                size="sm"
                variant={isGridView ? "solid" : "outline"}
                onClick={() => setIsGridView(true)}
              />
            </Flex>
          </Flex>
          {documents.length > 0 ? (
            isGridView 
              ? <GridView documents={documents} handlePreview={handlePreview} handleDelete={handleDelete} borderColor={borderColor} hoverBg={hoverBg} />
              : <ListView documents={documents} handlePreview={handlePreview} handleDelete={handleDelete} borderColor={borderColor} hoverBg={hoverBg} />
          ) : (
            <Text textAlign="center" color={subTextColor}>
              No documents uploaded yet. Start by uploading some files!
            </Text>
          )}
        </VStack>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{previewContent.name}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box maxHeight="60vh" overflowY="auto">
              {previewContent.type === 'application/pdf' ? (
                <iframe
                  src={previewContent.content}
                  width="100%"
                  height="500px"
                  title="PDF Preview"
                />
              ) : (
                <Text whiteSpace="pre-wrap">{previewContent.content}</Text>
              )}
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