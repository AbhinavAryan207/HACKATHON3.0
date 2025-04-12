// App.js
import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, VStack, Grid, theme, Container, Heading, Text } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import ResumeAnalyzerPage from './pages/ResumeAnalyzerPage';
import CareerExplorerPage from './pages/CareerExplorerPage';
import LearningPathPage from './pages/LearningPathPage';
import ProfilePage from './pages/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  const [studentId, setStudentId] = useState(localStorage.getItem('studentId') || null);
  const [studentData, setStudentData] = useState(null);
  
  useEffect(() => {
    if (studentId) {
      localStorage.setItem('studentId', studentId);
      fetchStudentData();
    }
  }, [studentId]);
  
  const fetchStudentData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/student/${studentId}`);
      if (response.ok) {
        const data = await response.json();
        setStudentData(data);
      } else {
        console.error('Failed to fetch student data');
        // Clear invalid student ID
        setStudentId(null);
        localStorage.removeItem('studentId');
      }
    } catch (error) {
      console.error('Error fetching student data:', error);
    }
  };
  
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Box textAlign="center" fontSize="xl">
          <Header studentId={studentId} />
          <Container maxW="container.xl" py={5}>
            <Routes>
              <Route path="/" element={
                <HomePage 
                  studentId={studentId} 
                  setStudentId={setStudentId} 
                />
              } />
              <Route path="/dashboard" element={
                <DashboardPage 
                  studentId={studentId} 
                  studentData={studentData} 
                  fetchStudentData={fetchStudentData} 
                />
              } />
              <Route path="/resume-analyzer" element={
                <ResumeAnalyzerPage 
                  setStudentId={setStudentId} 
                  setStudentData={setStudentData} 
                />
              } />
              <Route path="/career-explorer" element={
                <CareerExplorerPage 
                  studentId={studentId} 
                  studentData={studentData} 
                />
              } />
              <Route path="/learning-path" element={
                <LearningPathPage 
                  studentId={studentId} 
                  studentData={studentData} 
                  fetchStudentData={fetchStudentData} 
                />
              } />
              <Route path="/profile" element={
                <ProfilePage 
                  studentId={studentId} 
                  studentData={studentData} 
                  fetchStudentData={fetchStudentData} 
                />
              } />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </Container>
          <Footer />
        </Box>
      </Router>
    </ChakraProvider>
  );
}

export default App;
