import React from 'react';
import { Box, Heading, Text, SimpleGrid, Divider } from '@chakra-ui/react';

const Dashboard = () => {
  return (
    <Box>
      <Heading mb={6} fontSize="2xl" color="brand.600">
        Welcome to Your Dashboard
      </Heading>
      <Divider mb={6} borderColor="gray.200" />
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
        <Box p={6} borderRadius="lg" boxShadow="xl" bg="white" transition="transform 0.3s" _hover={{ transform: 'scale(1.05)' }}>
          <Heading size="md" mb={4}>Recent Activity</Heading>
          <Text color="gray.600">You have no recent activity.</Text>
        </Box>
        <Box p={6} borderRadius="lg" boxShadow="xl" bg="white" transition="transform 0.3s" _hover={{ transform: 'scale(1.05)' }}>
          <Heading size="md" mb={4}>Quick Stats</Heading>
          <Text color="gray.600">No stats available yet.</Text>
        </Box>
      </SimpleGrid>
    </Box>
  );
};

export default Dashboard;
