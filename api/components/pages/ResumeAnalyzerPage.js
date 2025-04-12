import React, { useState } from 'react';
import { Box, Button, Textarea, VStack, Heading, Text, useToast, Progress } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const ResumeAnalyzerPage = ({ setStudentId, setStudentData }) => {
  const [resumeText, setResumeText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeText.trim()) {
      toast({
        title: 'Resume text is required',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/analyze_resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: resumeText }),
      });

      if (response.ok) {
        const data = await response.json();
        setStudentId(data.student_id);
        setStudentData(data);
        toast({
          title: 'Resume analyzed successfully!',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        navigate('/dashboard');
      } else {
        const error = await response.json();
        toast({
          title: 'Failed to analyze resume',
          description: error.detail || 'Please try again later',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'An error occurred while analyzing the resume. Please try again later.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      {/* Add your component JSX here */}
    </Box>
  );
};

export default ResumeAnalyzerPage;