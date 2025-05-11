const SummaryColumn = ({ summary, summarizeText, ratio, setRatio, loading, disabled }) => {
  return (
    <div className="flex-1 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4 text-black">Generate Summary</h2>
      <div className="flex items-center gap-2 mb-4">
        <label htmlFor="ratio" className="text-sm font-medium text-gray-700">
          Summary Ratio:
        </label>
        <input
          id="ratio"
          type="number"
          min="0.1"
          max="1"
          step="0.1"
          value={ratio}
          onChange={(e) => setRatio(parseFloat(e.target.value))}
          className="w-20 p-2 bg-white text-black border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        className="bg-white text-black border border-gray-600 px-6 py-2 rounded-md hover:bg-gray-200 disabled:bg-gray-400 disabled:text-gray-600 mb-4"
        onClick={summarizeText}
        disabled={loading || disabled}
      >
        {loading ? 'Summarizing...' : 'Generate Summary'}
      </button>
      {summary && (
        <div>
          <h3 className="text-lg font-medium mb-2 text-gray-700">Summary</h3>
          <p className="p-4 bg-white border border-gray-600 rounded-md text-gray-700">{summary}</p>
        </div>
      )}
    </div>
  );
};

export default SummaryColumn;