const TextInput = ({ text, setText, setError }) => {
  return (
    <div className="w-full max-w-2xl">
      <h2 className="text-xl font-semibold mb-4 text-white">Enter Your Text</h2>
      <textarea
        className="w-full h-40 p-4 bg-white text-black border-4 border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Enter your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
    </div>
  );
};

export default TextInput;