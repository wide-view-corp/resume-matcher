import React from 'react';
import { Icon, useColorModeValue } from '@chakra-ui/react';
import { FaFile, FaFilePdf, FaFileWord } from 'react-icons/fa';

const FileIcon = ({ type, size = "2em" }) => {
  const color = useColorModeValue("blue.500", "blue.300");

  let IconComponent;
  switch (type) {
    case 'application/pdf':
      IconComponent = FaFilePdf;
      break;
    case 'application/msword':
    case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      IconComponent = FaFileWord;
      break;
    default:
      IconComponent = FaFile;
  }

  return <Icon as={IconComponent} fontSize={size} color={color} />;
};

export default FileIcon;