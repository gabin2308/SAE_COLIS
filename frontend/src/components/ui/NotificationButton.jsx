import { useNavigate } from "react-router-dom";

export default function NotificationButton() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/notification"); // Assure-toi que le chemin correspond à ton router.jsx
  };

  return (
    <button 
      onClick={handleClick} 
      className="relative p-2 text-slate-600 hover:text-[#0d2a4a] transition-colors"
    >
      🔔
    </button>
  );
}