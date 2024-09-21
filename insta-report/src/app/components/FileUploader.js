import { useDropzone } from 'react-dropzone';
import { useState } from 'react';
import styles from '../styles/FileUploader.module.css';

const FileUploader = ({ onFileUpload }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const onDrop = (acceptedFiles) => {
    setSelectedFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
    acceptedFiles.forEach(file => onFileUpload(file));
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: 'application/pdf',
    multiple: true, // Allow multiple files
  });

  // Remove file from the list
  const handleRemoveFile = (index) => {
    setSelectedFiles(selectedFiles.filter((_, i) => i !== index));
  };

  return (
    <div {...getRootProps()} className={styles.uploader}>
      <input {...getInputProps()} />
      <p>Drag & drop PDF files here, or click to select</p>

      {/* Display uploaded files */}
      {selectedFiles.length > 0 && (
        <ul className={styles.fileList}>
          {selectedFiles.map((file, index) => (
            <li key={index} className={styles.fileItem}>
              {file.name}
              <button onClick={() => handleRemoveFile(index)} className={styles.removeButton}>Remove</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FileUploader;
