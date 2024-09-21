import dynamic from 'next/dynamic';
import 'react-quill/dist/quill.snow.css';

const ReactQuill = dynamic(() => import('react-quill'), { ssr: false });

const ReportEditor = ({ report, setReport }) => {
  const handleChange = (content) => {
    setReport(content);
  };

  return (
    <div>
      <ReactQuill
        theme="snow"
        value={report}
        onChange={handleChange}
        placeholder="Your AI-Generated Report will appear here......"
      />
    </div>
  );
};

export default ReportEditor;
