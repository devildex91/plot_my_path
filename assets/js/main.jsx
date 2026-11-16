import { createRoot } from 'react-dom/client';
import Onboarding from './components/Onboarding.jsx';
import SearchBar from './components/SearchBar.jsx';
import ItineraryBuilder from './components/itinerary_builder.jsx';
import { getCookie } from '../utils.js';
const rootElement = document.getElementById("onboarding");
const searchRoot = document.getElementById("searchDiv");
const builder = document.getElementById("builder");
const dataElement = document.getElementById("app-data");
if (rootElement) {
const homeUrl = rootElement.getAttribute("data-home-url");

 createRoot(rootElement).render(<Onboarding homeUrl={homeUrl} />)
}


// Search bar root element 
if (searchRoot) {
  const baseUrl = searchRoot.getAttribute("data-base-url");
  createRoot(searchRoot).render(<SearchBar baseUrl={baseUrl} />);
}
if (builder) {
  const {
    trip,
    preferences,
    days,
    attractions,
    weather,
    weather_error: weatherError,
  } = JSON.parse(dataElement.textContent);
  createRoot(builder).render(
    <ItineraryBuilder
      trip={trip}
      preferences={preferences}
      days={days}
      attractions={attractions}
      weather={weather}
      weatherError={weatherError}
    />,
  );
}
// Standard JS code for django templates not using react 

// Theme toggle
const toggle = document.getElementById("theme-toggle");
const root = document.documentElement;

if (toggle) {
  toggle.checked = root.getAttribute("data-theme") === "sunset";

  toggle.addEventListener("change", () => {
    const theme = toggle.checked ? "sunset" : "fantasy";
    root.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  });
}


// Favourite button for Django-rendered destination cards
document.addEventListener("click", async (e) => {
  const button = e.target.closest(".favourite-btn");

  if (!button || button.disabled) return;

  button.disabled = true;

  try {
    const response = await fetch(button.dataset.url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not update favourite.");
    }

    const icon = button.querySelector("i");

    if (data.is_favourite) {
      icon.classList.replace("fa-regular", "fa-solid");
      icon.classList.add("text-red-500");
      button.setAttribute("aria-label", "Remove from favourites");
    } else {
      icon.classList.replace("fa-solid", "fa-regular");
      icon.classList.remove("text-red-500");
      button.setAttribute("aria-label", "Add to favourites");
    }

  } catch (error) {
    console.error("Favourite error:", error);
  } finally {
    button.disabled = false;
  }
});
