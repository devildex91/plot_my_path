import { createRoot } from "react-dom/client";
import Onboarding from "./components/Onboarding.jsx";
import SearchBar from "./components/SearchBar.jsx";
import ItineraryBuilder from "./components/itinerary_builder.jsx";
import { getCookie } from "../utils.js";
const rootElement = document.getElementById("onboarding");
const searchRoot = document.getElementById("searchDiv");
const builder = document.getElementById("builder");
const dataElement = document.getElementById("app-data");
if (rootElement) {
  const homeUrl = rootElement.getAttribute("data-home-url");

  createRoot(rootElement).render(<Onboarding homeUrl={homeUrl} />);
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
// Theme toggle for Django-rendered pages.
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

// Toggle saved-destination state for Django-rendered destination cards.
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

// Start Checkout for Django-rendered payment buttons.
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("#checkout-button");
  if (!btn || btn.disabled) return;

  btn.disabled = true;

  try {
    const res = await fetch(btn.dataset.url, {
      method: "POST",
      headers: { "X-CSRFToken": btn.dataset.csrf },
    });
    const data = await res.json();

    if (data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }
    alert(data.error || "Error: Unable to proceed to payment");
  } catch (err) {
    alert("Payment processing failed");
  }
  btn.disabled = false;
});

// Fade out success and error messages after a short display period.
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll("#message-container .alert");

  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add("fade-out");
    }, 3000);
  });
});

// Confirm before submitting refund or logout forms.
const setupFormConfirmations = () => {
  document
    .getElementById("refund-form")
    ?.addEventListener("submit", (event) => {
      if (!confirm("Refund your purchase and remove premium?")) {
        event.preventDefault();
      }
    });

  document
    .getElementById("logout-form")
    ?.addEventListener("submit", (event) => {
      if (!confirm("Are you sure you want to logout?")) {
        event.preventDefault();
      }
    });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupFormConfirmations);
} else {
  setupFormConfirmations();
}

//confirm before submitting delete trip forms.
const setupDeleteTripConfirmations = () => {
  document.querySelectorAll(".delete-trip-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!confirm("Delete this trip? This cannot be undone.")) {
        event.preventDefault();
      }
    });
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupDeleteTripConfirmations);
} else {
  setupDeleteTripConfirmations();
}

// Submit continent filter forms on change.
const setupContinentFilters = () => {
    document.querySelectorAll(".continent-filter").forEach((radio) => {
        radio.addEventListener("change", () => {
            radio.form.submit();
        });
    });
};

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupContinentFilters);
} else {
    setupContinentFilters();
}