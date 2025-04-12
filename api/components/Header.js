// components/Header.js
import React from 'react';
import { Box, Flex, Text, Button, Stack, Link, useColorModeValue, useDisclosure } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

const Header = ({ studentId }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const handleToggle = () => (isOpen ? onClose() : onOpen());

  return (
    <Box bg={useColorModeValue('blue.500', 'blue.900')} px={4} boxShadow="md">
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <RouterLink to="/">
          <Text fontSize="xl" fontWeight="bold" color="white">
            PathfinderAI
          </Text>
        </RouterLink>

        <Flex alignItems="center">
          <Stack direction="row" spacing={4} display={{ base: 'none', md: 'flex' }}>
            {studentId ? (
              <>
                <NavLink to="/dashboard">Dashboard</NavLink>
                <NavLink to="/career-explorer">Careers</NavLink>
                <NavLink to="/learning-path">Learning Path</NavLink>
                <NavLink to="/profile">Profile</NavLink>
              </>
            ) : (
              <NavLink to="/resume-analyzer">Get Started</NavLink>
            )}
          </Stack>
        </Flex>
      </Flex>
    </Box>
  );
};

const NavLink = ({ children, to }) => (
  <RouterLink to={to}>
    <Link
      px={2}
      py={1}
      rounded="md"
      color="white"
      _hover={{
        textDecoration: 'none',
        bg: 'blue.600',
      }}
    >
      {children}
    </Link>
  </RouterLink>
);

export default Header;
