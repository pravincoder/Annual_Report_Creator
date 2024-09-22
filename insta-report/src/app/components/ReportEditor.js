import { marked } from 'marked';
import styles from '../styles/report.module.css';
import { useState } from 'react';

const ReportReader = ({ report }) => {
  const [showPreview, setShowPreview] = useState(true); // Always show the preview

  return (
    <div className={styles['report-reader-container']}>
      <div className={styles.toolbar}>
        <button 
          onClick={() => setShowPreview(!showPreview)} 
          className={styles['toggle-preview-btn']}
        >
          {showPreview ? 'Hide Preview' : 'Show Preview'}
        </button>
      </div>

      {showPreview && (
        <div 
          className={styles['markdown-preview']} 
          dangerouslySetInnerHTML={{ __html: marked(report) }} 
        />
      )}
    </div>
  );
};

export default ReportReader;
