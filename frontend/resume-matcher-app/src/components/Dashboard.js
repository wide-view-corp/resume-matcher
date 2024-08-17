import React from 'react';
import { Box, Heading, Text, SimpleGrid } from '@chakra-ui/react';

const Dashboard = () => {
  return (
    <Box>
      <Heading mb={6}>Welcome to Your Dashboard</Heading>
      <SimpleGrid columns={2} spacing={6}>
        <Box p={6} borderRadius="lg" boxShadow="md" bg="white">
          <Heading size="md" mb={4}>Recent Activity</Heading>
          <Text>You have no recent activity.</Text>
        </Box>
        <Box p={6} borderRadius="lg" boxShadow="md" bg="white">
          <Heading size="md" mb={4}>Quick Stats</Heading>
          <Text>No stats available yet.</Text>
        </Box>
      </SimpleGrid>
    </Box>
  );
};

export default Dashboard;