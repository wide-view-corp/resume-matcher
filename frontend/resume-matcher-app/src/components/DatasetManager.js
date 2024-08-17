import React, { useState, useRef, useEffect } from 'react';
import {
  Box, Button, VStack, Heading, Text, useToast, List, ListItem, IconButton,
  Flex, Progress, useColorModeValue, Modal, ModalOverlay, ModalContent,
  ModalHeader, ModalFooter, ModalBody, ModalCloseButton, useDisclosure,
  Grid, GridItem, Icon, Divider, Image, Tooltip
} from '@chakra-ui/react';
import { FaFileUpload, FaTrash, FaEye, FaListUl, FaTh } from 'react-icons/fa';
import FileIcon from './FileIcon';
import datasetService from '../services/datasetService';

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
  <Grid templateColumns="repeat(auto-fill, minmax(120px, 1fr))" gap={4}>
    {documents.map((doc) => (
      <GridItem key={doc.id} w="100%" textAlign="center">
        <VStack
          spacing={2}
          p={3}
          borderWidth={1}
          borderRadius="md"
          borderColor={borderColor}
          _hover={{ bg: hoverBg }}
          height="100%"
          justifyContent="space-between"
        >
          <FileIcon type={doc.type} size="3em" />
          <Tooltip label={doc.name} aria-label="Document name">
            <Box width="100%" overflow="hidden">
              <Text
                fontSize="sm"
                fontWeight="medium"
                noOfLines={2}
                textOverflow="ellipsis"
                overflow="hidden"
                wordBreak="break-word"
              >
                {doc.name}
              </Text>
            </Box>
          </Tooltip>
          <Flex mt={2} justifyContent="center" width="100%">
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

  const supportedFileTypes = ['.pdf', '.doc', '.docx', '.txt'];
  const fileInputAccept = supportedFileTypes.join(',');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const fetchedDocuments = await datasetService.getDocuments();
      setDocuments(fetchedDocuments);
    } catch (error) {
      toast({
        title: 'Error fetching documents',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    const unsupportedFiles = files.filter(file => !supportedFileTypes.some(type => file.name.toLowerCase().endsWith(type)));
    
    if (unsupportedFiles.length > 0) {
      toast({
        title: 'Unsupported file type(s)',
        description: `Please upload only ${supportedFileTypes.join(', ')} files.`,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      const existingFiles = files.filter(file => documents.some(doc => doc.name === file.name));
      if (existingFiles.length > 0) {
        const existingFileNames = existingFiles.map(file => file.name).join(', ');
        toast({
          title: 'File(s) already exist',
          description: `The following file(s) already exist: ${existingFileNames}. Please rename or choose different files.`,
          status: 'warning',
          duration: 5000,
          isClosable: true,
        });
        setUploading(false);
        return;
      }

      const uploadedDocuments = await Promise.all(
        files.map(async (file) => {
          const formData = new FormData();
          formData.append('file', file);
          const result = await datasetService.uploadDocument(formData);
          setUploadProgress((prev) => prev + (100 / files.length));
          return result;
        })
      );

      setDocuments(prev => [...prev, ...uploadedDocuments]);
      toast({
        title: `${files.length} document${files.length > 1 ? 's' : ''} uploaded successfully`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error uploading documents',
        description: error.response ? error.response.data.error : error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDelete = async (id) => {
    try {
      await datasetService.deleteDocument(id);
      setDocuments(documents.filter(doc => doc.id !== id));
      toast({
        title: 'Document deleted',
        status: 'info',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error deleting document',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handlePreview = async (doc) => {
    try {
      const content = await datasetService.getDocumentContent(doc.id);
      setPreviewContent({ ...doc, content });
      onOpen();
    } catch (error) {
      toast({
        title: 'Error fetching document content',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const renderPreviewContent = () => {
    switch (previewContent.type) {
      case 'application/pdf':
        return (
          <iframe
            src={previewContent.content}
            width="100%"
            height="500px"
            title="PDF Preview"
          />
        );
      case 'image/jpeg':
      case 'image/png':
      case 'image/gif':
        return (
          <Image
            src={previewContent.content}
            alt={previewContent.name}
            maxWidth="100%"
            maxHeight="500px"
          />
        );
      default:
        return <Text whiteSpace="pre-wrap">{previewContent.content}</Text>;
    }
  };

  return (
    <Box>
      <Heading mb={6} color={textColor}>Dataset Manager</Heading>
      <Box p={6} borderRadius="lg" boxShadow="xl" bg={bgColor}>
        <VStack spacing={6} align="stretch">
          <Box p={5} borderWidth={2} borderRadius="md" borderStyle="dashed" borderColor={borderColor} textAlign="center">
            <input
              type="file"
              multiple
              accept={fileInputAccept}
              onChange={handleFileChange}
              ref={fileInputRef}
              style={{ display: 'none' }}
            />
            <VStack spacing={3}>
              <Icon as={FaFileUpload} fontSize="3xl" color={uploadIconColor} />
              <Tooltip label={`Supported file types: ${supportedFileTypes.join(', ')}`}>
                <Button
                  onClick={() => fileInputRef.current.click()}
                  colorScheme="blue"
                  isLoading={uploading}
                  loadingText="Uploading..."
                >
                  Upload Documents
                </Button>
              </Tooltip>
              <Text fontSize="sm" color={subTextColor}>
                Drag and drop files here or click to select
              </Text>
              <Text fontSize="xs" color={subTextColor}>
                Supported file types: {supportedFileTypes.join(', ')}
              </Text>
            </VStack>
          </Box>
          
          {uploading && (
            <Progress value={uploadProgress} size="sm" colorScheme="blue" />
          )}
          
          <Divider />
          
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
              {renderPreviewContent()}
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