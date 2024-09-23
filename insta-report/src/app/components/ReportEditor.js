import { motion } from 'framer-motion';
import styles from '../styles/report.module.css'; // Create a new CSS file for styling

export default function ReportEditor({ reportHtml }) {
  return (
    <motion.section
      className={styles.editorSection}
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.7, duration: 0.8, ease: 'easeOut' }}
    >
      <h2 className={styles.editorTitle}>Generated Report</h2>
      
      {/* Options for actions like download or export */}
      <div className={styles.actionBar}>
        <button className={styles.actionButton}>Download as PDF</button>
        <button className={styles.actionButton}>Share Report</button>
      </div>

      {/* Render the compiled HTML safely */}
      <div
        dangerouslySetInnerHTML={{ __html: reportHtml }}
        className={styles.reportOutput}
      />
    </motion.section>
  );
}