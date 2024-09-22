'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';
import FileUploader from './components/FileUploader'; // FileUploader component
import ReportEditor from './components/ReportEditor'; // ReportEditor component
import Navbar from './components/Navbar'; // Navbar component
import styles from './styles/page.module.css';

export default function MyPage() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [report, setReport] = useState('');
  const [isReportGenerating, setIsReportGenerating] = useState(false); // State to show loading

  // Function to handle file upload
  const handleFileUpload = (file) => {
    setUploadedFiles((prevFiles) => [...prevFiles, file]);
  };

  // Function to handle report generation
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
        setReport(data.report);
        console.log(report)// Update the editor with the generated report
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
        {/* FileUploader Component */}
        <FileUploader onFileUpload={handleFileUpload} />

        {/* Display uploaded files */}
        {uploadedFiles.length > 0 && (
          <>
            <ul className={styles.fileList}>
              {uploadedFiles.map((file, index) => (
                <li key={index} className={styles.fileItem}>
                  {file.name}
                </li>
              ))}
            </ul>

            {/* Generate Report Button */}
            <motion.button
              className={styles.generateButton}
              onClick={handleGenerateReport}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={isReportGenerating} // Disable button while loading
            >
              {isReportGenerating ? 'Generating Report...' : 'Generate Report'}
            </motion.button>
          </>
        )}
      </motion.section>

      {/* Report Editor Section */}
      <motion.section
        className={styles.editorSection}
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.8, ease: 'easeOut' }}
      >
        <h2 className={styles.editorTitle}>Generated Report</h2>
        <ReportEditor report={report} setReport={setReport} />
      </motion.section>
    </div>
  );
}
