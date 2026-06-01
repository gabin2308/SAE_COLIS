export default function Toast({ message, type }) {
  const styles = {
    success: "bg-green-600 border-green-700",
    error: "bg-red-600 border-red-700",
    info: "bg-blue-600 border-blue-700"
  };

  return (
    <div className={`fixed bottom-5 right-5 z-50 px-6 py-3 rounded-lg shadow-2xl text-white border-l-4 ${styles[type] || styles.info}`}>
      <p className="font-semibold">{message}</p>
    </div>
  );
}