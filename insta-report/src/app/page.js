'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';
import FileUploader from './components/FileUploader';
import Navbar from './components/Navbar';
import ReportEditor from './components/ReportEditor'; // Import the new ReportEditor component
import styles from './styles/page.module.css';

export default function MyPage() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [reportHtml, setReportHtml] = useState('');
  const [isReportGenerating, setIsReportGenerating] = useState(false);

  // Function to handle file upload (update)
  const handleFileUpload = (file) => {
    setUploadedFiles((prevFiles) => [...prevFiles, file]); // Append new file
  };

  // Function to handle report generation (no changes)
  const handleGenerateReport = async () => {
    if (uploadedFiles.length === 0) return alert('Please upload a file first');

    setIsReportGenerating(true); // Set loading state
    const formData = new FormData();

    uploadedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/report/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate report');
      }

      const data = await response.json();
      if (data.error) {
        console.error('Error:', data.error);
      } else {
        let cleanedHtml = data.report;
        if (cleanedHtml.startsWith('```html')) {
          cleanedHtml = cleanedHtml.replace(/^```html/, '').trim(); // Remove the opening tag
        }
        if (cleanedHtml.endsWith('```')) {
          cleanedHtml = cleanedHtml.replace(/```$/, '').trim(); // Remove the closing tag
        }

        setReportHtml(cleanedHtml); // Store the cleaned HTML code in state
        console.log(cleanedHtml); // For debugging purposes
      }
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setIsReportGenerating(false); // Reset loading state
    }
  };

  return (
    <div className={styles.pageContainer}>
      {/* Navbar */}
      <Navbar />

      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        className={styles.header}
      >
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>InstaReport</span>
        </h1>
        <p className={styles.tagline}>
          <span className={styles.animatedText}>Effortless</span>,{' '}
          <span className={styles.animatedText}>AI-Driven</span> Reports Tailored
          to Your Data.
        </p>
      </motion.header>

      {/* File Uploader Section */}
      <motion.section
        className={styles.section}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.5, duration: 0.8, ease: 'easeOut' }}
      >
        <h2 className={styles.sectionTitle}>Select PDF Files to Upload</h2>
        <FileUploader onFileUpload={handleFileUpload} />

        {uploadedFiles.length > 0 && (
          <>
            <ul className={styles.fileList}>
              {uploadedFiles.map((file, index) => (
                <li key={index} className={styles.fileItem}>
                  {file.name}
                </li>
              ))}
            </ul>

            <motion.button
              className={styles.generateButton}
              onClick={handleGenerateReport}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={isReportGenerating}
            >
              {isReportGenerating ? 'Generating Report...' : 'Generate Report'}
            </motion.button>
          </>
        )}
      </motion.section>

      {/* Render the ReportEditor component */}
      {reportHtml && <ReportEditor reportHtml={reportHtml} />}
    </div>
  );
}