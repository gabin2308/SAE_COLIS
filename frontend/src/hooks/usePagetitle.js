import { useEffect } from "react";

export default function usePageTitle(title) {
  useEffect(() => {
    document.title = `${title}  - Sorbonne Paris Nord`;
  }, [title]);
}