import { useState } from 'react';
import axios from 'axios';
import TextInput from './components/TextInput';
import ExtractColumn from './components/ExtractColumn';
import SummaryColumn from './components/SummaryColumn';
import TopicClassify from './components/TopicClassify';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [summary, setSummary] = useState('');
  const [topic, setTopic] = useState('');
  const [ratio, setRatio] = useState(0.3);
  const [loading, setLoading] = useState({ keywords: false, summary: false, topic: false });
  const [error, setError] = useState('');

  const extractKeywords = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setLoading({ ...loading, keywords: true });
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/extract_keywords', {
        text,
        top_n: 5,
      });
      setKeywords(response.data.keywords);
    } catch (err) {
      setError('Failed to extract keywords. Please try again.');
    }
    setLoading({ ...loading, keywords: false });
  };

  const summarizeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setLoading({ ...loading, summary: true });
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/summarize', {
        text,
        ratio,
      });
      setSummary(response.data.summary);
    } catch (err) {
      setError('Failed to generate summary. Please try again.');
    }
    setLoading({ ...loading, summary: false });
  };

  const classifyText = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setLoading({ ...loading, topic: true });
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/classify_topic', {
        text,
      });
      setTopic(response.data.topic);
    } catch (err) {
      setError('Failed to classify topic. Please try again.');
    }
    setLoading({ ...loading, topic: false });
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col p-6">
      <div className="flex-1 flex flex-col justify-center items-center">
        <h1 className="text-6xl font-bold mb-8">AI-powered Text Analysis System</h1>
        <TextInput text={text} setText={setText} setError={setError} />
        {error && <p className="text-red-500 mt-4">{error}</p>}
      </div>
      <div className="flex-1 flex justify-center items-start">
        <div className="w-full max-w-5xl flex flex-col md:flex-row gap-6">
          <ExtractColumn
            keywords={keywords}
            extractKeywords={extractKeywords}
            loading={loading.keywords}
            disabled={loading.keywords}
          />
          <SummaryColumn
            summary={summary}
            summarizeText={summarizeText}
            ratio={ratio}
            setRatio={setRatio}
            loading={loading.summary}
            disabled={loading.summary}
          />
          <TopicClassify
            topic={topic}
            classifyText={classifyText}
            loading={loading.topic}
            disabled={loading.topic}
          />
        </div>
      </div>
    </div>
  );
}

export default App;