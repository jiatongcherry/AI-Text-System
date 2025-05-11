const TopicClassify = ({ topic, classifyText, loading, disabled }) => {
  return (
    <div className="flex-1 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4 text-black">Classify Topic</h2>
      <button
        className="bg-white text-black border border-gray-600 px-6 py-2 rounded-md hover:bg-gray-200 disabled:bg-gray-400 disabled:text-gray-600 mb-4"
        onClick={classifyText}
        disabled={loading || disabled}
      >
        {loading ? 'Classifying...' : 'Classify Topic'}
      </button>
      {topic && (
        <div>
          <h3 className="text-lg font-medium mb-2 text-gray-700">Predicted Topic</h3>
          <p className="p-4 bg-white border border-gray-600 rounded-md text-gray-700">{topic}</p>
        </div>
      )}
    </div>
  );
};

export default TopicClassify;