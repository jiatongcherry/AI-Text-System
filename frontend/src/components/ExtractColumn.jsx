const ExtractColumn = ({ keywords, extractKeywords, loading, disabled }) => {
  return (
    <div className="flex-1 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4 text-black">Extract Keywords</h2>
      <button
        className="bg-white text-black border border-gray-600 px-6 py-2 rounded-md hover:bg-gray-200 disabled:bg-gray-400 disabled:text-gray-600 mb-4"
        onClick={extractKeywords}
        disabled={loading || disabled}
      >
        {loading ? 'Extracting...' : 'Extract Keywords'}
      </button>
      {keywords.length > 0 && (
        <div>
          <h3 className="text-lg font-medium mb-2 text-gray-700">Keywords</h3>
          <ul className="list-disc pl-6 text-gray-700">
           {keywords.map((keyword, index) => (
              <li key={index} className="mb-1">
                {keyword}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ExtractColumn;