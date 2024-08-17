import React from 'react';
import { Box, Heading, Text, SimpleGrid, Icon } from '@chakra-ui/react';
import { FaChartLine, FaCalendarAlt } from 'react-icons/fa';

const Dashboard = () => {
  return (
    <Box>
      <Heading mb={6} color="white">Welcome to Your Dashboard</Heading>
      <SimpleGrid columns={2} spacing={6}>
        <Box p={6} borderRadius="lg" boxShadow="md" bg="white" backdropFilter="blur(10px)" backgroundColor="rgba(255,255,255,0.8)">
          <Heading size="md" mb={4} display="flex" alignItems="center">
            <Icon as={FaChartLine} mr={2} /> Recent Activity
          </Heading>
          <Text>You have no recent activity.</Text>
        </Box>
        <Box p={6} borderRadius="lg" boxShadow="md" bg="white" backdropFilter="blur(10px)" backgroundColor="rgba(255,255,255,0.8)">
          <Heading size="md" mb={4} display="flex" alignItems="center">
            <Icon as={FaCalendarAlt} mr={2} /> Quick Stats
          </Heading>
          <Text>No stats available yet.</Text>
        </Box>
      </SimpleGrid>
    </Box>
  );
};

export default Dashboard;
