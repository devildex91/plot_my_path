
import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import Onboarding from "../components/Onboarding.jsx";

describe("Onboarding", () => {
  beforeEach(() => {
    window.DJANGO_STATIC_URL = "/static/";
  });

  it("displays the main onboarding heading", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("heading", { name: "What we do" })
    ).toBeInTheDocument();
  });

  it("displays all three onboarding sections", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("heading", { name: "Personalised Itineraries" })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: "Discover Amazing Destinations" })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: "Real-Time Info" })
    ).toBeInTheDocument();
  });

  it("displays the introductory descriptions", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByText(/Tell us your preferences and we will show you/)
    ).toBeInTheDocument();

    expect(
      screen.getByText(/Explore top attractions, hidden gems and local favourites/)
    ).toBeInTheDocument();

    expect(
      screen.getByText(/Get timely weather updates and smart recommendations/)
    ).toBeInTheDocument();
  });

  it("provides a skip link to the home page", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(screen.getByRole("link", { name: "skip" })).toHaveAttribute(
      "href",
      "/home/"
    );
  });

  it("provides next and previous links between slides", () => {
    render(<Onboarding homeUrl="/home/" />);

    const nextLinks = screen.getAllByRole("link", { name: "Next" });

    expect(nextLinks).toHaveLength(2);
    expect(nextLinks[0]).toHaveAttribute("href", "#item2");
    expect(nextLinks[1]).toHaveAttribute("href", "#item3");

    expect(screen.getAllByRole("link", { name: "❮" })).toHaveLength(2);
    expect(screen.getAllByRole("link", { name: "❮" })[0]).toHaveAttribute(
      "href",
      "#item1"
    );
    expect(screen.getAllByRole("link", { name: "❮" })[1]).toHaveAttribute(
      "href",
      "#item2"
    );
  });

  it("provides a Get Started link to the home page", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("link", { name: "Get Started" })
    ).toHaveAttribute("href", "/home/");
  });

  it("displays all three onboarding images with descriptive alternative text", () => {
    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("img", {
        name: "Items on table while planning for a trip",
      })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("img", {
        name: "A person discovering new places",
      })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("img", {
        name: "Real time data being used to plan a trip",
      })
    ).toBeInTheDocument();
  });

  it("uses the Django static URL for onboarding images", () => {
    window.DJANGO_STATIC_URL = "/custom-static/";

    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("img", {
        name: "Items on table while planning for a trip",
      })
    ).toHaveAttribute(
      "src",
      "/custom-static/images/personalised_itinery.avif"
    );

    expect(
      screen.getByRole("img", {
        name: "A person discovering new places",
      })
    ).toHaveAttribute(
      "src",
      "/custom-static/images/new_discovery.avif"
    );

    expect(
      screen.getByRole("img", {
        name: "Real time data being used to plan a trip",
      })
    ).toHaveAttribute(
      "src",
      "/custom-static/images/real_time.avif"
    );
  });

  it("uses the default static URL when Django static URL is unavailable", () => {
    delete window.DJANGO_STATIC_URL;

    render(<Onboarding homeUrl="/home/" />);

    expect(
      screen.getByRole("img", {
        name: "Items on table while planning for a trip",
      })
    ).toHaveAttribute(
      "src",
      "/static/images/personalised_itinery.avif"
    );
  });
});
