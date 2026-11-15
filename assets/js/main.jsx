import { createRoot } from 'react-dom/client';
import Onboarding from './components/Onboarding.jsx';
import SearchBar from './components/SearchBar.jsx';

const rootElement = document.getElementById("onboarding");
const searchRoot = document.getElementById("searchDiv");
if (rootElement) {
const homeUrl = rootElement.getAttribute("data-home-url");

 createRoot(rootElement).render(<Onboarding homeUrl={homeUrl} />)
}


// Search bar root element 
if (searchRoot) {
  const baseUrl = searchRoot.getAttribute("data-base-url");
  createRoot(searchRoot).render(<SearchBar baseUrl={baseUrl} />);
}

// Standard JS code for django templates not using react 

