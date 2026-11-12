import { createRoot } from 'react-dom/client';
import Onboarding from './components/Onboarding.jsx';


const rootElement = document.getElementById("onboarding");

if (rootElement) {
const homeUrl = rootElement.getAttribute("data-home-url");

 createRoot(rootElement).render(<Onboarding homeUrl={homeUrl} />)
}





// Standard JS code for django templates not using react 

// THeme toggle